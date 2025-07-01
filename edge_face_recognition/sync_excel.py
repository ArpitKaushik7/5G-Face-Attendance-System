import gdown

def download_latest_excel():
    url = 'https://docs.google.com/spreadsheets/d/1Nv3cKZLBcBLH0JeLmRTJLOrgHWhIBOV94OyW-mjk0FY/export?format=xlsx'
    output_path = r"E:\5G Face Attendance System\form_responses.xlsx"
    gdown.download(url, output_path, quiet=False)
