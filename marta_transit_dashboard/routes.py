"""
Web routes for the Simple MARTA App
"""

from flask import Blueprint, render_template
import os

# Create a Blueprint for web routes
web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    """
    Render the main application page
    
    Returns:
        str: Rendered HTML template
    """
    return render_template('index.html') 