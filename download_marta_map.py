import os
import requests
import shutil
from PIL import Image
import io

def download_marta_map():
    """Download the MARTA train map and save it to the static directory"""
    os.makedirs('static', exist_ok=True)
    
    try:
        print("Downloading MARTA train map...")
        # First try to get the map from MARTA website
        response = requests.get("https://www.itsmarta.com/images/train-stations-map.jpg", stream=True)
        
        if response.status_code == 200:
            with open("static/marta_train_map.jpg", 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            print("✅ MARTA train map downloaded successfully!")
        else:
            # If that fails, use a backup source
            print("Failed to download from primary source, trying backup...")
            backup_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/MARTA_Rail_Map.svg/1200px-MARTA_Rail_Map.svg.png"
            response = requests.get(backup_url, stream=True)
            
            if response.status_code == 200:
                with open("static/marta_train_map.jpg", 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                print("✅ MARTA train map downloaded from backup source!")
            else:
                # If both fail, create a simple placeholder map
                create_placeholder_map()
    except Exception as e:
        print(f"❌ Error downloading MARTA map: {e}")
        create_placeholder_map()

def create_placeholder_map():
    """Create a simple placeholder map image if download fails"""
    try:
        print("Creating a placeholder MARTA map...")
        # Create a simple placeholder map
        width, height = 800, 600
        image = Image.new('RGB', (width, height), (240, 240, 240))
        
        # Save the placeholder image
        image.save("static/marta_train_map.jpg")
        print("✅ Created placeholder map. You may want to replace it with the actual MARTA map.")
    except Exception as e:
        print(f"❌ Error creating placeholder map: {e}")
        # As an absolute fallback, create an empty file
        with open("static/marta_train_map.jpg", "wb") as f:
            f.write(b"")
        print("⚠️ Created empty file for MARTA map. Please add a map image manually.")

if __name__ == "__main__":
    download_marta_map()
    
    # Check if file exists
    if os.path.exists("static/marta_train_map.jpg"):
        size = os.path.getsize("static/marta_train_map.jpg")
        print(f"Map file size: {size/1024:.2f} KB")
        
        if size > 0:
            print("Map file is ready to use!")
        else:
            print("⚠️ Warning: Map file is empty. Please add a map image manually.")
    else:
        print("❌ Map file was not created. Please add a map image manually to static/marta_train_map.jpg") 