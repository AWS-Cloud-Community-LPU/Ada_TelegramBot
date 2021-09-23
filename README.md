# Ada_TelegramBot
Ada - A telegram bot for AWS Cloud Community Telegram Group. Hosted on AWS EC2.

## :zap: Installation
**1. Clone this repo by running either of the below commands.**

    https : `git clone https://github.com/AWS-Cloud-Community-LPU/Ada_TelegramBot.git`
  
    ssh : `git@github.com:AWS-Cloud-Community-LPU/Ada_TelegramBot.git`

**2. Now, run the following commands:**

```bash
cd Ada_TelegramBot
pip install -r requirements.txt
```
This will install all the project dependencies.

**3. Configure Missing Files:**

**File: secrets.ini**
```bash
echo "[KEYS]\nAPI_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" > secrets.ini
```
A file ```secrets.ini``` is missing as it contains a token to access the HTTP API of [Ada](t.me/AdaLovelance_bot). The file is structured in this way: 
```python
[KEYS]
API_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

**File: titles.txt**
```bash
touch titles.txt
```
A file ```titles.txt``` contains all titles of brodcasted news so that duplicate news cannot be sended.

**4. :tada: Run the bot:**
```bash
python3 main.py
```

## :page_facing_up: License
[MIT](./LICENSE) © AWS Cloud Community LPU