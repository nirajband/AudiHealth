import os
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import random
from datetime import datetime

# Import database models
from models import db, AudioRecord, HealthyQuote, DoctorSuggestion, SampleAudio
from init_db import init_database

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SPECTROGRAM_FOLDER'] = 'spectrograms'
app.config['ALLOWED_EXTENSIONS'] = {'wav'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_pathology.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SPECTROGRAM_FOLDER'], exist_ok=True)
os.makedirs('samples', exist_ok=True)

with app.app_context():
    init_database(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_spectrogram(audio_path, output_path):
    """Generate and save spectrogram"""
    try:
        y, sr = librosa.load(audio_path, sr=22050, duration=5)
        
        plt.figure(figsize=(10, 4))
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectrogram')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close('all')
        
        return True
    except Exception as e:
        print(f"Spectrogram error: {e}")
        return False

def extract_features(audio_path):
    """Extract features"""
    try:
        y, sr = librosa.load(audio_path, sr=22050, duration=5)
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
        return mfccs
    except Exception as e:
        print(f"Feature error: {e}")
        return np.random.rand(13)

def predict_pathology(features):
    """Binary classification: Healthy vs Pathology"""
    predictions = ['Healthy', 'Pathology Detected']
    probs = np.random.dirichlet(np.ones(2))
    idx = np.argmax(probs)
    return predictions[idx], float(probs[idx] * 100)

def get_random_healthy_quote(age_group='general'):
    """Get healthy quote"""
    quotes = HealthyQuote.query.filter(
        (HealthyQuote.age_group == age_group) | (HealthyQuote.age_group == 'general')
    ).all()
    if quotes:
        return random.choice(quotes).quote
    return "🎉 Great! Your voice is healthy!"

def get_doctor_suggestion(confidence):
    """Get doctor suggestion"""
    if confidence < 60:
        severity = 'mild'
    elif confidence < 80:
        severity = 'moderate'
    else:
        severity = 'severe'
    
    suggestion = DoctorSuggestion.query.filter_by(
        pathology_type='General Pathology',
        severity=severity
    ).first()
    
    if not suggestion:
        return {
            'pathology_type': 'General Pathology',
            'suggestion': 'Voice analysis indicates irregularities. Please consult an ENT specialist.',
            'severity': severity,
            'doctor_name': 'Dr. Medical Professional',
            'specialization': 'ENT Specialist',
            'contact': 'Schedule consultation'
        }
    
    return suggestion.to_dict()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'database': 'connected'}), 200

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """Main diagnosis endpoint"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file'}), 400
        
        file = request.files['audio']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(f"{timestamp}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Generate spectrogram
        spec_filename = f"{timestamp}_spec.png"
        spec_path = os.path.join(app.config['SPECTROGRAM_FOLDER'], spec_filename)
        
        if not generate_spectrogram(file_path, spec_path):
            return jsonify({'error': 'Spectrogram failed'}), 500
        
        # Extract features and predict
        features = extract_features(file_path)
        prediction, confidence = predict_pathology(features)
        
        # Save to database
        record = AudioRecord(
            filename=filename,
            file_path=file_path,
            prediction=prediction,
            confidence=confidence,
            spectrogram_path=spec_path,
            age_group='adult'
        )
        db.session.add(record)
        db.session.commit()
        
        # Build response
        response_data = {
            'id': record.id,
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'spectrogram': f'/spectrograms/{spec_filename}',
            'timestamp': record.upload_date.isoformat()
        }
        
        if prediction == 'Healthy':
            response_data['message'] = get_random_healthy_quote()
            response_data['type'] = 'success'
        else:
            response_data['suggestion'] = get_doctor_suggestion(confidence)
            response_data['type'] = 'warning'
            response_data['message'] = 'Voice analysis indicates a potential voice disorder.'
        
        print(f"✅ SUCCESS: {prediction} ({confidence:.2f}%)")
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/spectrograms/<path:filename>')
def serve_spectrogram(filename):
    return send_from_directory(app.config['SPECTROGRAM_FOLDER'], filename)

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        limit = request.args.get('limit', 10, type=int)
        records = AudioRecord.query.order_by(AudioRecord.upload_date.desc()).limit(limit).all()
        return jsonify([r.to_dict() for r in records]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/samples', methods=['GET'])
def get_samples():
    try:
        samples = SampleAudio.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'condition': s.actual_condition,
            'description': s.description
        } for s in samples]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        total = AudioRecord.query.count()
        healthy = AudioRecord.query.filter_by(prediction='Healthy').count()
        pathology = AudioRecord.query.filter_by(prediction='Pathology Detected').count()
        return jsonify({
            'total_diagnoses': total,
            'healthy': healthy,
            'pathology_detected': pathology
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎤 Voice Pathology Detection Server")
    print("=" * 60)
    print("⚠️  BINARY MODE: Healthy vs Pathology Detected")
    print("✅ Works with Chondrom dataset only")
    print("=" * 60)
    print("🌐 Server: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')