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

### 4. Create your .env file

a. Rename .env.example file as .env
b. Replace "your-api-key-here with" by your API key
c. Replace "your-lucca-account-name" by your Lucca account name
d. Replace "your-sandbox-name" by your sandbox name

```bash
API_KEY="lucca application={your-api-key-here}"
ACCOUNT="your-lucca-account-name"
SANDBOX_NAME="your-sandbox-name"
```

### 5. Launch the script

```bash 
python3 script.py 
```



