import sqlite3

# SQLite 데이터베이스 연결 함수
def create_connection():
    conn = sqlite3.connect('comments.db')
    return conn

# 댓글 테이블 생성 함수
def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                comment TEXT NOT NULL
            )
        ''')

# 댓글 삽입 함수
def insert_comment(conn, comment):
    with conn:
        conn.execute('INSERT INTO comments (comment) VALUES (?)', (comment,))

# 모든 댓글 조회 함수
def get_all_comments(conn):
    with conn:
        comments = conn.execute('SELECT created_at, comment FROM comments').fetchall()
    yield from comments
