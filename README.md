# 🎓 Student Management System

A web-based **Student Management System** built using **Python and Streamlit**, allowing users to manage student records, upload data files, calculate grades, and view performance statistics.

![Screenshot](https://github.com/Ahmad-Ali-Rafique/Student_Management_System/blob/main/LMS%20Dashboard.png)

---

## 📌 Features

- ✅ Add individual student records (Name, Roll No, Marks)
- ✅ Calculate and assign grades automatically
- ✅ Upload data from `.csv` or `.xlsx` files
- ✅ Prevent duplicate entries based on Roll No
- ✅ View all student records in a clean, searchable table
- ✅ Update or delete student records easily
- ✅ View insightful statistics:
  - Total students
  - Average marks
  - Grade distribution (bar chart)
- ✅ Export all data as a `.csv` file
- ✅ Reset all data with a single click

---

## 📸 Demo

> Here's the live app on Streamlit Cloud (deployed)  
> 🔗 [Live Demo Link](https://student-management-system-lms.streamlit.app/) 

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Streamlit** – for the web interface
- **Pandas** – for data processing
- **JSON** – for data storage
- **Matplotlib/Streamlit Charts** – for visual statistics

---

## 📁 File Structure

```
student-management-system/
├── app.py               # Main Streamlit app
├── students.json        # Local data storage (JSON format)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.10 or later installed
- Pip or Conda environment

### 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/student-management-system.git
cd student-management-system
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

---

## 📤 Upload File Format

Make sure your `.csv` or `.xlsx` file has the following columns:

| name       | roll_no | marks |
|------------|---------|--------|
| John Smith | 101     | 89.5   |
| Jane Doe   | 102     | 95.0   |

> ⚠️ Roll No must be unique

---

## 📊 Grade Calculation Logic

| Marks Range | Grade |
|-------------|-------|
| 90-100      | A     |
| 80-89       | B     |
| 70-79       | C     |
| 60-69       | D     |
| Below 60    | F     |

---

## 🧑‍💻 Author

**Ahmad Ali Rafique**  
AI & Machine Learning Specialist | Deep Learning | NLP Expert  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/ahmad-ali-rafique/)  
🎥 [YouTube: AboutAI](https://www.youtube.com/@AhmadAliRafique)

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ⭐️ Support

If you like this project, give it a ⭐️ on GitHub and feel free to contribute or provide feedback!

---
