import json

file_path = "C:/Telegram_project/TGDataset_4/file_105_from_thesneaker_kingz_to_tinder.json"

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Top-level keys in the file:")
for key in data:
    print(f"{key}: {type(data[key])}")
