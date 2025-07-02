import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="attendance_db",
        user="admin",
        password="Kaushikjii@7",
        host="localhost",
        port="5432"
    )
