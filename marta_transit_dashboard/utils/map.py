"""
Map utilities for the Simple MARTA App
"""

import os
import sys
import requests
import shutil
from PIL import Image
import io

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    MARTA_MAP_URL,
    MAP_BACKUP_URL,
    MAP_FILE_PATH,
    STATIC_DIR
)

def download_marta_map():
    """
    Download the MARTA train map and save it to the static directory
    
    Returns:
        bool: True if successful, False otherwise
    """
    os.makedirs(os.path.dirname(MAP_FILE_PATH), exist_ok=True)
    
    try:
        print("Downloading MARTA train map...")
        # First try to get the map from MARTA website
        response = requests.get(MARTA_MAP_URL, stream=True)
        
        if response.status_code == 200:
            with open(MAP_FILE_PATH, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            print("✅ MARTA train map downloaded successfully!")
            return True
        else:
            # If that fails, use a backup source
            print("Failed to download from primary source, trying backup...")
            response = requests.get(MAP_BACKUP_URL, stream=True)
            
            if response.status_code == 200:
                with open(MAP_FILE_PATH, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                print("✅ MARTA train map downloaded from backup source!")
                return True
            else:
                # If both fail, create a simple placeholder map
                return create_placeholder_map()
    except Exception as e:
        print(f"❌ Error downloading MARTA map: {e}")
        return create_placeholder_map()

def create_placeholder_map():
    """
    Create a simple placeholder map image if download fails
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print("Creating a placeholder MARTA map...")
        # Create a simple placeholder map
        width, height = 800, 600
        image = Image.new('RGB', (width, height), (240, 240, 240))
        
        # Save the placeholder image
        image.save(MAP_FILE_PATH)
        print("✅ Created placeholder map. You may want to replace it with the actual MARTA map.")
        return True
    except Exception as e:
        print(f"❌ Error creating placeholder map: {e}")
        # As an absolute fallback, create an empty file
        try:
            with open(MAP_FILE_PATH, "wb") as f:
                f.write(b"")
            print("⚠️ Created empty file for MARTA map. Please add a map image manually.")
            return False
        except:
            print("❌ Could not create map file. Please add a map image manually.")
            return False

def ensure_map_exists():
    """
    Ensure that the map file exists, downloading it if necessary
    
    Returns:
        bool: True if map exists, False otherwise
    """
    if os.path.exists(MAP_FILE_PATH):
        size = os.path.getsize(MAP_FILE_PATH)
        if size > 0:
            return True
    
    # If map doesn't exist or is empty, download it
    return download_marta_map() 