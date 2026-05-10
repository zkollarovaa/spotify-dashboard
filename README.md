# How to run this spotify dashboard

### 1. Create a virtual environment:

```bash
python -m venv .venv
```


### 2. Activate the environment

```bash
# On macOS / Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

---

### 3. After activation install requirements:

```bash
pip install -r requirements.txt
```

---

### 4. Run the app

```bash
python main.py
```

***

### Interactive Exploration: Brushing & Linking

#### How it Works in the Dashboard

*   **The Brush (Selection):** Users can use the **Lasso Tool** on the Master Scatter Plot (Chart 1) to "brush" over a cluster of interesting data points (e.g., songs with high TikTok views but low Spotify streams).
*   **The Link (Coordination):** The moment the selection is made, that exact cohort of songs is "linked" and highlighted simultaneously across Charts 2, 3, and 4.
*   **Context Preservation:** Unselected tracks are not deleted from the screen. Instead, they fade into a transparent grey (`opacity=0.05`). This instantly reveals where your selected niche sits compared to the macro-level industry trends.

***
