print("Welcome to our Arithmetic Calculator")

op=input("""Operations:
"+"  - Add,
"-"  - Subtract,
"*"  - Multiply,
"/"  - Divide,
"%"  - Remainder,
"**" - Power,
Enter the operator: """)

if op not in ("+", "-", "*", "/", "%", "**"):
    print("Enter a valid operator")
else:
    if op in ("/"):
        num1=float(input("Enter dividend: "))
        num2=float(input("Enter divisor: "))
    elif op in ("**"):
        num1=float(input("Enter base: "))
        num2=float(input("Enter exponent: "))
    elif op in ("/","%"):
        num1=float(input("Enter dividend: "))
        num2=float(input("Enter divisor: "))
    else:
        num1=float(input("Enter first number: "))
        num2=float(input("Enter second number: "))
    if op=="+":
        print("Adding...")
        print("Result:",num1+num2)
    elif op=="-":
        print("Subtracting...")
        print("Result:",num1-num2)
    elif op=="*":
        print("Multiplying...")
        print("Result:",num1*num2)
    elif op=="/":
        if num2==0:
            print("Division by 0 is not possible")
        else:
            print("Dividing...")
            print("Result:",num1/num2)
    elif op=="%":
        if num2==0:
            print("Division by 0 is not possible")
        else:
            print("Finding Remainder...")
            print("Result:",num1%num2)
    elif op=="**":
        print("Evaluating...")
        print("Result:",num1**num2)

print("Thanks for using this simple arithmetic calculator")

