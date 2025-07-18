## Environment Variables
After cloning the repo, you need to create your own `.env` file at the root of the directory.

This file should include:
1. A Django secret key 
2. LLM API credentials 

### 1. Django Secret Key
Contact turtle for the secret key.

Variable format
```
SECRET_KEY="<THE_KEY>"
```

### 2. LLM API Credentials
We are currently using the DeepSeek API. Contact turtle for the API key. 

Variable format:
```
LLM_API_KEY="<YOUR_KEY>
LLM_API_BASE="https://api.deepseek.com"
LLM_MODEL="deepseek-reasoner"
```

