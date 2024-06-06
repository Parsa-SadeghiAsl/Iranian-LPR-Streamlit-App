
#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make webapp.sh executable
chmod +x webapp.sh

# Deactivate the virtual environment
deactivate

# Print setup completion message
echo "Setup is completed.Now you can run webapp with ./webapp.sh"



































