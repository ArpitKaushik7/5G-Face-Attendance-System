import psycopg2
from datetime import datetime

name_to_id = {
    "Arpit Kaushik": 58901,
    "Jane Doe": 58902
}

name_to_branch = {
    "Arpit Kaushik": "CSE",
    "Jane Doe": "ECE"
}

name_to_batch = {
    "Arpit Kaushik": "2025",
    "Jane Doe": "2024"
}

def log_attendance(name, subject, lecture_slot):
    try:
        student_id = name_to_id.get(name)
        branch = name_to_branch.get(name, "Unknown")
        batch = name_to_batch.get(name, "Unknown")
        now = datetime.now()
        date = now.date()
        time = now.time()

        if not student_id:
            print(f"[WARN] ID not found for {name}")
            return

        conn = psycopg2.connect(
            dbname="attendance_db",
            user="postgres",
            password="your_password",  # change this if needed
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Check for existing entry
        cursor.execute("""
            SELECT 1 FROM attendance_logs
            WHERE id = %s AND date = %s AND subject = %s AND lecture_slot = %s
        """, (student_id, date, subject, lecture_slot))
        
        if cursor.fetchone():
            print(f"[INFO] Attendance already logged for {name} ({subject}, {lecture_slot})")
        else:
            cursor.execute("""
                INSERT INTO attendance_logs (id, date, time, name, branch, batch, subject, lecture_slot)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (student_id, date, time, name, branch, batch, subject, lecture_slot))
            conn.commit()
            print(f"[DB] Logged attendance for {name} ({subject}, {lecture_slot})")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to log attendance: {e}")
