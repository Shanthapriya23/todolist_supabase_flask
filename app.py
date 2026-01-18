from flask import Flask,render_template,request,jsonify
from supabase import create_client
#for deploying
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL:
    raise ValueError("Supabase url not set")

if not SUPABASE_KEY:
    raise ValueError("Supabase key not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

#read all todos
@app.route("/todos",methods=["GET"])
def get_todos():
    rows  = supabase.table("todos").select("*").order("id").execute()
    return jsonify(rows.data if hasattr(rows, "data")else rows)

#add new item to todo table
@app.route("/todos",methods=["POST"])
def add_todo():
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title required"}),400
    new_row = {"title":title, "done":False}
    res = supabase.table("todos").insert(new_row).execute()
    return jsonify(res.data if hasattr(res,"data")else res),201

#delete an item from todo table
@app.route("/todos/<int:todo_id>",methods=["DELETE"])
def delete_todo(todo_id):
    res = supabase.table("todos").delete().eq("id",todo_id).execute()
    return jsonify(res.data if hasattr(res,"data") else res)

#update an item in todo table
@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    data = request.json
    updates = {}
    if "title" in data:
        updates["title"] = data["title"]
    if "done" in data:
        updates["done"] = bool(data["done"])
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    res = supabase.table("todos").update(updates).eq("id", todo_id).execute()
    return jsonify(res.data if hasattr(res, "data") else res)


#to run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

 