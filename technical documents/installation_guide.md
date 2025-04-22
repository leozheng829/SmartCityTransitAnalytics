# MARTA Transit Dashboard - Installation Guide

## System Requirements

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection for API access
- Git (optional, for cloning the repository)

## Installation Steps

### 1. Obtain the Source Code

#### Option A: Clone from Git (if using version control)

```bash
git clone https://github.com/leozheng829/SmartCityTransitAnalytics.git
cd marta-transit-dashboard
```

#### Option B: Download and Extract (if provided as ZIP archive)

```bash
# Extract the ZIP file
unzip marta-transit-dashboard.zip
cd marta_transit_dashboard
```

### 2. Set Up a Virtual Environment (Recommended)

Creating a virtual environment keeps the application dependencies isolated from other Python projects.

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Configuration

Verify the settings in `config/config.py`. You may need to add your MARTA Train API key if it's not already present. See the [Configuration Guide](configuration_guide.md) for details on all settings.

### 5. Running the Application

Start the Flask development server:

```bash
python run.py
```

The application should now be running, typically at [http://localhost:5001](http://localhost:5001) (check the terminal output or `config/config.py` for the exact address).