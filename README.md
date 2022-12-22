# Expression Evaluator
A simple Python class that takes in a mathematical expression as a string, evaluates it, and returns the result. Designed to be simple to use; just feed it a string, and if anything is wrong with your input it will tell you what the problem is.

## Usage:
```
calc = Calculator.Calculator()
expr = "(17.32 * 4.3301 + (4 ^ 3)) * -(11 / (24 - -19))(3.14)"
print(calc.evaluate(expr))
```

## Info
Recognizes the following operators: +, -, \*, /, %, ^  
You can enter any expression composed of these operators, digits, and  parentheses. Additionally, this class can simplify any number of sequential negative signs ("-"), so it can handle statements such as "2 -- -2". Implicit multiplication by parentheses is also understood (e.g. "2(3)" would be parsed as "2\*3").

Performs validation of the input. Checks for:  
- Balanced parentheses
- Balanced operators
- Valid decimal points (e.g. "3.14.159" is not valid)
- No invalid characters (i.e. no characters that are not digits, decimal points, operators, or parentheses).

This was my first dive into Python, so there may be some oddities in the code.
