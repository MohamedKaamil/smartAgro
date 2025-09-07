from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config.config import config
import os

db = SQLAlchemy()

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
         supports_credentials=True)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.locations import locations_bp
    from app.routes.seller import seller_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(seller_bp, url_prefix='/api/seller')
    app.register_blueprint(main_bp, url_prefix='/api')
    
    # Import buyer test blueprint for debugging
    try:
        from app.routes.buyer_test import buyer_test_bp
        app.register_blueprint(buyer_test_bp, url_prefix='/api/buyer')
        print("SUCCESS: Buyer test blueprint registered successfully")
    except Exception as e:
        print(f"ERROR: Error registering buyer test blueprint: {e}")
        import traceback
        traceback.print_exc()
        
    # Import buyer blueprint separately with error handling
    try:
        from app.routes.buyer import buyer_bp
        app.register_blueprint(buyer_bp, url_prefix='/api/buyer-full')
        print("SUCCESS: Buyer full blueprint registered successfully")
    except Exception as e:
        print(f"ERROR: Error registering buyer full blueprint: {e}")
        import traceback
        traceback.print_exc()
        
    # Import test blueprint for debugging
    try:
        from app.routes.main_test import main_test_bp
        app.register_blueprint(main_test_bp, url_prefix='/api/test')
        print("SUCCESS: Test blueprint registered successfully")
    except Exception as e:
        print(f"ERROR: Error registering test blueprint: {e}")
        import traceback
        traceback.print_exc()
    
    # Create database tables
    with app.app_context():
        from app.utils.database import init_database
        init_database()
    
    return app