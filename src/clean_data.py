
from pathlib import Path
import pandas as pd

# Get the absolute path to the CSV
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up from src/ to project root
DATA_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024.csv"

# Load the CSV
df = pd.read_csv(DATA_PATH, encoding="latin-1")


print("Data loaded successfully! Number of rows:", len(df))
print(df.head())