
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    data = load_data()
    # sort tasks by due date if present
    tasks = data.get("tasks", [])
    tasks_sorted = sorted(tasks, key=lambda t: t.get("date",""))
    return render_template("index.html", tasks=tasks_sorted)

@app.route("/add", methods=["GET","POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title","").strip()
        subject = request.form.get("subject","").strip()
        date = request.form.get("date","").strip()
        note = request.form.get("note","").strip()
        priority = request.form.get("priority","normal")
        if title:
            data = load_data()
            task = {
                "id": int(datetime.utcnow().timestamp()*1000),
                "title": title,
                "subject": subject,
                "date": date,
                "note": note,
                "priority": priority
            }
            data.setdefault("tasks", []).append(task)
            save_data(data)
        return redirect(url_for("index"))
    return render_template("add_task.html")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    data = load_data()
    tasks = data.get("tasks", [])
    tasks = [t for t in tasks if t.get("id") != task_id]
    data["tasks"] = tasks
    save_data(data)
    return redirect(url_for("index"))

@app.route("/export")
def export_html():
    data = load_data()
    tasks = sorted(data.get("tasks", []), key=lambda t: t.get("date",""))
    # render a printable page
    return render_template("export.html", tasks=tasks)

@app.route("/api/tasks")
def api_tasks():
    data = load_data()
    return jsonify(data.get("tasks", []))

if __name__ == "__main__":
    app.run(debug=True)
