
from flask import Flask, request, jsonify
import sqlite3
import re  # ✅ Regular expressions module for name & department validation

# Initialize Flask App
app = Flask(__name__)

# Database Connection Function
def connect_db():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        department TEXT NOT NULL,
                        salary INTEGER NOT NULL)''')
    conn.commit()
    return conn

# Validation Functions
def is_valid_name(name):
    return re.match("^[A-Za-z ]+$", name) is not None

def is_valid_department(department):
    return re.match("^[A-Za-z ]+$", department) is not None

# Add Employee (POST Request)
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name, age, department, salary = data.get("name"), data.get("age"), data.get("department"), data.get("salary")
    
    if not (name and age and department and salary):
        return jsonify({"error": "All fields are required"}), 400
    if not is_valid_name(name) or not is_valid_department(department):
        return jsonify({"error": "Invalid name or department"}), 400
    if not (18 <= age <= 100):
        return jsonify({"error": "Age must be between 18 and 100"}), 400
    if salary <= 0:
        return jsonify({"error": "Salary must be greater than 0"}), 400
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, age, department, salary) VALUES (?, ?, ?, ?)", 
                   (name, age, department, salary))
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee added successfully!"}), 201

# View Employees (GET Request)
@app.route('/employees', methods=['GET'])
def get_employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return jsonify(employees)

@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()

    conn = connect_db()
    cursor = conn.cursor()

    # 🔹 Employee exist karta hai ya nahi check karo
    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    existing_employee = cursor.fetchone()

    if not existing_employee:
        return jsonify({"error": "Employee ID not found"}), 404

    # 🔹 Pehle se database me jo values hain, unko le lo
    existing_name, existing_age, existing_department, existing_salary = existing_employee[1:]

    # 🔹 Agar koi field missing hai, toh uski purani value use karo
    name = data.get("name", existing_name)
    age = data.get("age", existing_age)
    department = data.get("department", existing_department)
    salary = data.get("salary", existing_salary)

    # 🔹 Validation check (invalid data reject karne ke liye)
    if not is_valid_name(name) or not is_valid_department(department):
        return jsonify({"error": "Invalid name or department"}), 400
    if not (18 <= age <= 100):
        return jsonify({"error": "Age must be between 18 and 100"}), 400
    if salary <= 0:
        return jsonify({"error": "Salary must be greater than 0"}), 400

    # 🔹 Update query ab safely execute hogi
    cursor.execute("UPDATE employees SET name = ?, age = ?, department = ?, salary = ? WHERE id = ?", 
                   (name, age, department, salary, emp_id))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee updated successfully!"})

# View Employee by ID (GET Request)
@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee_by_id(emp_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch employee details
    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    employee = cursor.fetchone()

    conn.close()

    # If employee exists, return details; otherwise, return error
    if employee:
        emp_data = {
            "id": employee[0],
            "name": employee[1],
            "age": employee[2],
            "department": employee[3],
            "salary": employee[4]
        }
        return jsonify(emp_data)
    else:
        return jsonify({"error": "Employee ID not found"}), 404


# Delete Employee (DELETE Request)
@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee deleted successfully!"})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def home():
    return "Hello, Flask!"
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask is working!"

if __name__ == "__main__":
    app.run(debug=True)

