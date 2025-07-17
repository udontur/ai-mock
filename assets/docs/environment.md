## Environment Variables
After cloning the repo, you need to create your own `.env` file at the root of the directory.

This file should include:
1. A Django secret key 
2. OpenRouter API credentials 

### 1. Django Secret Key
Contact turtle for the secret key.

Variable format
```
SECRET_KEY="<THE_KEY>"
```

### 2. OpenRouter API Credentials
Signed up in [OpenRouter](https://openrouter.ai). After signing up, they will prompt you the API key. Make sure to save the API key!

Variable format:
```
OPENROUTER_API_KEY="<YOUR_KEY>"
OPENROUTER_API_BASE="https://openrouter.ai/api/v1"
OPENROUTER_MODEL_NAME="deepseek/deepseek-r1-0528:free"
```

