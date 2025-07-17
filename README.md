# Mock Paper Generator
Developers: [@RailgunGLM](https://github.com/RailgunGLM), [@Animal-Migration](https://github.com/Animal-Migration), [@udontur](https://github.com/udontur)

## Development
> [!NOTE]
> Python version **must be**: `Python 3.12`
### Initial Cloning
After cloning the repo, you need to create your own `.env` file that contains:
1. A Django secret key (Contact turtle for the secret key)
2. LLM API credentials (Contact turtle to create your API key) 

More information available in the [documentation](assets/docs/environment.md)

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
Detailed documentation is available in [assets/docs](assets/docs)
