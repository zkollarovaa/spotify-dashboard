import pandas as pd
import re
from pathlib import Path

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024.csv"
OUTPUT_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024-clean.csv"
fix_names = {
    "Beyoncï¿": "Beyoncé",
    "Patati Patatï¿": "Patati Patatá",
    "Thullio Milionï¿½ï¿": "Thullio Milionário",
    "cassï¿": "cassö",
    "nadie sabe lo que va a pasar maï¿½ï¿": "nadie sabe lo que va a pasar mañana",
    "I Ainï¿½ï¿½ï¿½t Worried": "I Ain't Worried",
    "Dianï¿": "Diané",
    "ROSALï¿": "ROSALÍA",
    "Tiï¿½ï¿": "Tiësto",
    "Eden Muï¿½ï": "Eden Muñoz",
    "Polimï¿½ï¿½ Westc": "Polimá WestCoast",
    "Marï¿½ï¿½lia Mendo": "Marília Mendonça",
    "Mï¿½ï¿½ne": "Måneskin",
    "Fousheï¿": "Fousheé",
    "Kï¿½ï¿½ï¿½": "Käärijä",
    "Emir Can ï¿½ï¿": "Emir Can İğrek",
    "Gruppo Menos ï¿½ï¿": "Grupo Menos é Mais",
    "Maria Marï¿½ï": "Maria Marçal",
    "Chayï¿½ï¿½n R": "Chayanne"
}

# Define a function to fix the "mojibake" (corrupted characters)
def fix_mojibake(text):
    if not isinstance(text, str):
        return text
    # This specifically reverses the common "Excel-saving-UTF8-as-Latin1" corruption
    # We encode to latin-1 to get bytes, then decode as utf-8.
    try:
        return text.encode('latin-1').decode('utf-8')
    except:
        return text
    

def clean_text_data(text):
    """General text normalization and corruption detection."""
    if not isinstance(text, str):
        return text
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Check for heavy corruption (lots of question marks)
    if text.count('?') > 5 or "ý" in text:
        return "Unknown"
        
    return text

def drop_unfixable_data(df):
    # If the track name or artist is still "Unknown" or contains encoding errors, 
    # and we have enough other data, just drop these rows.
    # Count how many corrupted characters exist per row
    df = df[df['artist'] != "Unknown"] 
    df = df[~df['track'].str.contains(r'[\?ï¿½]', na=False)]
    return df


def process_spotify_data():
    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv(DATA_PATH, encoding="latin-1")

    # 2. Drop unused columns
    drop_cols = [
        "TIDAL Popularity", "Soundcloud Streams", "SiriusXM Spins",
        "Pandora Track Stations", "Pandora Streams", "Amazon Playlist Count"
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    # 3. Clean Text Columns
    text_cols = ["Track", "Album Name", "Artist"]
    # This regex looks for the specific patterns that indicate corruption
    corruption_pattern = r'[\uFFFD]|Ã¯|Â¿|Â½'

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(fix_mojibake)
            df[col] = df[col].apply(clean_text_data)
            df[col] = df[col].replace(r'.*\?{3,}.*', "Unknown", regex=True)
            # Drop rows where the text matches the corruption pattern
            df = df[~df[col].astype(str).str.contains(corruption_pattern, na=False)]    
            # Map the corrupted strings to the corrected ones
            df[col] = df[col].replace(fix_names)


    # 4. Standardize Column Names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # 5. Convert Data Types
    # Convert Dates
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Convert Numerics (automatically handles commas)
    exclude_cols = ["track", "album_name", "artist", "release_date", "isrc"]
    for col in df.columns:
        if col not in exclude_cols:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
            # Fill missing numeric values with median
            df[col] = df[col].fillna(df[col].median())

    # 6. Final Deduplication
    df = df.drop_duplicates()
    
    # Fill remaining text NaNs
    df["artist"] = df["artist"].fillna("Unknown")

    # drop rows that are still unfixable
    df = drop_unfixable_data(df)
    print(f"Final shape after cleaning: {df.shape}")

    # 7. Save
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"Success! Cleaned data saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    process_spotify_data()