import sqlite3

def get_db_connection():
    # سيقوم بإنشاء ملف excora.db تلقائياً
    conn = sqlite3.connect('excora.db')
    conn.row_factory = sqlite3.Row
    return conn

# إنشاء الجداول الأساسية عند التشغيل الأول
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, username TEXT, expiry_date TEXT)''')
    conn.commit()
    conn.close()
