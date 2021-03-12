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

**File: api_key.py**
```bash
echo "API_KEY = 'YOUR_BOT_API_KEY'
CHANNEL_ID = 'CHAT_ID_OF_GROUP'" > secrets.py
```
A file ```secrets.py``` is missing as it contains a token to access the HTTP API of [Ada](t.me/AdaLovelance_bot) and Chat_id of [this](t.me/awscclpu) Group. The file is structured in this way: 
```python
API_KEY = 'YOUR_BOT_API_KEY'
CHANNEL_ID = 'CHAT_ID_OF_GROUP'
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