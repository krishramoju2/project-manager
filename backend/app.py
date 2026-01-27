from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    return sqlite3.connect("database.db", check_same_thread=False)

db = get_db()
cur = db.cursor()

# ---- CREATE TABLES ----
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT,
 email TEXT,
 password TEXT,
 role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS projects (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT,
 status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 title TEXT,
 description TEXT,
 status TEXT,
 project_id INTEGER,
 assigned_user_id INTEGER
)
""")

db.commit()

# ---- DEFAULT DATA ----
cur.execute("SELECT COUNT(*) FROM users")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO users VALUES (NULL,'Admin','admin@pm.com','admin123','manager')")
    cur.execute("INSERT INTO users VALUES (NULL,'Bob','bob@pm.com','bob123','employee')")
    cur.execute("INSERT INTO users VALUES (NULL,'Charlie','charlie@pm.com','charlie123','employee')")

    cur.execute("INSERT INTO projects VALUES (NULL,'Website Revamp','ongoing')")

    cur.execute("""
    INSERT INTO tasks VALUES
    (NULL,'Design UI','Create homepage','pending',1,2),
    (NULL,'Backend APIs','Build APIs','pending',1,3)
    """)
    db.commit()

# ---- AUTH ----
@app.post("/register")
def register():
    u = request.json
    cur.execute(
        "INSERT INTO users VALUES (NULL,?,?,?,?)",
        (u["name"],u["email"],u["password"],u["role"])
    )
    db.commit()
    return {"msg":"Registered"}

@app.post("/login")
def login():
    u = request.json
    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (u["email"],u["password"])
    )
    row = cur.fetchone()
    if row:
        return jsonify({
            "id":row[0],
            "name":row[1],
            "email":row[2],
            "role":row[4]
        })
    return {}

# ---- DATA ----
@app.get("/projects")
def projects():
    cur.execute("SELECT * FROM projects")
    return jsonify(cur.fetchall())

@app.post("/projects")
def add_project():
    cur.execute("INSERT INTO projects VALUES (NULL,?,?)",
                (request.json["name"],"ongoing"))
    db.commit()
    return {"msg":"Project added"}

@app.get("/tasks/<int:uid>/<role>")
def tasks(uid, role):
    if role == "manager":
        cur.execute("SELECT * FROM tasks")
    else:
        cur.execute("SELECT * FROM tasks WHERE assigned_user_id=?", (uid,))
    return jsonify(cur.fetchall())

@app.post("/tasks")
def add_task():
    t = request.json
    cur.execute("""
      INSERT INTO tasks VALUES (NULL,?,?,?, ?,?)
    """,(t["title"],t["description"],"pending",t["project_id"],t["user_id"]))
    db.commit()
    return {"msg":"Task added"}

@app.post("/task/complete/<int:id>")
def complete_task(id):
    cur.execute("UPDATE tasks SET status='completed' WHERE id=?", (id,))
    db.commit()
    return {"msg":"Done"}

@app.post("/project/complete/<int:id>")
def complete_project(id):
    cur.execute("UPDATE projects SET status='completed' WHERE id=?", (id,))
    db.commit()
    return {"msg":"Done"}

app.run(host="0.0.0.0", port=5000, debug=True)

