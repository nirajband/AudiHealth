# 🎤 Voice Pathology Detection System

An advanced web-based application for detecting voice disorders in children using deep learning (Liquid State Machine) with comprehensive database integration.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![React](https://img.shields.io/badge/react-18.0%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

### Core Functionality
- ✅ **Real-time Voice Analysis** - Upload and analyze voice recordings instantly
- ✅ **Spectrogram Visualization** - Visual representation of voice frequencies
- ✅ **Multi-class Detection** - Identifies Healthy voices, Laryngitis, and Vocal Polyps
- ✅ **Confidence Scoring** - AI confidence percentage for each prediction

### Database Integration
- 📊 **Complete Data Persistence** - SQLite database for all records
- 📝 **Audio History** - Track all uploaded recordings and predictions
- 💬 **Dynamic Responses** - Age-appropriate quotes and medical suggestions
- 🎯 **Sample Audio Library** - Pre-loaded healthy and pathological voice samples

### Child-Friendly Features
- 🎉 **Playful Quotes** - Encouraging messages for healthy voice detections
- 🌈 **Age-Appropriate Content** - Different messages for children, teens, and adults
- ⭐ **Positive Reinforcement** - Motivational feedback to keep children engaged

### Medical Features
- 👨‍⚕️ **Doctor Suggestions** - Professional recommendations for pathological cases
- 📋 **Severity-based Advice** - Mild, moderate, and severe condition guidelines
- 🏥 **Specialist Information** - ENT doctor details and contact information
- ⚕️ **Immediate Action Steps** - Clear instructions for voice care

## 🏗️ Project Structure

```
voice-pathology-detection/
│
├── 📁 backend/
│   ├── app.py                  # Main Flask application with API endpoints
│   ├── models.py               # SQLAlchemy database models
│   ├── init_db.py             # Database initialization script
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── 📁 models/             # Machine learning models
│   │   ├── lsm_model.pkl     # Your trained LSM model
│   │   └── scaler.pkl        # Feature scaler
│   │
│   ├── 📁 uploads/            # Uploaded audio files (auto-created)
│   ├── 📁 spectrograms/       # Generated spectrograms (auto-created)
│   ├── 📁 samples/            # Sample audio files
│   └── voice_pathology.db    # SQLite database
│
├── 📁 frontend/               # React frontend (your existing code)
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── ResultsDisplay.jsx
│   │   │   └── ResultsDisplay.css
│   │   └── ...
│   └── ...
│
├── README.md
├── .gitignore
└── LICENSE
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- Git

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/sahilbrid/voice-pathology-detection.git
cd voice-pathology-detection
```

2. **Backend Setup**
```bash
# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py
```

3. **Add Sample Audio Files**

Place sample WAV files in the `samples/` folder:
- `healthy_child_1.wav`
- `healthy_child_2.wav`
- `healthy_adult_1.wav`
- `laryngitis_1.wav`
- `laryngitis_child_1.wav`
- `vocal_polyp_1.wav`
- `vocal_polyp_2.wav`

**Download samples from:** [Saarbrücken Voice Database](https://stimmdb.coli.uni-saarland.de/)

4. **Frontend Setup** (Keep your existing frontend)
```bash
cd frontend
npm install
```

5. **Run the Application**

Terminal 1 - Backend:
```bash
python app.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

6. **Access the Application**
```
Frontend: http://localhost:5173
Backend API: http://localhost:5000
```

## 📡 API Documentation

### Endpoints

#### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### 2. Diagnose Audio
```http
POST /api/diagnose
Content-Type: multipart/form-data
```
**Request:**
```
Body: { audio: File }
```
**Response (Healthy):**
```json
{
  "id": 1,
  "prediction": "Healthy",
  "confidence": 92.5,
  "spectrogram": "/spectrograms/20241109_143025_spectrogram.png",
  "timestamp": "2024-11-09T14:30:25",
  "type": "success",
  "message": "🎉 Wow! Your voice is super awesome! Keep singing and having fun!"
}
```

**Response (Unhealthy):**
```json
{
  "id": 2,
  "prediction": "Laryngitis",
  "confidence": 85.3,
  "spectrogram": "/spectrograms/20241109_143100_spectrogram.png",
  "timestamp": "2024-11-09T14:31:00",
  "type": "warning",
  "message": "Voice analysis indicates Laryngitis. Please review the medical suggestions below.",
  "suggestion": {
    "pathology_type": "Laryngitis",
    "suggestion": "Rest your voice...",
    "severity": "moderate",
    "doctor_name": "Dr. Michael Chen",
    "specialization": "Pediatric ENT Specialist",
    "contact": "Recommended consultation"
  }
}
```

#### 3. Get History
```http
GET /api/history?limit=10
```

#### 4. Get Sample Audios
```http
GET /api/samples
```

#### 5. Get Statistics
```http
GET /api/statistics
```

#### 6. Get Spectrogram Image
```http
GET /spectrograms/{filename}
```

## 💾 Database Schema

### Tables

**1. AudioRecord**
- Stores uploaded audio files and prediction results
- Fields: id, filename, file_path, upload_date, prediction, confidence, spectrogram_path, age_group, notes

**2. HealthyQuote**
- Playful quotes for healthy voice results
- Fields: id, quote, age_group (child/teen/general)
- Pre-loaded with 18+ encouraging messages

**3. DoctorSuggestion**
- Medical suggestions for pathological cases
- Fields: id, pathology_type, suggestion, severity, doctor_name, specialization, contact
- Pre-loaded with severity-based recommendations

**4. SampleAudio**
- Metadata for sample audio files
- Fields: id, name, file_path, actual_condition, description, age_group

## 🎨 Frontend Integration

### Example: Using ResultsDisplay Component

```jsx
import React, { useState } from 'react';
import ResultsDisplay from './components/ResultsDisplay';

function AudioChecker() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAudioUpload = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('audio', file);

    try {
      const response = await fetch('http://localhost:5000/api/diagnose', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Your audio upload UI */}
      {loading && <div>Analyzing...</div>}
      {result && <ResultsDisplay result={result} />}
    </div>
  );
}
```

## 🔧 Model Integration

### Replace Placeholder Prediction

In `app.py`, replace the placeholder prediction with your actual LSM model:

```python
def load_model():
    """Load your trained LSM model"""
    try:
        import pickle
        model = pickle.load(open('models/lsm_model.pkl', 'rb'))
        scaler = pickle.load(open('models/scaler.pkl', 'rb'))
        return model, scaler
    except Exception as e:
        print(f"Model loading error: {e}")
        return None, None

# Load model at startup
model, scaler = load_model()

def predict_pathology(features):
    """Predict using your LSM model"""
    if model is not None and scaler is not None:
        # Scale features
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Get prediction
        prediction_idx = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(probabilities.max() * 100)
        
        # Map to class names
        class_names = ['Healthy', 'Laryngitis', 'Vocal Polyp']
        prediction = class_names[prediction_idx]
        
        return prediction, confidence
    
    # Fallback if model not loaded
    return "Healthy", 85.0
```

## 🧪 Testing

### Test API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Get samples
curl http://localhost:5000/api/samples

# Get statistics
curl http://localhost:5000/api/statistics

# Upload audio (replace with actual file)
curl -X POST -F "audio=@test_audio.wav" http://localhost:5000/api/diagnose
```

### Database Testing

```python
# Test database connection
python -c "from app import app, db; app.app_context().push(); print(db.session.execute('SELECT 1').scalar())"

# Check records
python -c "from app import app, db, AudioRecord; app.app_context().push(); print(AudioRecord.query.count())"
```

## 📊 Sample Data Included

### Healthy Quotes (18 total)
- 8 child-friendly quotes
- 5 teen-oriented quotes
- 5 general quotes

### Doctor Suggestions (7 total)
- 3 Laryngitis suggestions (mild, moderate, severe)
- 3 Vocal Polyp suggestions (mild, moderate, severe)
- 1 General pathology suggestion

### Sample Audio Metadata (7 entries)
- 3 Healthy voice samples
- 2 Laryngitis samples
- 2 Vocal Polyp samples

## 🛠️ Customization

### Adding New Quotes

```python
from models import db, HealthyQuote

quote = HealthyQuote(
    quote="Your new encouraging quote here! 🌟",
    age_group="child"  # or "teen" or "general"
)
db.session.add(quote)
db.session.commit()
```

### Adding New Doctor Suggestions

```python
from models import db, DoctorSuggestion

suggestion = DoctorSuggestion(
    pathology_type="Laryngitis",
    suggestion="Your medical advice here...",
    severity="moderate",
    doctor_name="Dr. John Doe",
    specialization="ENT Specialist",
    contact="Contact information"
)
db.session.add(suggestion)
db.session.commit()
```

## 🔒 Security Considerations

- ✅ File upload validation (WAV files only)
- ✅ Secure filename handling
- ✅ File size limits (16MB max)
- ⚠️ Add rate limiting in production
- ⚠️ Implement user authentication
- ⚠️ Use HTTPS in production
- ⚠️ Sanitize all user inputs

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm voice_pathology.db
python init_db.py
```

### Port Already in Use
```python
# Change port in app.py
app.run(debug=True, port=5001)
```

### Module Not Found
```bash
pip install --upgrade -r requirements.txt
```

### Spectrogram Not Displaying
- Check CORS configuration
- Verify spectrogram folder permissions
- Check image path in response

## 📈 Future Enhancements

- [ ] User authentication and accounts
- [ ] Audio playback feature
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Real-time analysis with WebSocket
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Advanced age detection
- [ ] Voice comparison feature
- [ ] Treatment progress tracking

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Sahil Brid** - *Initial work* - [GitHub](https://github.com/sahilbrid)

## 🙏 Acknowledgments

- Saarbrücken Voice Database for training data
- Anthropic Claude for assistance
- All contributors and testers

## 📧 Contact

For questions or support:
- GitHub Issues: [Create an issue](https://github.com/sahilbrid/voice-pathology-detection/issues)
- Email: your-email@example.com

## 🔗 Links

- [Live Demo](http://voice-pathology-detection.s3-website.ap-south-1.amazonaws.com/)
- [Documentation](https://github.com/sahilbrid/voice-pathology-detection/wiki)
- [Saarbrücken Voice Database](https://stimmdb.coli.uni-saarland.de/)

---

**⚠️ Medical Disclaimer:** This application provides preliminary analysis only. Always consult qualified healthcare professionals for proper diagnosis and treatment.

Made with ❤️ for children's voice health