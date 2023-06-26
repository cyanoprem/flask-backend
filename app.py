from flask import Flask, render_template, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from config import MONGODB_URI

app = Flask(__name__)

uri = MONGODB_URI

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["tasks"]
col = db["todos"]

@app.route("/")
def home():
    todos = col.find()
    return render_template("index.html", todos=todos)

@app.route("/add_todo", methods=["POST"])
def add_todo():
    todo = request.form["todo"]
    col.insert_one({"todo": todo, "completed": "no"})
    return redirect("/")

@app.route("/delete_todo", methods=["POST"])
def delete_todo():
    todo_id = request.form["todo_id"]
    col.delete_one({"_id": ObjectId(todo_id)})
    return redirect("/")

@app.route("/update_todo", methods=["POST"])
def update_todo():
    todo_id = request.form["todo_id"]
    updated_todo = request.form["updated_todo"]
    col.update_one({"_id": ObjectId(todo_id)}, {"$set": {"todo": updated_todo}})
    return redirect("/")

@app.route("/update_completion", methods=["POST"])
def update_completion():
    todo_id = request.form["todo_id"]
    todo = col.find_one({"_id": ObjectId(todo_id)})
    completed = todo["completed"]
    if completed == "no":
        col.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": "yes"}})
    else:
        col.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": "no"}})
    return redirect("/")

if __name__ == "__main__":
    app.run()
