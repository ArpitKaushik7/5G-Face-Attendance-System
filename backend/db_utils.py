import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname = "db_5g_fas",
        user = "admin",
        password = "user@5glab",
        host = "localhost",
        port = "5432"
    )
