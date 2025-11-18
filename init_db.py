import os
from flask import Flask
from models import db, HealthyQuote, DoctorSuggestion, SampleAudio, AudioRecord

def init_database(app):
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if HealthyQuote.query.first() is None:
            populate_healthy_quotes()
        
        if DoctorSuggestion.query.first() is None:
            populate_doctor_suggestions()
        
        if SampleAudio.query.first() is None:
            populate_sample_audios()
        
        print("Database initialized successfully!")


def populate_healthy_quotes():
    """Add playful quotes for healthy voices"""
    quotes = [
        # Child-friendly quotes
        {"quote": "🎉 Wow! Your voice is super awesome! Keep singing and having fun!", "age_group": "child"},
        {"quote": "⭐ Amazing! Your voice is as healthy as a superhero's! You're doing great!", "age_group": "child"},
        {"quote": "🌈 Fantastic! Your voice is bright and beautiful! Keep being awesome!", "age_group": "child"},
        {"quote": "🦸 Your voice is super strong! You sound like a champion! Keep it up!", "age_group": "child"},
        {"quote": "🎵 Hooray! Your voice is perfect for singing your favorite songs!", "age_group": "child"},
        {"quote": "🌟 Yay! Your voice is healthy and happy! Keep talking and laughing!", "age_group": "child"},
        {"quote": "🚀 Your voice is out of this world! You're a star!", "age_group": "child"},
        {"quote": "🎈 Brilliant! Your voice sounds wonderful! Keep being you!", "age_group": "child"},
        
        # Teen quotes
        {"quote": "💪 Your voice is in great shape! Keep rocking those conversations!", "age_group": "teen"},
        {"quote": "🎤 Awesome! Your voice is healthy and strong! You're crushing it!", "age_group": "teen"},
        {"quote": "✨ Perfect! Your vocal health is on point! Keep being amazing!", "age_group": "teen"},
        {"quote": "🔥 Your voice is fire! Healthy and confident! Keep it up!", "age_group": "teen"},
        {"quote": "🎸 Rock on! Your voice is in excellent condition! You got this!", "age_group": "teen"},
        
        # General quotes
        {"quote": "🌟 Excellent! Your voice is healthy and vibrant! Keep taking care of it!", "age_group": "general"},
        {"quote": "👍 Great news! Your vocal health is excellent! Continue the good work!", "age_group": "general"},
        {"quote": "😊 Wonderful! Your voice is in perfect condition! Stay healthy!", "age_group": "general"},
        {"quote": "💚 Your voice is healthy! Keep hydrated and keep singing!", "age_group": "general"},
    ]
    
    for quote_data in quotes:
        quote = HealthyQuote(**quote_data)
        db.session.add(quote)
    
    db.session.commit()
    print(f"Added {len(quotes)} healthy quotes")


