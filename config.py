import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Folders
    UPLOAD_FOLDER = 'uploads'
    SPECTROGRAM_FOLDER = 'spectrograms'
    SAMPLE_FOLDER = 'samples'
    MODEL_FOLDER = 'models'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}
    
    # Audio processing settings
    SAMPLE_RATE = 22050
    N_MELS = 128
    N_MFCC = 13
    
    # Model settings
    MODEL_PATH = 'models/lsm_model.pkl'
    SCALER_PATH = 'models/scaler.pkl'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///voice_pathology.db'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use stronger secret key in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_voice_pathology.db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}