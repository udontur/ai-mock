# Mock Paper Generator
Developers: [@RailgunGLM](https://github.com/RailgunGLM), [@Animal-Migration](https://github.com/Animal-Migration), [@udontur](https://github.com/udontur)

## Development
### Initial Cloning
After cloning the repo, you need to create your own `.env` file that contains the Django secret key. Contact turtle for the secret key. 

Python version *must be*: `Python 3.12`

### Install packages
Create and start a virtual environment
```
./assets/scripts/venv.sh
source .venv/bin/activate
```
Install the required packages
```sh
pip install -r requirements.txt
```

### Running it Locally
Start the development server
```bash
python3 manage.py runserver
```

Open `http://localhost:8000` in your browser.

### Documentation
Detailed documentation is available on [assets/docs](assets/docs)