def populate_doctor_suggestions():
    """Add doctor suggestions for unhealthy voices"""
    suggestions = [
        # Laryngitis suggestions
        {
            "pathology_type": "Laryngitis",
            "suggestion": "Rest your voice as much as possible. Avoid whispering as it strains vocal cords more than normal speech. Drink plenty of warm water and use a humidifier. If symptoms persist for more than 2 weeks, please consult an ENT specialist.",
            "severity": "mild",
            "doctor_name": "Dr. Sarah Johnson",
            "specialization": "Otolaryngologist (ENT)",
            "contact": "Schedule consultation with ENT department"
        },
        {
            "pathology_type": "Laryngitis",
            "suggestion": "Your voice shows signs of inflammation. Important steps: 1) Complete voice rest for 48-72 hours, 2) Stay hydrated with warm fluids, 3) Avoid irritants like smoke, 4) Use throat lozenges. Seek immediate medical attention if breathing becomes difficult.",
            "severity": "moderate",
            "doctor_name": "Dr. Michael Chen",
            "specialization": "Pediatric ENT Specialist",
            "contact": "Recommended for children - Pediatric ENT consultation"
        },
        {
            "pathology_type": "Laryngitis",
            "suggestion": "Immediate medical consultation recommended. Your laryngitis appears significant. Please see an ENT specialist within 24-48 hours. Meanwhile: complete voice rest, steam inhalation, avoid cold drinks, and take prescribed anti-inflammatory medication under medical supervision.",
            "severity": "severe",
            "doctor_name": "Dr. Emily Rodriguez",
            "specialization": "Voice Pathologist & ENT Surgeon",
            "contact": "Emergency ENT consultation required"
        },
        
        # Vocal Polyp suggestions
        {
            "pathology_type": "Vocal Polyp",
            "suggestion": "Voice evaluation detected potential vocal polyp. Please schedule an appointment with an ENT specialist for laryngoscopy examination. Treatment may include voice therapy or surgical removal. Avoid voice strain, shouting, and smoking.",
            "severity": "mild",
            "doctor_name": "Dr. James Wilson",
            "specialization": "Voice & Laryngeal Surgeon",
            "contact": "ENT consultation with videostroboscopy"
        },
        {
            "pathology_type": "Vocal Polyp",
            "suggestion": "Your voice shows characteristics consistent with vocal polyps. Important: 1) Schedule ENT consultation immediately, 2) Consider voice therapy with speech-language pathologist, 3) Avoid vocal abuse (shouting, singing loudly), 4) No smoking or irritant exposure. Early intervention is key!",
            "severity": "moderate",
            "doctor_name": "Dr. Lisa Anderson",
            "specialization": "Laryngologist & Voice Specialist",
            "contact": "Urgent voice clinic appointment needed"
        },
        {
            "pathology_type": "Vocal Polyp",
            "suggestion": "Significant vocal polyp indicators detected. URGENT: See ENT specialist within 1-2 days. You may require: 1) Detailed laryngoscopic examination, 2) Voice therapy program, 3) Possible microsurgical intervention, 4) Complete voice rest until medical evaluation. Do not delay consultation!",
            "severity": "severe",
            "doctor_name": "Dr. Robert Martinez",
            "specialization": "Phonosurgeon & Laryngologist",
            "contact": "Priority ENT appointment - Contact immediately"
        },
        
        # General pathology suggestions (for binary classification)
        {
            "pathology_type": "General Pathology",
            "suggestion": "Your voice analysis suggests some vocal irregularities. We recommend consulting with an ENT specialist or speech-language pathologist for a comprehensive evaluation. Early detection and treatment lead to better outcomes.",
            "severity": "mild",
            "doctor_name": "Dr. Amanda Foster",
            "specialization": "Speech-Language Pathologist",
            "contact": "Voice clinic consultation recommended"
        },
        {
            "pathology_type": "General Pathology",
            "suggestion": "Voice analysis indicates potential voice disorder. Important steps: 1) Schedule ENT consultation within 1-2 weeks, 2) Rest your voice when possible, 3) Stay hydrated, 4) Avoid shouting or straining. A specialist can provide accurate diagnosis and treatment plan.",
            "severity": "moderate",
            "doctor_name": "Dr. Robert Chen",
            "specialization": "Otolaryngologist (ENT)",
            "contact": "ENT consultation recommended within 1-2 weeks"
        },
        {
            "pathology_type": "General Pathology",
            "suggestion": "URGENT: Voice analysis shows significant abnormalities. Please see an ENT specialist within 24-48 hours for proper examination and diagnosis. Meanwhile: complete voice rest, avoid whispering, stay hydrated with warm fluids. Do not delay consultation.",
            "severity": "severe",
            "doctor_name": "Dr. Patricia Williams",
            "specialization": "Laryngologist & Voice Specialist",
            "contact": "URGENT - Schedule ENT appointment immediately"
        }
    ]
    
    for suggestion_data in suggestions:
        suggestion = DoctorSuggestion(**suggestion_data)
        db.session.add(suggestion)
    
    db.session.commit()
    print(f"Added {len(suggestions)} doctor suggestions")


def populate_sample_audios():
    """Add sample audio metadata (actual audio files need to be placed in samples/ folder)"""
    samples = [
        {
            "name": "Healthy Child Voice Sample 1",
            "file_path": "samples/healthy_child_1.wav",
            "actual_condition": "Healthy",
            "description": "Normal healthy child voice recording",
            "age_group": "child"
        },
        {
            "name": "Healthy Child Voice Sample 2",
            "file_path": "samples/healthy_child_2.wav",
            "actual_condition": "Healthy",
            "description": "Normal healthy child voice recording",
            "age_group": "child"
        },
        {
            "name": "Healthy Adult Voice Sample",
            "file_path": "samples/healthy_adult_1.wav",
            "actual_condition": "Healthy",
            "description": "Normal healthy adult voice recording",
            "age_group": "adult"
        },
        {
            "name": "Laryngitis Sample 1",
            "file_path": "samples/laryngitis_1.wav",
            "actual_condition": "Laryngitis",
            "description": "Voice recording with laryngitis symptoms",
            "age_group": "adult"
        },
        {
            "name": "Laryngitis Child Sample",
            "file_path": "samples/laryngitis_child_1.wav",
            "actual_condition": "Laryngitis",
            "description": "Child voice recording with laryngitis",
            "age_group": "child"
        },
        {
            "name": "Vocal Polyp Sample 1",
            "file_path": "samples/vocal_polyp_1.wav",
            "actual_condition": "Vocal Polyp",
            "description": "Voice recording with vocal polyp",
            "age_group": "adult"
        },
        {
            "name": "Vocal Polyp Sample 2",
            "file_path": "samples/vocal_polyp_2.wav",
            "actual_condition": "Vocal Polyp",
            "description": "Voice recording showing vocal polyp characteristics",
            "age_group": "adult"
        }
    ]
    
    for sample_data in samples:
        sample = SampleAudio(**sample_data)
        db.session.add(sample)
    
    db.session.commit()
    print(f"Added {len(samples)} sample audio records")


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_pathology.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    init_database(app)