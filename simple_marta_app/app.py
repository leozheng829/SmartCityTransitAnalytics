"""
Main application module for the Simple MARTA App
"""

import os
import sys
from flask import Flask
import urllib.request

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import application components
from config.config import (
    DEBUG, 
    PORT, 
    HOST, 
    TEMPLATES_AUTO_RELOAD,
    STATIC_DIR,
    TEMPLATES_DIR,
)
from api.routes import api_bp
from routes import web_bp
from utils.map import ensure_map_exists

def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__, 
                static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)
    
    # Configure app
    app.config['TEMPLATES_AUTO_RELOAD'] = TEMPLATES_AUTO_RELOAD
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    # Ensure static and template directories exist
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    # Create HTML template if it doesn't exist
    template_path = os.path.join(TEMPLATES_DIR, 'index.html')
    if not os.path.exists(template_path):
        from utils.templates import create_index_template
        create_index_template()
    
    # Create CSS file if it doesn't exist
    css_path = os.path.join(STATIC_DIR, 'style.css')
    if not os.path.exists(css_path):
        from utils.templates import create_css_template
        create_css_template()
    
    return app

def run_app():
    """
    Run the Flask application
    """
    # Ensure the map image exists
    ensure_map_exists()
    
    # Create and run the app
    app = create_app()
    print(f"Starting the Simple MARTA Transit App on http://{HOST}:{PORT}")
    app.run(debug=DEBUG, port=PORT, host=HOST)

if __name__ == '__main__':
    run_app() 