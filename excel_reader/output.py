import pandas as pd
import os
from pathlib import Path

def save_to_excel(data: list[dict], file_path: str):
    """
    Save the data to an Excel file.
    """
    if not data:
        raise ValueError("No data to save")
    
    output_dir = str(Path.home() / "Downloads")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, file_path)
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, engine="openpyxl")

    print(f"Saved to {file_path}")
