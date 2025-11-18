from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class AudioRecord(db.Model):
    """Store audio file records and predictions"""
    __tablename__ = 'audio_records'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    prediction = db.Column(db.String(100))  # 'Healthy', 'Laryngitis', 'Vocal Polyp'
    confidence = db.Column(db.Float)
    spectrogram_path = db.Column(db.String(500))
    age_group = db.Column(db.String(50))  # 'child', 'teen', 'adult'
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AudioRecord {self.filename} - {self.prediction}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat(),
            'prediction': self.prediction,
            'confidence': self.confidence,
            'spectrogram_path': self.spectrogram_path,
            'age_group': self.age_group
        }


class HealthyQuote(db.Model):
    """Store playful quotes for healthy voice results"""
    __tablename__ = 'healthy_quotes'
    
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    age_group = db.Column(db.String(50))  # 'child', 'teen', 'general'
    
    def __repr__(self):
        return f'<HealthyQuote {self.id}>'


class DoctorSuggestion(db.Model):
    """Store doctor suggestions for unhealthy voice results"""
    __tablename__ = 'doctor_suggestions'
    
    id = db.Column(db.Integer, primary_key=True)
    pathology_type = db.Column(db.String(100), nullable=False)  # 'Laryngitis', 'Vocal Polyp'
    suggestion = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50))  # 'mild', 'moderate', 'severe'
    doctor_name = db.Column(db.String(200))
    specialization = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<DoctorSuggestion {self.pathology_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pathology_type': self.pathology_type,
            'suggestion': self.suggestion,
            'severity': self.severity,
            'doctor_name': self.doctor_name,
            'specialization': self.specialization,
            'contact': self.contact
        }


class SampleAudio(db.Model):
    """Store sample audio files for testing"""
    __tablename__ = 'sample_audios'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    actual_condition = db.Column(db.String(100))  # 'Healthy', 'Laryngitis', 'Vocal Polyp'
    description = db.Column(db.Text)
    age_group = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<SampleAudio {self.name} - {self.actual_condition}>'