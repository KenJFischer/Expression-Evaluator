# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 14:50:59 2022

@author: Ken


A simple calculator that lets you type math expressions (using any symbol in OPERATORS as well as parentheses)
into the console and prints out the result. You can include any number of sequential -'s,
and it works with decimal values. However, there must always be a number to the right and left
of a decimal point. Checks that the expression is valid before computing anything.


EXAMPLE USAGE:
    calc = Calculator.Calculator()
    while True:
        print(calc.evaluate(input()))

"""

import re


class Calculator:
    
    OPERATORS = [ "^", "*", "/", "%", "+", "-" ]
    __inputString = ""
    __badInput = False

    #================================================
    # pass in an expression, returns the result or None if bad expression
    def evaluate(self, string):
        if self.setInput(string) != -1:
            return self.getResult()

    #================================================
    # set the input string and ensure it is valid (but doesn't check parentheses!)
    # checking for balanced parentheses occurs when you call getResult()
    # returns -1 if not valid and 1 if valid
    def setInput(self, string): 
        self.__badInput = False
        # clean input
        string = string.replace(" ", "")
        string = string.replace(")(", ")*(")
        
        # check for invalid characters, validate decimal points, and add explicit "*" for implicit multiplication on parentheses
        foundDecimal = False
        for i in range(0, len(string)):
            if not string[i].isdigit() and string[i] not in self.OPERATORS and string[i] != "." and\
                string[i] != "(" and string[i] != ")":
                return self.__setInputHelper(True, string, "Invalid character: " + string[i])
            # enforce only one decimal point per number
            if string[i] == ".":
                if foundDecimal:
                    return self.__setInputHelper(True, string, "Multiple decimal points in a single number")
                foundDecimal = True
            elif string[i] in self.OPERATORS:
                foundDecimal = False
            if i > 0 and string[i] == "(" and string[i - 1].isdigit():
                string = string[0 : i] + "*" + string[i : len(string)]
                i += 1
            elif i > 0 and string[i - 1] == ")" and string[i].isdigit():
                string = string[0 : i] + "*" + string[i : len(string)]
                i += 1
                
        # remove symbols to facilitate checking for a valid statement
        temp = string.replace("(", "")
        temp = temp.replace(")", "")
        while temp.find("--") != -1:
            temp = temp.replace("--", "-")
                
        if temp == "":
            return self.__setInputHelper(True, string, "Enter an expression")
        
        # check for invalid decimal and parenthesis combinations, since we can't check that in temp
        if string.find(".(") > -1 or string.find(".)") > -1 or string.find("(.") > -1 or string.find(").") > -1:
            return self.__setInputHelper(True, string, "Invalid decimal")
        
        for c in range(0, len(temp)):
            if temp[c] in self.OPERATORS or temp[c] == ".": # check balanced operators and decimal points
                
                # operator should not be at start or end of expression (except negative sign at start)
                if c == 0 and temp[c] != "-":
                    return self.__setInputHelper(True, string, "Operator cannot be at start of expression")
                elif c == len(temp) - 1:
                    return self.__setInputHelper(True, string, "Operator cannot be at end of expression")
                
                # if not a negative sign (i.e. it is actually an operator)
                if not (temp[c] == "-" and temp[c + 1].isdigit()):
                    # check before and after operator for arguments
                    if not temp[c - 1].isdigit():
                        return self.__setInputHelper(True, string, "Invalid operation: " + str(temp[c-1]) + str(temp[c]))
                    elif not temp[c + 1].isdigit() and not (temp[c + 1] == "-" and temp[c + 2].isdigit()):
                        return self.__setInputHelper(True, string, "Invalid operation: " + str(temp[c]) + str(temp[c + 1]))
                    
        return self.__setInputHelper(False, string)
        
    #================================================
    def getInputString(self):
        return self.__inputString
    
    #================================================
    def getInputStringLength(self):
        return len(self.__inputString)     
        
    #================================================
    # parse and evaluate the input string and return the result
    def getResult(self): 
        if not self.__badInput:
            result = self.__getResultHelper(self.getInputString())
            if result == None:
                return
            else:
                return float(result)
        else:
            print("Bad Input")
    
    #================================================
    # returns -1 if not valid, else returns 1 and sets __inputString
    def __setInputHelper(self, badInput, string, msg = "Bad Input"):
        self.__badInput = badInput
        if badInput:
            print(msg)
            return -1
        
        self.__inputString = string
        return 1
    
    #================================================
    # simplify parentheses (find all parentheses and evaluate their internal expressions)
    def __getResultHelper(self, string):
        openIndex = string.find("(")
        
        while openIndex != -1:
            closeIndex = self.__getCloseParenIndex(openIndex, string)                
            
            if closeIndex != -1: # we have a pair of parentheses
                newString = ""
                if openIndex == 0:
                    # recursively evaluate within the parentheses
                    newString = self.__getResultHelper(str(string[openIndex + 1 : closeIndex]))
                else:
                    # recursively evaluate within the parentheses
                    newString = str(string[0 : openIndex]) + self.__getResultHelper(str(string[openIndex + 1 : closeIndex]))
                if closeIndex < len(string) - 1:
                    newString += str(string[closeIndex + 1 : len(string)])
                    
                string = str(newString)
            else:
                print("Unbalanced Parentheses")
                return 
                    
            openIndex = string.find("(")
            
        closeIndex = string.find(")")
        if closeIndex != -1: # if unmatched close parenthesis
            print("Unbalanced Parentheses")
            return 
        
        # at this point we have a long expression with no parentheses, so we can evaluate
        return self.__evaluateExpression(string) # essentially Base Case
    
    #================================================
    # finds the index in string of the ")" corresponding to a "(" at openIndex
    def __getCloseParenIndex(self, openIndex, string): 
        stack = [ "(" ]
        
        for i in range(openIndex + 1, len(string)):
            
            if string[i] ==  "(":
                stack.append(string[i])
            elif string[i] == ")":
                stack.pop()
                
            if len(stack) == 0:
                return i
            
        if len(stack) != 0:
            return -1 # unmatched open parenthesis
    
    #================================================
    # completely evaluate an expression that contains no parentheses
    def __evaluateExpression(self, expr): 
        while not self.__isNumber(expr):
            expr = self.__simplifyExpression(expr)
            
        return expr
    
    #================================================
    # checks that expr is a number composed of only digits and ".", with an optional leading "-" 
    # doesn't enforce only one decimal point per number (that was enforced in setInput())
    def __isNumber(self, expr): 
        temp = ""
        
        if expr[0] == "-":
            temp = expr[1 : len(expr)]
        else:
            temp = expr
            
        for c in str(temp):
            if not c.isdigit() and c != ".":
                return False
            
        return True
    
    #================================================
    # evaluates the operation that should come first, based on order of operations
    def __simplifyExpression(self, expr): 
        result = expr
        
        # evaluate exponentiation
        index = expr.find("^")
        
        if index != -1:
            leadArg, startIndex, tailArg, tailIndex, expr, index = self.__findArgs(expr, index)
            result = leadArg ** tailArg
            return self.__createSimplifiedExpr(expr, index, result, startIndex, tailIndex)
        
        # evaluate multiplication, division, and modulus, from left to right
        index = expr.find("*")
        temp = expr.find("/")
        isDivision = False
        isModulo = False
        
        if (temp < index or index == -1) and temp != -1:
            index = temp  
            isDivision = True
        temp = expr.find("%")
        if (temp < index or index == -1) and temp != -1:
            index = temp
            isModulo = True
            isDivision = False
            
        if index != -1:
            if isDivision:
                leadArg, startIndex, tailArg, tailIndex, expr, index = self.__findArgs(expr, index)
                result = leadArg / tailArg
                return self.__createSimplifiedExpr(expr, index, result, startIndex, tailIndex)
            elif isModulo:
                leadArg, startIndex, tailArg, tailIndex, expr, index = self.__findArgs(expr, index)
                result = leadArg % tailArg
                return self.__createSimplifiedExpr(expr, index, result, startIndex, tailIndex)
            else:
                leadArg, startIndex, tailArg, tailIndex, expr, index = self.__findArgs(expr, index)
                result = leadArg * tailArg
                return self.__createSimplifiedExpr(expr, index, result, startIndex, tailIndex)
         
        # evaluate addition and subtraction, from left to right
        index = expr.find("+")        
        temp = re.search(r'\d-[-\d]', expr) # use regular expression to only pick up certain -'s
        
        if temp:
            temp = temp.start() + 1
        else:
            temp = -1
        isSubtraction = False
        
        if (temp < index or index == -1) and temp != -1:
            index = temp  
            isSubtraction = True
        
        if index != -1:
            if isSubtraction:
                leadArg, startIndex, tailArg, tailIndex, expr, index = self.__findArgs(expr, index)
                result = leadArg - tailArg
                return self.__createSimplifiedExpr(expr, index, result, startIndex, tailIndex)
            else:
                leadArg, startIndex, tailArg, tailIndex, expr, index = self.__findArgs(expr, index)
                result = leadArg + tailArg
                return self.__createSimplifiedExpr(expr, index, result, startIndex, tailIndex)
          
        # expr was just a single number with no operators
        expr = expr.replace("--", "")
        return expr
    
    #================================================
    # returns the left and right arguments to the operator at index
    # also simplifies compound negatives and returns the simplified expression and new operator index after simplification
    def __findArgs(self, expr, index): 
        length = len(expr)
        leadArg, expr, startIndex = self.__getLeadArg(expr, index)
        index -= length - len(expr)
        tailArg, expr, tailIndex = self.__getTailArg(expr, index)
        return leadArg, startIndex, tailArg, tailIndex, expr, index
    
    #================================================
    # replaces an operator and its arguments with the result of evaluating that operator
    def __createSimplifiedExpr(self, expr, index, result, startIndex, tailIndex):
        newString = ""
        
        if startIndex == 0:
            newString = str(result)
        else:
            newString = expr[0 : startIndex] + str(result)
        if tailIndex + 1 < len(expr):
            newString += expr[tailIndex + 1 : len(expr)]
        return newString
         
    #================================================
    # returns the entire number (including a negative sign) to the left of opIndex
    # returns the simplified expression and the index of the start of the left argument
    def __getLeadArg(self, expr, opIndex): 
        length = len(expr)
        startIndex, expr = self.__getLeadArgStartIndex(expr, opIndex)
        opIndex -= length - len(expr)
        return float(expr[startIndex : opIndex]), expr, startIndex
    
    #================================================
    # returns the index within expr of the start of the number (possibly including a negative sign) to the left of opIndex
    # also simplifies double negatives preceding the left argument and returns the simplified expression
    def __getLeadArgStartIndex(self, expr, opIndex): 
        for i in range(1, opIndex):
            if not expr[opIndex - i].isdigit() and expr[opIndex - i] != ".": # if found start of number
                # remove double negatives
                while opIndex - i - 1 >= 0 and expr[opIndex - i] == "-" and expr[opIndex - i - 1] == "-": # while previous two chars are '-'
                    if not (opIndex - i - 2 >= 0 and expr[opIndex - i - 2].isdigit()): # if double negative not preceded by a digit (treat as operator if preceded by digit)
                        expr = str(expr[0 : opIndex - i - 1]) + str(expr[opIndex - i + 1 : len(expr)]) # remove the double negative
                        opIndex -= 2
                        if opIndex - i < 0:
                            i = opIndex
                    else:
                        break # treat the negative as an operator
                        
                # check if the negative is a negative sign or an operator
                if opIndex - i > 0 and expr[opIndex - i - 1].isdigit():
                    return opIndex - i + 1, expr # operator
                else:
                    return opIndex - i, expr # negation
            
        return 0, expr
    
    #================================================
    # returns the entire number (including a leading negative sign) to the right of opIndex
    # returns the simplified expression, and the index of the end of the right argument
    def __getTailArg(self, expr, opIndex): 
        tailIndex, expr = self.__getTailArgEndIndex(expr, opIndex)
        return float(expr[opIndex + 1 : tailIndex + 1]), expr, tailIndex
    
    #================================================
    # returns the index of the end of the number to the right of opIndex
    # simplifies double negatives immediately after the operator and returns the simplified expression
    def __getTailArgEndIndex(self, expr, opIndex): 
        index = 1
        while expr[opIndex + index] == "-" and expr[opIndex + index + 1] == "-":
            expr = str(expr[0 : opIndex + 1]) + str(expr[opIndex + 3 : len(expr)])
            
        for i in range(1, len(expr) - opIndex):
            if not expr[opIndex + i].isdigit() and not (i == 1 and expr[opIndex + i] == "-") and expr[opIndex + i] != ".":
                return opIndex + i - 1, expr # found end of number
            
        return len(expr) - 1, expr
    

                
        
    