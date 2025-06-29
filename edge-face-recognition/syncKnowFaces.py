import pandas as pd
import os
import requests

# === CONFIGURATION ===
GDRIVE_EXPORT_LINK = "https://docs.google.com/spreadsheets/d/1Nv3cKZLBcBLH0JeLmRTJLOrgHWhIBOV94OyW-mjk0FY/export?format=xlsx"
EXCEL_PATH = r"E:\5G Face Attendance System\form_responses.xlsx"
KNOWN_DIR = r"E:\5G Face Attendance System\known faces"

def download_latest_excel():
    """Download latest Excel from Google Sheets"""
    print("[SYNC] Downloading latest form responses...")
    response = requests.get(GDRIVE_EXPORT_LINK)
    if response.status_code == 200:
        with open(EXCEL_PATH, "wb") as f:
            f.write(response.content)
        print("[SYNC] Excel downloaded.")
    else:
        print("[ERROR] Could not download Excel.")

def extract_drive_id(url):
    """Extract file ID from Google Drive share link"""
    if "id=" in url:
        return url.split("id=")[-1].split("&")[0]
    elif "/d/" in url:
        return url.split("/d/")[1].split("/")[0]
    return None

def download_image(file_id, save_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"[IMG] Saved: {save_path}")
    else:
        print(f"[ERROR] Failed to download image: {save_path}")

def sync_known_faces():
    if not os.path.exists(KNOWN_DIR):
        os.makedirs(KNOWN_DIR)

    download_latest_excel()
    df = pd.read_excel(EXCEL_PATH)

    for _, row in df.iterrows():
        try:
            raw_name = str(row["Photo (name it as ID_Firstname Surname)"]).strip()
            file_id = extract_drive_id(raw_name)
            filename = raw_name.split('/')[-1] if '/' in raw_name else raw_name
            filename = filename.replace(" ", "_").replace(".jpg", "") + ".jpg"
            save_path = os.path.join(KNOWN_DIR, filename)

            if not os.path.exists(save_path) and file_id:
                download_image(file_id, save_path)
        except Exception as e:
            print(f"[WARN] Failed to sync image: {e}")

if __name__ == "__main__":
    sync_known_faces()
