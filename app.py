import json
import os
import pandas as pd
import streamlit as st
from typing import List, Dict

# ------------------- Constants -------------------
DATA_FILE = "students.json"

# ------------------- Grade Calculation -------------------
def calculate_grade(marks: float) -> str:
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "F"

# ------------------- Load & Save -------------------
def load_students() -> List[Dict]:
    """
    Loads students from JSON and makes sure every record has a grade.
    """
    students: List[Dict] = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                students = json.load(f)
        except json.JSONDecodeError:
            pass

    # ✨ Auto-backfill missing grades
    rerecord = False
    for s in students:
        if "grade" not in s:
            s["grade"] = calculate_grade(float(s["marks"]))
            rerecord = True
    if rerecord:  # save back only if we changed something
        save_students(students)

    return students


def save_students(students: List[Dict]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# ------------------- Core Functionalities -------------------
def add_student(name: str, roll_no: str, marks: float) -> None:
    students = load_students()
    if any(s["roll_no"] == roll_no for s in students):
        st.warning("⚠️ Student with this roll number already exists.")
        return
    students.append(
        {
            "name": name,
            "roll_no": roll_no,
            "marks": marks,
            "grade": calculate_grade(marks),
        }
    )
    save_students(students)
    st.success("✅ Student added successfully.")

def upload_file(file) -> None:
    try:
        df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return

    required = {"name", "roll_no", "marks"}
    if not required.issubset(df.columns):
        st.error("File must contain 'name', 'roll_no', and 'marks' columns.")
        return

    df = df[["name", "roll_no", "marks"]].dropna()
    df["marks"] = pd.to_numeric(df["marks"], errors="coerce")
    df.dropna(subset=["marks"], inplace=True)
    df["grade"] = df["marks"].apply(calculate_grade)

    new_records = df.to_dict(orient="records")
    existing = load_students()
    existing_rolls = {s["roll_no"] for s in existing}

    added, skipped = 0, 0
    for rec in new_records:
        if rec["roll_no"] in existing_rolls:
            skipped += 1
            continue
        existing.append(rec)
        added += 1

    save_students(existing)
    st.success(f"📥 File processed. Added: {added}, Skipped (duplicates): {skipped}")

def download_csv() -> bytes:
    students = load_students()
    if not students:
        return b""
    return pd.DataFrame(students).to_csv(index=False).encode("utf-8")

def view_students():
    students = load_students()
    if students:
        st.dataframe(pd.DataFrame(students))
    else:
        st.info("No student records found.")

def update_student_marks():
    roll = st.text_input("Enter Roll No")
    new_marks = st.number_input("Enter New Marks", 0.0, 100.0, step=0.1)
    if st.button("Update Marks"):
        if not (0 <= new_marks <= 100):
            st.error("Marks must be between 0 and 100.")
            return
        students = load_students()
        for s in students:
            if s["roll_no"] == roll:
                s["marks"] = new_marks
                s["grade"] = calculate_grade(new_marks)
                save_students(students)
                st.success("✅ Marks updated successfully.")
                return
        st.warning("⚠️ Student not found.")

def delete_student():
    roll = st.text_input("Enter Roll No to Delete")
    if st.button("Delete"):
        students = load_students()
        new_students = [s for s in students if s["roll_no"] != roll]
        if len(new_students) == len(students):
            st.warning("⚠️ Student not found.")
        else:
            save_students(new_students)
            st.success("✅ Student deleted.")

def show_statistics():
    students = load_students()
    if not students:
        st.info("No data to show.")
        return

    df = pd.DataFrame(students)
    st.metric("Total Students", len(df))
    st.metric("Average Marks", round(df["marks"].mean(), 2))

    grade_counts = df["grade"].value_counts().sort_index()
    st.subheader("📊 Grade Distribution")
    st.bar_chart(grade_counts)

# ------------------- Streamlit Layout -------------------
st.set_page_config(page_title="Student Dashboard", layout="centered")
st.title("🎓 Student Management System")

# Add new student
st.header("Add New Student :")
with st.form("add_student_form"):
    name = st.text_input("Name")
    roll_no = st.text_input("Roll No")
    marks = st.number_input("Marks (0-100)", 0.0, 100.0, step=0.1)
    if st.form_submit_button("Add Student"):
        if name and roll_no:
            add_student(name, roll_no, marks)
        else:
            st.error("Please fill in all fields.")

st.divider()

# Stats
st.header("📊 Statistics")
show_statistics()

st.divider()

# Download
st.header("⬇️ Download All Students Data")
csv_data = download_csv()
if csv_data:
    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name="students_data.csv",
        mime="text/csv",
    )
else:
    st.info("No data available to download.")

# ------------------- Collapsible Menu -------------------
with st.expander("☰ Click to Open Sidebar Menu", expanded=False):
    st.sidebar.header("📂 Menu")
    sidebar_option = st.sidebar.radio(
        "Choose Option",
        [
            "None",
            "Upload File",
            "View All Students",
            "Update Marks",
            "Delete Student",
            "Reset All Data",
        ],
    )

    if sidebar_option == "Upload File":
        file = st.sidebar.file_uploader(
            "Upload Excel or CSV", type=["csv", "xlsx"]
        )
        if file:
            upload_file(file)

    elif sidebar_option == "View All Students":
        st.subheader("All Students")
        view_students()

    elif sidebar_option == "Update Marks":
        st.subheader("Update Student Marks")
        update_student_marks()

    elif sidebar_option == "Delete Student":
        st.subheader("Delete a Student")
        delete_student()

    elif sidebar_option == "Reset All Data":
        save_students([])
        st.sidebar.success("✅ All student data cleared.")
