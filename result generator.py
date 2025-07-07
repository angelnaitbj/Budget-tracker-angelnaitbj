# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 11:16:14 2025


@author: naitb
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import platform

# Subject List
subjects = [
    "Mathematics", "English", "Science", "Social Studies", "Civic Education",
    "Religious Knowledge", "Health Education", "Computer", "Agriculture",
    "Verbal Reasoning", "Quantitative Reasoning", "Physical Education", "Handwriting",
    "Phonics", "Drawing", "Music", "Cultural & Creative Arts", "Home Economics",
    "French", "Literature", "Moral Instruction", "History", "Yoruba/Igbo/Hausa"
]

# ===== Main Window with Both Scrollbars =====
root = tk.Tk()
root.title("St. Paul Result Generator @AngelNaitbj")
root.geometry("1400x700")

# Outer frame holding canvas + scrollbars
outer_frame = tk.Frame(root)
outer_frame.pack(fill="both", expand=True)

main_canvas = tk.Canvas(outer_frame, bg="white")
v_scroll = tk.Scrollbar(outer_frame, orient="vertical", command=main_canvas.yview)
h_scroll = tk.Scrollbar(outer_frame, orient="horizontal", command=main_canvas.xview)

main_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
v_scroll.pack(side="right", fill="y")
h_scroll.pack(side="bottom", fill="x")
main_canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(main_canvas)
main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def configure_scroll(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scroll)

# ===== Header =====
tk.Label(
    scrollable_frame,
    text="St. Paul's Nursery & Primary Schools New Kutunku, Gwagwalada, Abuja",
    font=("Arial", 16, "bold")
).pack(pady=10)

# ===== Student Info =====
info_frame = tk.Frame(scrollable_frame)
info_frame.pack()

