from typing import List, Generator
from enum import Enum
from abc import ABC, abstractmethod

def get_id() -> Generator[int]:
    i = 1
    while True:
        yield i
        i += 1
        
id = get_id()

class ANSWER(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"

class Question(ABC):
    def __init__(self, description: str, points_awarded=1) -> None:
        self._description = ""
        self._points_awarded = 1
        
        self.description = description
        self.points_awarded = points_awarded

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        if not value.strip():
            raise ValueError("Description cannot be empty")
        self._description = value.strip()

    @property
    def points_awarded(self) -> int:
        return self._points_awarded

    @points_awarded.setter
    def points_awarded(self, value: int) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Points must be a number")
        if value <= 0:
            raise ValueError("Points must be greater than 0")
        self._points_awarded = int(value)
        
    @abstractmethod
    def check_answer(self, answer: str) -> bool:
        pass

    def __str__(self) -> str:
        return f"""
            Question: {self.description}
            Points: {self.points_awarded}
            """
            
class MultipleChoiceQuestion(Question):
    def __init__(self, description: str, a: str, b: str, c: str, d: str, correct_answer: ANSWER, points_awarded=1) -> None:
        super().__init__(description, points_awarded)
        self._a = ""
        self._b = ""
        self._c = ""
        self._d = ""
        self._correct_answer = ANSWER.A
        
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.correct_answer = correct_answer
        
    @property
    def a(self) -> str:
        return self._a

    @a.setter
    def a(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Option A must be a string")
        if not value.strip():
            raise ValueError("Option A cannot be empty")
        self._a = value.strip()

    @property
    def b(self) -> str:
        return self._b

    @b.setter
    def b(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Option B must be a string")
        if not value.strip():
            raise ValueError("Option B cannot be empty")
        self._b = value.strip()

    @property
    def c(self) -> str:
        return self._c

    @c.setter
    def c(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Option C must be a string")
        if not value.strip():
            raise ValueError("Option C cannot be empty")
        self._c = value.strip()

    @property
    def d(self) -> str:
        return self._d

    @d.setter
    def d(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Option D must be a string")
        if not value.strip():
            raise ValueError("Option D cannot be empty")
        self._d = value.strip()

    @property
    def correct_answer(self) -> ANSWER:
        return self._correct_answer

    @correct_answer.setter
    def correct_answer(self, value: ANSWER) -> None:
        if not isinstance(value, ANSWER):
            raise TypeError("Correct answer must be an ANSWER enum")
        self._correct_answer = value
        
    def check_answer(self, answer: str) -> bool:
        return self._correct_answer == answer

class Quiz:
    def __init__(self, title: str, description="") -> None:
        self._questions: List[Question] = []
        self._title = ""
        self._description = ""
        self._id = next(id)
        self._history: List[int] = []
        
        self.title = title
        self.description = description
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value: str):
        if value.strip() == "":
            raise TypeError("Can't be empty")
        
        self._title = value
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value
        
    @property
    def average_score(self) -> float:
        if self._history:
            return sum(self._history) / len(self._history)
        
        print("Quiz hasn't been taken yet")
        return 0.0
    
    @property
    def times_taken(self) -> int:
        return len(self._history)
    
    @property
    def id(self) -> int:
        return self._id
        
    def add_question(self, question: Question):
        if not isinstance(question, Question):
            raise TypeError("Make sure you pass a Question")
        self._questions.append(question)
    
    def remove_question(self, question: Question):
        if not isinstance(question, Question):
            raise TypeError("Make sure you pass a Question")
        if question not in self._questions:
            raise ValueError("Question doesn't exist")
        
        self._questions.remove(question)
    
    def take_quiz(self):
        total = 0
        
        for question in self._questions:
            print(f"{question.description} ({question.points_awarded} point(s))")
            print(f"a) {question.a}")
            print(f"b) {question.b}")
            print(f"c) {question.c}")
            print(f"d) {question.d}")
            
            answer = input("Pick an answer (a to d) ")
            while answer.lower() not in [e.value for e in ANSWER]:
                answer = input("Make sure you pick one of a, b, c or d ")
                
            if answer.lower() == question.correct_answer.value:
                total += question.points_awarded
                
        print(f"Your score: {total}")
        self._history.append(total)
    
class QuizManager:
    def __init__(self) -> None:
        self._quizzes: List[Quiz] = []
        
    def get_stats(self):
        if self._quizzes:
            average_of_all_quizzes = sum(quiz.average_score for quiz in self._quizzes) / len(self._quizzes)
            print(f"Average across all quizzes is {average_of_all_quizzes}")
            
            times_all_quizzes_taken = sum(quiz.times_taken for quiz in self._quizzes)
            print(f"All quizzes times taken: {times_all_quizzes_taken}")

    def add_quiz(self, quiz: Quiz):
        self._quizzes.append(quiz)
    
    def remove_quiz(self, quiz_id: int):
        found_quiz = next((quiz for quiz in self._quizzes if quiz.id == quiz_id), None)
        
        if found_quiz:
            self._quizzes.remove(found_quiz)
        else:
            print("Quiz not found")
    
    def show_all_quizzes(self):
        for quiz in self._quizzes:
            print(f"{quiz.id} - {quiz.title}")
            
        print("-----------------------------")
    
    def take_quiz(self, quiz_id: int):
        found_quiz = next((quiz for quiz in self._quizzes if quiz.id == quiz_id), None)
        
        if found_quiz:
            found_quiz.take_quiz()
        else:
            print("Quiz not found")
            
# Create quiz manager
quiz_manager = QuizManager()

# Quiz 1 - Python Basics
python_basics = Quiz("Python Basics")
python_basics.add_question(MultipleChoiceQuestion(
    "What is the correct way to create a variable in Python?",
    "var name = value", 
    "variable = value",
    "set name = value",
    "name := value",
    ANSWER.B
))
python_basics.add_question(MultipleChoiceQuestion(
    "Which of these is NOT a Python data type?",
    "int",
    "str", 
    "char",
    "bool",
    ANSWER.C
))
python_basics.add_question(MultipleChoiceQuestion(
    "What symbol is used for comments in Python?",
    "#",
    "//",
    "/* */",
    "--",
    ANSWER.A
))
python_basics.add_question(MultipleChoiceQuestion(
    "How do you create a list in Python?",
    "array()",
    "{1, 2, 3}",
    "(1, 2, 3)",
    "[1, 2, 3]",
    ANSWER.D
))
python_basics.add_question(MultipleChoiceQuestion(
    "Which method is used to add an item to a list?",
    "append()",
    "add()",
    "insert()",
    "push()",
    ANSWER.A
))

# Quiz 2 - Programming Concepts
programming_concepts = Quiz("Programming Concepts")
programming_concepts.add_question(MultipleChoiceQuestion(
    "What is encapsulation?",
    "Bundling data and methods that work on that data within a single unit",
    "Converting data types",
    "Creating multiple instances of a class",
    "Breaking down a problem into smaller parts",
    ANSWER.A
))
programming_concepts.add_question(MultipleChoiceQuestion(
    "What is inheritance in OOP?",
    "Creating multiple objects",
    "A mechanism that allows a class to inherit properties from another class",
    "Hiding implementation details",
    "Method overloading",
    ANSWER.B
))
programming_concepts.add_question(MultipleChoiceQuestion(
    "What is a constructor?",
    "A method to destroy objects",
    "A method to compare objects",
    "A special method that creates new objects",
    "A method to convert data types",
    ANSWER.C
))
programming_concepts.add_question(MultipleChoiceQuestion(
    "What is polymorphism?",
    "Writing secure code",
    "Creating multiple classes",
    "Having multiple constructors",
    "The ability to present the same interface for different underlying forms",
    ANSWER.D
))
programming_concepts.add_question(MultipleChoiceQuestion(
    "What is abstraction?",
    "Hiding complex implementation details and showing only functionality",
    "Creating abstract classes",
    "Converting concrete classes to interfaces",
    "Method overriding",
    ANSWER.A
))

# Quiz 3 - Data Structures
data_structures = Quiz("Data Structures")
data_structures.add_question(MultipleChoiceQuestion(
    "What is a stack?",
    "LIFO data structure",
    "FIFO data structure",
    "Random access structure",
    "Tree structure",
    ANSWER.A
))
data_structures.add_question(MultipleChoiceQuestion(
    "What is a queue?",
    "Random access structure",
    "FIFO data structure",
    "Tree structure",
    "LIFO data structure",
    ANSWER.B
))
data_structures.add_question(MultipleChoiceQuestion(
    "Which data structure uses nodes?",
    "Array",
    "Stack",
    "Linked List",
    "Queue",
    ANSWER.C
))
data_structures.add_question(MultipleChoiceQuestion(
    "What is the time complexity of binary search?",
    "O(n)",
    "O(n²)",
    "O(n log n)",
    "O(log n)",
    ANSWER.D
))
data_structures.add_question(MultipleChoiceQuestion(
    "Which is a non-linear data structure?",
    "Tree",
    "Array",
    "Stack",
    "Queue",
    ANSWER.A
))

# Add quizzes to quiz manager
quiz_manager.add_quiz(python_basics)
quiz_manager.add_quiz(programming_concepts)
quiz_manager.add_quiz(data_structures)

while True:
    print("1. Show all quizzes")
    print("2. Take a quiz")
    print("3. See stats")
    print("4. Exit")

    action = input("Choose an action ")
    while action not in ("1", "2", "3", "4"):
        action = input("Choose a value between 1 and 4 ")
        
    if action == "1":
        quiz_manager.show_all_quizzes()
        
    if action == "2":
        while True:
            try:
                quiz_id = int(input("Which quiz do you want to take? "))
                break
            except:
                print("Enter a number id")
        
        quiz_manager.take_quiz(int(quiz_id))
        
    if action == "3":
        quiz_manager.get_stats()
        
    if action == "4":
        break