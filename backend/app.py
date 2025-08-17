from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Подключение к MongoDB
DB_HOST = os.getenv("DB_HOST", "mongo")  # в docker-compose сервис можно назвать mongo
DB_PORT = int(os.getenv("DB_PORT", "27017"))
DB_NAME = os.getenv("DB_NAME", "tasks_db")

client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]
tasks_collection = db["tasks"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = []
    for t in tasks_collection.find():
        tasks.append({
            "id": str(t["_id"]),
            "title": t["title"],
            "done": t.get("done", False)
        })
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    result = tasks_collection.insert_one({"title": title, "done": False})
    return jsonify({
        "id": str(result.inserted_id),
        "title": title,
        "done": False
    }), 201


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(force=True) or {}
    update_fields = {}

    if "title" in data:
        update_fields["title"] = data["title"]
    if "done" in data:
        update_fields["done"] = bool(data["done"])

    if not update_fields:
        return jsonify({"error": "provide title and/or done"}), 400

    result = tasks_collection.find_one_and_update(
        {"_id": ObjectId(task_id)},
        {"$set": update_fields},
        return_document=True
    )

    if not result:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "id": str(result["_id"]),
        "title": result["title"],
        "done": result["done"]
    }), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = tasks_collection.find_one_and_delete({"_id": ObjectId(task_id)})

    if not result:
        return jsonify({"error": "not found"}), 404

    return jsonify({"deleted": str(result["_id"])}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
