## venv
Initiate the virtual environment
```
./script/venv.sh
```
Start the virtual environment
```
source .venv/bin/activate
```
If you are using NixOS, run this in the venv
```
fix-python --venv .venv
```

## Installation
```
pip install -r requirements.txt
```

## Django
Run the development server
```
python3 manage.py runserver
```

