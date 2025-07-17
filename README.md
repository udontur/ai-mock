# Mock Paper Generator
Developers: [@RailgunGLM](https://github.com/RailgunGLM), [@Animal-Migration](https://github.com/Animal-Migration), [@udontur](https://github.com/udontur)

## Development
### Initial Cloning
After cloning the repo, you need to create your own `.env` file that contains the Django secret key and OpenRouter API key. Contact turtle for the secret key. Sign up in OpenRouter for the OpenRouter API Key.

Python version **must be**: `Python 3.12`

### Getting Started
Run the following script. It creates a virtual environment and installs required packages. 
```
./assets/scripts/venv.sh
```

### Running it Locally
Open the Python virtual environment
```sh
source .venv/bin/activate
```
Start the development server
```bash
python3 manage.py runserver
```

Open `http://localhost:8000` in your browser.

### Documentation
Detailed documentation is available on [assets/docs](assets/docs)
