import gdown
import pandas as pd

EXCEL_URL = 'https://docs.google.com/spreadsheets/d/1Nv3cKZLBcBLH0JeLmRTJLOrgHWhIBOV94OyW-mjk0FY/export?format=xlsx'
EXCEL_PATH = r"E:\5G Face Attendance System\form_responses.xlsx"

def download_latest_excel():
    gdown.download(EXCEL_URL, EXCEL_PATH, quiet=False)

def load_excel():
    return pd.read_excel(EXCEL_PATH)

def get_student_details(student_id, df):
    try:
        student_id = int(student_id)
        row = df[df["Id"] == student_id]
        if not row.empty:
            return row.iloc[0]["Name"], row.iloc[0]["Branch"], row.iloc[0]["Batch"]
    except:
        pass
    return "Unknown", "Unknown", "Unknown"

# Example usage
if __name__ == "__main__":
    download_latest_excel()
    df = load_excel()
    print(get_student_details("58901", df))
