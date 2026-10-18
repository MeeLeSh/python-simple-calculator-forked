


def Calculate(a,b,op):
    result=0
    if op=="+":
        result=a+b
    elif op=="-":
        result=a-b
    elif op=="*":
        result=a*b
    elif op=="/":
        try:
            result=a/b
        except:
            print("Error")
    elif op=="%":
        result=a%b
    elif op=="**":
        result=a**b
    return result


def main():
 print("Welcome to our Arithmetic Calculator")
 op=input("""Operations:
 "+" - Add,
 "-" - Subtract,
 "*" - Multiply,
 "/" - Divide,
 "%" - Remainder,
 "**" - Power,
 Enter the operator: """)

 if op not in ("+","-","*","/","%","**"):
  print("Enter a valid operator")
 else:
  num1=float(input("Enter first number: "))
  num2=float(input("Enter second number: "))
  if op=="/" or op=="%":
   if num2==0: print("Division by 0 is not possible")
   else:
    print("Result:",Calculate(num1,num2,op))
  else:
   print("Result:",Calculate(num1,num2,op))
 print("Thanks for using this simple arithmetic calculator")


if __name__=="__main__":
 main()
