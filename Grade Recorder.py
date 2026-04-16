from flask import Flask, request, jsonify
import json
import statistics
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# ---------------- FILE HANDLING ---------------- #

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}  # prevent crash if file is corrupted

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- CRUD ---------------- #

@app.route("/add_class", methods=["POST"])
def add_class():
    data = load_data()
    req = request.get_json()

    if not req or "class_name" not in req:
        return jsonify({"error": "class_name is required"}), 400

    class_name = req["class_name"]

    if class_name in data:
        return jsonify({"error": "Class already exists"}), 400

    data[class_name] = {}
    save_data(data)
    return jsonify({"message": "Class added"})


@app.route("/add_student", methods=["POST"])
def add_student():
    data = load_data()
    req = request.get_json()

    if not req or "class_name" not in req or "student" not in req:
        return jsonify({"error": "class_name and student required"}), 400

    class_name = req["class_name"]
    student = req["student"]

    if class_name not in data:
        return jsonify({"error": "Class not found"}), 404

    if student in data[class_name]:
        return jsonify({"error": "Student already exists"}), 400

    data[class_name][student] = []
    save_data(data)
    return jsonify({"message": "Student added"})


@app.route("/add_grade", methods=["POST"])
def add_grade():
    data = load_data()
    req = request.get_json()

    if not req or "class_name" not in req or "student" not in req or "grade" not in req:
        return jsonify({"error": "Missing fields"}), 400

    class_name = req["class_name"]
    student = req["student"]

    try:
        grade = float(req["grade"])  # ensure number
    except:
        return jsonify({"error": "Grade must be a number"}), 400

    if class_name not in data or student not in data[class_name]:
        return jsonify({"error": "Class or student not found"}), 404

    data[class_name][student].append(grade)
    save_data(data)
    return jsonify({"message": "Grade added"})

# ---------------- ANALYSIS ---------------- #

@app.route("/student_stats", methods=["GET"])
def student_stats():
    data = load_data()
    class_name = request.args.get("class_name")
    student = request.args.get("student")

    if class_name not in data or student not in data[class_name]:
        return jsonify({"error": "Not found"}), 404

    grades = data[class_name][student]

    if len(grades) == 0:
        return jsonify({"error": "No grades"}), 400

    result = {
        "highest": max(grades),
        "lowest": min(grades),
        "mean": round(statistics.mean(grades), 2),
        "mode": statistics.multimode(grades)  # safer than mode()
    }

    return jsonify(result)


@app.route("/class_stats", methods=["GET"])
def class_stats():
    data = load_data()
    class_name = request.args.get("class_name")

    if class_name not in data:
        return jsonify({"error": "Class not found"}), 404

    all_grades = []
    for student in data[class_name]:
        all_grades.extend(data[class_name][student])

    if len(all_grades) == 0:
        return jsonify({"error": "No grades"}), 400

    result = {
        "highest": max(all_grades),
        "lowest": min(all_grades),
        "mean": round(statistics.mean(all_grades), 2),
        "mode": statistics.multimode(all_grades)
    }

    return jsonify(result)

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)