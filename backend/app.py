import psycopg2
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "tasks_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    tasks = [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]
    return jsonify(tasks), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id;", (title, False))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"id": task_id, "title": title, "done": False}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(force=True) or {}
    title = data.get("title")
    done = data.get("done")

    if title is None and done is None:
        return jsonify({"error": "provide title and/or done"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # Build dynamic query depending on provided fields
    fields = []
    values = []
    if title is not None:
        fields.append("title = %s")
        values.append(title)
    if done is not None:
        fields.append("done = %s")
        values.append(bool(done))
    values.append(task_id)
    cur.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s RETURNING id, title, done;", values)
    row = cur.fetchone()
    conn.commit()
    cur.close(); conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": row[0], "title": row[1], "done": row[2]}), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close(); conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": row[0]}), 200

if __name__ == "__main__":
    # Run with builtin server for simplicity; in production use gunicorn
    app.run(host="0.0.0.0", port=5000)