tk.Label(info_frame, text="Student Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
student_name = tk.Entry(info_frame, width=30)
student_name.grid(row=0, column=1, padx=10)

tk.Label(info_frame, text="Class Name:", font=("Arial", 12)).grid(row=0, column=2, sticky="e")
class_name_entry = tk.Entry(info_frame, width=30)
class_name_entry.grid(row=0, column=3, padx=10)

tk.Label(info_frame, text="Class Position:", font=("Arial", 12)).grid(row=0, column=4, sticky="e")
class_position_overall = tk.Entry(info_frame, width=20)
class_position_overall.grid(row=0, column=5, padx=10)

# ===== Result Table =====
table_frame = tk.LabelFrame(scrollable_frame, text="Student Results Table", padx=10, pady=10)
table_frame.pack(padx=10, pady=10)

headers = ["Subject", "CA", "Exam", "Subject Total", "Subject Position"]
for col, text in enumerate(headers):
    tk.Label(table_frame, text=text, font=("Arial", 10, "bold"), width=20).grid(row=0, column=col)

ca_entries = {}
exam_entries = {}
total_entries = {}
subject_pos_entries = {}

total_score_in_table = tk.StringVar()
total_var = tk.StringVar()
aggregate_var = tk.StringVar()

def update_totals(event=None):
    total = 0
    count = 0
    for subject in subjects:
        try:
            ca = int(ca_entries[subject].get() or 0)
            exam = int(exam_entries[subject].get() or 0)
            if 0 <= ca <= 40 and 0 <= exam <= 60:
                score = ca + exam
                total_entries[subject].config(state="normal")
                total_entries[subject].delete(0, tk.END)
                total_entries[subject].insert(0, str(score))
                total_entries[subject].config(state="readonly")
                total += score
                count += 1
            else:
                raise ValueError
        except ValueError:
            total_entries[subject].config(state="normal")
            total_entries[subject].delete(0, tk.END)
            total_entries[subject].insert(0, "Err")
            total_entries[subject].config(state="readonly")

    avg = total / count if count else 0
    total_score_in_table.set(str(total))
    total_var.set(str(total))
    aggregate_var.set(f"{avg:.2f}")

# Table rows
for i, subject in enumerate(subjects):
    tk.Label(table_frame, text=subject, width=20, anchor="w").grid(row=i + 1, column=0)

    ca = tk.Entry(table_frame, width=10)
    ca.grid(row=i + 1, column=1)
    ca.bind("<KeyRelease>", update_totals)
    ca_entries[subject] = ca

    exam = tk.Entry(table_frame, width=10)
    exam.grid(row=i + 1, column=2)
    exam.bind("<KeyRelease>", update_totals)
    exam_entries[subject] = exam

    total = tk.Entry(table_frame, width=10, state="readonly")
    total.grid(row=i + 1, column=3)
    total_entries[subject] = total

    pos = tk.Entry(table_frame, width=15)
    pos.grid(row=i + 1, column=4)
    subject_pos_entries[subject] = pos

# Total row
tk.Label(table_frame, text="TOTAL", font=("Arial", 10, "bold")).grid(row=len(subjects) + 1, column=0)
tk.Entry(table_frame, textvariable=total_score_in_table, state="readonly", width=10).grid(row=len(subjects) + 1, column=3)

# ===== Summary Section =====
summary_frame = tk.LabelFrame(scrollable_frame, text="Summary", padx=10, pady=10)
summary_frame.pack(padx=10, pady=10)

tk.Label(summary_frame, text="Total Score:", width=20).grid(row=0, column=0, sticky="w")
tk.Entry(summary_frame, textvariable=total_var, state="readonly", width=30).grid(row=0, column=1)

tk.Label(summary_frame, text="Aggregate:", width=20).grid(row=1, column=0, sticky="w")
tk.Entry(summary_frame, textvariable=aggregate_var, state="readonly", width=30).grid(row=1, column=1)

tk.Label(summary_frame, text="Overall Position:", width=20).grid(row=2, column=0, sticky="w")
overall_position = tk.Entry(summary_frame, width=30)
overall_position.grid(row=2, column=1)

# ===== Remarks Section =====
remarks_frame = tk.LabelFrame(scrollable_frame, text="Remarks", padx=10, pady=10)
remarks_frame.pack(padx=10, pady=10)

tk.Label(remarks_frame, text="Classteacher's Remark:", font=("Arial", 12)).grid(row=0, column=0, sticky="ne")
class_teacher_remark = tk.Text(remarks_frame, width=80, height=2)
class_teacher_remark.grid(row=0, column=1, padx=5, pady=5)

tk.Label(remarks_frame, text="Headteacher's Remark:", font=("Arial", 12)).grid(row=1, column=0, sticky="ne")
headteacher_remark = tk.Text(remarks_frame, width=80, height=2)
headteacher_remark.grid(row=1, column=1, padx=5, pady=5)

# ===== Export and Print Buttons =====
def export_to_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Result"
    ws.append(["Subject", "CA", "Exam", "Subject Total", "Subject Position"])
    for subject in subjects:
        ws.append([
            subject,
            ca_entries[subject].get(),
            exam_entries[subject].get(),
            total_entries[subject].get(),
            subject_pos_entries[subject].get()
        ])
    ws.append([])
    ws.append(["Total Score", total_var.get()])
    ws.append(["Aggregate", aggregate_var.get()])
    ws.append(["Overall Position", overall_position.get()])
    ws.append(["Class Teacher's Remark", class_teacher_remark.get("1.0", tk.END).strip()])
    ws.append(["Headteacher's Remark", headteacher_remark.get("1.0", tk.END).strip()])
    wb.save(file_path)
    messagebox.showinfo("Success", "Exported to Excel successfully.")

def export_to_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y, "St. Paul's Nursery & Primary Schools")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Student Name: {student_name.get()}")
    y -= 20
    c.drawString(50, y, f"Class: {class_name_entry.get()}   Class Position: {class_position_overall.get()}")
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Subject     CA     Exam     Total     Position")
    y -= 15
    c.setFont("Helvetica", 11)
    for subject in subjects:
        ca = ca_entries[subject].get()
        exam = exam_entries[subject].get()
        total = total_entries[subject].get()
        pos = subject_pos_entries[subject].get()
        c.drawString(50, y, f"{subject[:12]:<12} {ca:<6} {exam:<6} {total:<7} {pos}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 40
    y -= 20
    c.drawString(50, y, f"Total Score: {total_var.get()}   Aggregate: {aggregate_var.get()}")
    y -= 20
    c.drawString(50, y, f"Overall Position: {overall_position.get()}")
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Class Teacher Remark:")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(50, y, class_teacher_remark.get("1.0", tk.END).strip())
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Headteacher Remark:")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(50, y, headteacher_remark.get("1.0", tk.END).strip())
    c.save()
    messagebox.showinfo("Success", "Exported to PDF successfully.")
    return file_path

def print_result():
    path = export_to_pdf()
    if path:
        if platform.system() == "Windows":
            os.startfile(path, "print")
        elif platform.system() == "Darwin":
            os.system(f"lp {path}")
        else:
            os.system(f"lpr {path}")

# Buttons
button_frame = tk.Frame(scrollable_frame)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Export to Excel", command=export_to_excel, bg="lightblue", width=20).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Export to PDF", command=export_to_pdf, bg="lightgreen", width=20).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Print", command=print_result, bg="lightgray", width=20).grid(row=0, column=2, padx=10)


# ===== Run Application =====
root.mainloop()

input()