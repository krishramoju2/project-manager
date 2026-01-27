from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="pm"
)
cur = db.cursor(dictionary=True)

@app.post("/register")
def register():
    u = request.json
    cur.execute(
        "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
        (u["name"],u["email"],u["password"],u["role"])
    )
    db.commit()
    return {"msg":"Registered"}

@app.post("/login")
def login():
    u = request.json
    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (u["email"],u["password"])
    )
    return jsonify(cur.fetchone())

@app.get("/users")
def users():
    cur.execute("SELECT id,name FROM users WHERE role='employee'")
    return jsonify(cur.fetchall())

@app.get("/projects")
def projects():
    cur.execute("SELECT * FROM projects")
    return jsonify(cur.fetchall())

@app.post("/projects")
def add_project():
    cur.execute(
        "INSERT INTO projects (name,status) VALUES (%s,'ongoing')",
        (request.json["name"],)
    )
    db.commit()
    return {"msg":"Project created"}

@app.get("/tasks/<int:uid>/<role>")
def tasks(uid, role):
    if role == "manager":
        cur.execute("""
          SELECT tasks.*, users.name employee
          FROM tasks JOIN users ON users.id = tasks.assigned_user_id
        """)
    else:
        cur.execute("SELECT * FROM tasks WHERE assigned_user_id=%s",(uid,))
    return jsonify(cur.fetchall())

@app.post("/tasks")
def add_task():
    t = request.json
    cur.execute("""
      INSERT INTO tasks (title,description,status,project_id,assigned_user_id)
      VALUES (%s,%s,'pending',%s,%s)
    """,(t["title"],t["description"],t["project_id"],t["user_id"]))
    db.commit()
    return {"msg":"Task added"}

@app.post("/task/complete/<int:id>")
def complete_task(id):
    cur.execute("UPDATE tasks SET status='completed' WHERE id=%s",(id,))
    db.commit()
    return {"msg":"Done"}

@app.post("/project/complete/<int:id>")
def complete_project(id):
    cur.execute("UPDATE projects SET status='completed' WHERE id=%s",(id,))
    db.commit()
    return {"msg":"Project Done"}

app.run(debug=True)
