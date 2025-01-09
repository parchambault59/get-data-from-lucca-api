### 1. Clone repository

```bash
git clone https://github.com/parchambault59/get-data-from-lucca-api.git
cd get-data-from-lucca-api
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
Might take up to 30 seconds to run.

### 4. Create your .env file

1. Rename .env.example file as .env -> you now have your .env file
2. Replace "your-api-key-here with" by your API key
3. Replace "your-lucca-account-name" by your Lucca account name
4. Replace "your-sandbox-name" by your sandbox name
5. Save the file

```bash
API_KEY="lucca application={your-api-key-here}"
ACCOUNT="your-lucca-account-name"
SANDBOX_NAME="your-sandbox-name"
```

### 5. Run the script

```bash 
python3 script.py 
```
Might take up to a minute to run the first time.


