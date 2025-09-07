#!/usr/bin/env python3
"""
Main entry point for the Crop Recommendation API
"""
import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print("="*60)
    print("CROP RECOMMENDATION API")
    print("="*60)
    print(f"Starting server on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Database: MySQL")
    print("="*60)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )