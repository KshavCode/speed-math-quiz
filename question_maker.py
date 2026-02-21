import random
from fractions import Fraction

def question_maker() :
    operator_list = ["+", "-", "*", "/"]
    operator = random.choice(operator_list)
    if operator == "+" :
        a, b = random.randint(1, 21), random.randint(1, 21)
        correct_answer = a + b
        options = [correct_answer-random.randint(1, 4), correct_answer+random.randint(1,4), correct_answer]
        random.shuffle(options)
    elif operator == "-" :
        a, b = random.randint(1, 21), random.randint(1, 11)
        while a<b :
            a, b = random.randint(1, 21), random.randint(1, 11)
        correct_answer = a - b
        options = [correct_answer-random.randint(1, 4), correct_answer+random.randint(1,4), correct_answer]
        random.shuffle(options)
    elif operator == "*" :
        a, b = random.randint(1, 16), random.randint(1, 11)
        correct_answer = a * b
        options = [correct_answer-random.randint(1, 4), correct_answer+random.randint(1,4), correct_answer]
        random.shuffle(options)
    elif operator == "/" :
        a, b = random.randint(2, 101), random.randint(2, 6)
        while a < b or a % b != 0: 
            a, b = random.randint(2, 101), random.randint(2, 6)
        correct_answer = int(Fraction(a, b))  
        options = [
            int(correct_answer + Fraction(random.randint(1, 4), 1)), 
            int(correct_answer - Fraction(random.randint(1, 4), 1)), 
            correct_answer
            ]
        random.shuffle(options)
    return (f"{a} {operator} {b} =", options, correct_answer)


if __name__ == "__main__" :
    for i in range(5000) :
        print(question_maker())
    
            
    
        
        
        