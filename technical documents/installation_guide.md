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
git clone https://github.com/yourusername/marta-transit-dashboard.git
cd marta-transit-dashboard
```

#### Option B: Download and Extract (if provided as ZIP archive)

```bash
# Extract the ZIP file
unzip marta-transit-dashboard.zip
cd marta-transit-dashboard
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

Create a configuration file by copying the example:

```bash
cp config/config.example.py config/config.py
```

Edit `config/config.py` to include your MARTA API key and any other custom settings. See the [Configuration Guide](configuration_guide.md) for details.

### 5. Create Required Directories

Ensure cache directories exist:

```bash
mkdir -p cache
```

### 6. Running the Application

Start the Flask development server:

```bash
python run.py
```

The application should now be running at [http://localhost:5000](http://localhost:5000).