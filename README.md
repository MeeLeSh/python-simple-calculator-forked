# python-simple-calculator

### 📘 Overview
This is a **simple command-line arithmetic calculator** written in **Python**.  
It allows users to perform basic mathematical operations like addition, subtraction, multiplication, division, remainder, and exponentiation — all through an interactive input prompt.

---

## ⚙️ Features
- **Addition**
- **Subtraction**
- **Multiplication**
- **Division** (with zero-division protection)
- **Remainder (Modulus)**
- **Power (Exponentiation)**

---

## 🖥️ How It Works
1. When you run the program, it displays:
   ```python
   Welcome to our Arithmetic Calculator
   ```
2. It then asks you to choose an operation:
   ```python
   Operations:
    "+"  - Add,
    "-"  - Subtract,
    "*"  - Multiply,
    "/"  - Divide,
    "%"  - Remainder,
    "**" - Power,
   Enter the operator:
   ```
3. Based on your choice, you will be asked to enter two numbers (e.g., dividend and divisor for division).  
4. The calculator performs the selected operation and prints the result.

---

## 🧾 Example
```bash
Welcome to our Arithmetic Calculator
Operations:
"+"  - Add,
"-"  - Subtract,
"*"  - Multiply,
"/"  - Divide,
"%"  - Remainder,
"**" - Power,
Enter the operator: *
Enter first number: 5
Enter second number: 7
Multiplying...
Result: 35.0
Thanks for using this simple arithmetic calculator
```

---

## 🚀 How to Run
Make sure you have **Python 3** installed.  
Then run the script using your terminal or command prompt:

```bash
python calculator.py
```

---

## 🧠 Concepts Used
- Conditional statements (`if`, `elif`, `else`)
- Input handling with `input()`
- Type conversion using `float()`
- Basic arithmetic operators in Python

---

## 🧰 Future Improvements
- Add support for more operations (like square root, logarithm, etc.)
- Allow multiple operations in one session
- Add a GUI using `tkinter` or a web version using Flask
