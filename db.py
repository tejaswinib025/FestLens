import sqlite3

def init_db():
    conn = sqlite3.connect("festival_log.db")
    cur = conn.cursor()
    # users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            phone TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    # media table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            festival TEXT,
            region TEXT,
            language TEXT,
            media_type TEXT,
            file_path TEXT,
            transcript TEXT,
            ai_caption TEXT,
            translation TEXT,
            tags TEXT,
            contributor TEXT,
            extra_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(phone, password):
    try:
        conn = sqlite3.connect("festival_log.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (phone, password) VALUES (?, ?)", (phone, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(phone, password):
    conn = sqlite3.connect("festival_log.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE phone=? AND password=?", (phone, password))
    user = cur.fetchone()
    conn.close()
    return user is not None

def insert_item(item):
    conn = sqlite3.connect("festival_log.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO media (title, festival, region, language, media_type, file_path,
                           transcript, ai_caption, translation, tags, contributor, extra_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (item["title"], item["festival"], item["region"], item["language"],
          item["media_type"], item["file_path"], item["transcript"],
          item["ai_caption"], item["translation"], item["tags"],
          item["contributor"], item["extra_json"]))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return nid

def query_items(filters, search=""):
    conn = sqlite3.connect("festival_log.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = "SELECT * FROM media WHERE 1=1"
    params = []
    if filters["festival"]:
        query += " AND festival LIKE ?"
        params.append("%" + filters["festival"] + "%")
    if filters["language"]:
        query += " AND language LIKE ?"
        params.append("%" + filters["language"] + "%")
    if filters["media_type"] and filters["media_type"] != "All":
        query += " AND media_type=?"
        params.append(filters["media_type"])
    if search:
        query += " AND (title LIKE ? OR tags LIKE ? OR festival LIKE ?)"
        params += ["%" + search + "%"] * 3
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()
    return [dict(row) for row in results]
