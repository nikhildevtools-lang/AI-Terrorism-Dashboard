import os
import gdown

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "globalterrorismdb_0718dist.csv")

# Replace this with YOUR Google Drive file ID
FILE_ID = "1ToH3ttJZFC1ljtg6AQ9BDF0hKiJooV7d"

URL = f"https://drive.google.com/uc?id={FILE_ID}"


def ensure_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(DATA_FILE):
        print("Dataset already exists.")
        return DATA_FILE

    print("Downloading dataset...")

    gdown.download(
        URL,
        DATA_FILE,
        quiet=False,
        fuzzy=True
    )

    print("Dataset downloaded.")

    return DATA_FILE