from pathlib import Path
import pandas as pd

# Get the absolute path to the CSV
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up from src/ to project root
DATA_PATH = BASE_DIR / "data" / "most-streamed-spotify-songs-2024.csv"

# Load the CSV
df = pd.read_csv(DATA_PATH, encoding="latin-1")

# === BASIC OVERVIEW ===
print("\n=== BASIC INFO ===")
print("Shape of dataset:", df.shape)

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

# === DATA TYPES & NON-NULL COUNTS ===
print("\n=== DATA TYPES & NON-NULL COUNTS ===")
print(df.info())

# === MISSING VALUES ===
print("\n=== MISSING VALUES (COUNT + %) ===")
missing_df = pd.DataFrame({
    "Missing Count": df.isnull().sum(),
    "Missing %": (df.isnull().sum() / len(df)) * 100
}).sort_values(by="Missing %", ascending=False)
print(missing_df)

# === COLUMN-BY-COLUMN ANALYSIS ===
print("\n=== COLUMN-BY-COLUMN ANALYSIS ===")
for col in df.columns:
    print(f"\n--- Column: {col} ---")
    print("Data type:", df[col].dtype)
    print("Unique values:", df[col].nunique())
    print("Sample values:", df[col].dropna().unique()[:5])
    print("Missing values:", df[col].isnull().sum())
    break  # Remove this break to analyze all columns

# === NUMERICAL & CATEGORICAL SUMMARY ===
print("\n=== NUMERICAL SUMMARY ===")
print(df.describe())

print("\n=== CATEGORICAL SUMMARY ===")
print(df.describe(include=["object"]))

print("\n=== DUPLICATES ===")
print("Number of duplicate rows:", df.duplicated().sum())
