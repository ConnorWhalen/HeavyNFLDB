# HeavyNFLDB
HeavyNFLD Database

## Installation

Install dependencies in your virtual environment:
```bash
pip install -r requirements.txt
```

## Run

For server v1 (flask + SQLAlchemy):
```bash
flask --app app.py run --debug --port 5000
```

For server v2, site is client-only. Run this script to compile json indexes from db:
```bash
python buildv2.py
```

To run server v2 locally:
```bash
flask --app appv2.py run --debug --port 5000
```
