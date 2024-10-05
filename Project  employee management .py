#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk
from tkinter import messagebox
import sqlite3

class Employee:
    def _init_(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

    def _repr_(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Dept: {self.department}, Salary: {self.salary}"


class EmployeeManager:
    def _init_(self, db):
        self.db = db

    def add_employee(self, emp):
        self.db.add_employee(emp)

    def remove_employee(self, emp_id):
        self.db.remove_employee(emp_id)

    def update_employee(self, emp_id, **kwargs):
        self.db.update_employee(emp_id, **kwargs)

    def list_employees(self):
        return self.db.list_employees()


class Database:
    def _init_(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                name TEXT,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()

    def add_employee(self, emp):
        self.cursor.execute('INSERT INTO employees VALUES (?, ?, ?, ?)',
                            (emp.emp_id, emp.name, emp.department, emp.salary))
        self.conn.commit()

    def remove_employee(self, emp_id):
        self.cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
        self.conn.commit()

    def update_employee(self, emp_id, **kwargs):
        columns = [f"{key} = ?" for key in kwargs]
        values = list(kwargs.values()) + [emp_id]
        self.cursor.execute(f"UPDATE employees SET {', '.join(columns)} WHERE id = ?", values)
        self.conn.commit()

    def list_employees(self):
        self.cursor.execute('SELECT * FROM employees')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


class EmployeeApp:
    def _init_(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Employee Management System")

        tk.Label(root, text="Employee ID").grid(row=0, column=0)
        tk.Label(root, text="Name").grid(row=1, column=0)
        tk.Label(root, text="Department").grid(row=2, column=0)
        tk.Label(root, text="Salary").grid(row=3, column=0)

        self.emp_id_entry = tk.Entry(root)
        self.name_entry = tk.Entry(root)
        self.dept_entry = tk.Entry(root)
        self.salary_entry = tk.Entry(root)

        self.emp_id_entry.grid(row=0, column=1)
        self.name_entry.grid(row=1, column=1)
        self.dept_entry.grid(row=2, column=1)
        self.salary_entry.grid(row=3, column=1)

        tk.Button(root, text="Add Employee", command=self.add_employee).grid(row=4, column=0)
        tk.Button(root, text="Update Employee", command=self.update_employee).grid(row=4, column=1)
        tk.Button(root, text="Remove Employee", command=self.remove_employee).grid(row=5, column=0)
        tk.Button(root, text="List Employees", command=self.list_employees).grid(row=5, column=1)

    def add_employee(self):
        emp_id = self.emp_id_entry.get()
        name = self.name_entry.get()
        department = self.dept_entry.get()
        salary = self.salary_entry.get()

        if emp_id and name and department and salary:
            try:
                salary = float(salary)
                emp = Employee(emp_id, name, department, salary)
                self.manager.add_employee(emp)
                messagebox.showinfo("Success", f"Employee {name} added successfully.")
            except ValueError:
                messagebox.showerror("Error", "Salary must be a number.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def update_employee(self):
        emp_id = self.emp_id_entry.get()
        name = self.name_entry.get()
        department = self.dept_entry.get()
        salary = self.salary_entry.get()

        update_data = {}
        if name:
            update_data['name'] = name
        if department:
            update_data['department'] = department
        if salary:
            try:
                update_data['salary'] = float(salary)
            except ValueError:
                messagebox.showerror("Error", "Salary must be a number.")
                return

        if emp_id and update_data:
            self.manager.update_employee(emp_id, **update_data)
            messagebox.showinfo("Success", f"Employee {emp_id} updated.")
        else:
            messagebox.showerror("Error", "Employee ID and at least one other field are required.")

    def remove_employee(self):
        emp_id = self.emp_id_entry.get()
        if emp_id:
            self.manager.remove_employee(emp_id)
            messagebox.showinfo("Success", f"Employee {emp_id} removed.")
        else:
            messagebox.showerror("Error", "Employee ID is required.")

    def list_employees(self):
        employees = self.manager.list_employees()
        if employees:
            emp_list = "\n".join([f"ID: {emp[0]}, Name: {emp[1]}, Dept: {emp[2]}, Salary: {emp[3]}" for emp in employees])
            messagebox.showinfo("Employee List", emp_list)
        else:
            messagebox.showinfo("Employee List", "No employees found.")

        if _name_ == "_main_":
            db = Database()
            manager = EmployeeManager(db)
            root = tk.Tk()
            app = EmployeeApp(root, manager)
            root.mainloop()
            db.close()


# In[ ]:




