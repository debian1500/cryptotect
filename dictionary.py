import json
from pathlib import Path

ADDRESSBOOK_PATH = Path("addressbook.json")

try:
    with open(ADDRESSBOOK_PATH, "r", encoding="utf-8") as f:
        AdressBook: dict[str, dict] = json.load(f)
except FileNotFoundError:
    AdressBook = {}

def save_addressbook():
    with open(ADDRESSBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(AdressBook, f, indent=2, ensure_ascii=False)
