## Virtual Environment (venv)
Initiate the virtual environment
```
python3 -m venv .venv
```
Start the virtual environment
```
source .venv/bin/activate
```

## Installation
Install the required packages
```
pip install -r requirements.txt
```
If you are using NixOS, run this in the venv
```
fix-python --venv .venv --libs assets/nix/libs.nix
```

## Development server
Run the development server
```
python3 manage.py runserver
```

