# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 18:59:07 2025

@author: naitb
"""

import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("AngelNaitbj C777® Calculator")
root.geometry("320x400")
root.resizable(False, False)

# Expression storage
expression = ""
input_text = tk.StringVar()

# Input display
input_frame = tk.Frame(root, width=312, height=50, bd=0, highlightbackground="black", highlightthickness=2)
input_frame.pack(side=tk.TOP)

input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text,
                       width=50, bg="#eee", bd=0, justify=tk.RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=10)

# Functions
def btn_click(item):
    global expression
    expression += str(item)
    input_text.set(expression)

def btn_clear():
    global expression
    expression = ""
    input_text.set("")

def btn_backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)

def btn_equal():
    global expression
    try:
        result = str(eval(expression))
    except ZeroDivisionError:
        result = "Error: Division by zero"
    except SyntaxError:
        result = "Syntax Error"
    except:
        result = "Error"
    input_text.set(result)
    expression = ""

# Optional: keyboard input support
def keypress(event):
    key = event.char
    if key in "0123456789+-*/.=":
        if key == "=":
            btn_equal()
        else:
            btn_click(key)
    elif event.keysym == "BackSpace":
        btn_backspace()
    elif event.keysym.lower() == "c":
        btn_clear()

root.bind("<Key>", keypress)

# Button layout frame
btns_frame = tk.Frame(root, width=312, height=272.5, bg="grey")
btns_frame.pack()

# First row
tk.Button(btns_frame, text="Clear", fg="white", width=21, height=3, bd=0, bg="#d9534f", command=btn_clear).grid(row=0, column=0, columnspan=2, padx=1, pady=1)
tk.Button(btns_frame, text="⌫", fg="black", width=10, height=3, bd=0, bg="#eee", command=btn_backspace).grid(row=0, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="/", fg="black", width=10, height=3, bd=0, bg="#ffa", command=lambda: btn_click("/")).grid(row=0, column=3, padx=1, pady=1)

# Second row
tk.Button(btns_frame, text="7", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(7)).grid(row=1, column=0, padx=1, pady=1)
tk.Button(btns_frame, text="8", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(8)).grid(row=1, column=1, padx=1, pady=1)
tk.Button(btns_frame, text="9", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(9)).grid(row=1, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="*", width=10, height=3, bd=0, bg="#ffa", command=lambda: btn_click("*")).grid(row=1, column=3, padx=1, pady=1)

# Third row
tk.Button(btns_frame, text="4", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(4)).grid(row=2, column=0, padx=1, pady=1)
tk.Button(btns_frame, text="5", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(5)).grid(row=2, column=1, padx=1, pady=1)
tk.Button(btns_frame, text="6", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(6)).grid(row=2, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="-", width=10, height=3, bd=0, bg="#ffa", command=lambda: btn_click("-")).grid(row=2, column=3, padx=1, pady=1)

# Fourth row
tk.Button(btns_frame, text="1", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(1)).grid(row=3, column=0, padx=1, pady=1)
tk.Button(btns_frame, text="2", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(2)).grid(row=3, column=1, padx=1, pady=1)
tk.Button(btns_frame, text="3", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(3)).grid(row=3, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="+", width=10, height=3, bd=0, bg="#ffa", command=lambda: btn_click("+")).grid(row=3, column=3, padx=1, pady=1)

# Fifth row
tk.Button(btns_frame, text="0", width=21, height=3, bd=0, bg="#fff", command=lambda: btn_click(0)).grid(row=4, column=0, columnspan=2, padx=1, pady=1)
tk.Button(btns_frame, text=".", width=10, height=3, bd=0, bg="#fff", command=lambda: btn_click(".")).grid(row=4, column=2, padx=1, pady=1)
tk.Button(btns_frame, text="=", width=10, height=3, bd=0, bg="#5cb85c", command=btn_equal).grid(row=4, column=3, padx=1, pady=1)

# Run the GUI
root.mainloop()
input()