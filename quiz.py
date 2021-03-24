from collections import namedtuple
from enum import Enum
import operator
from random import randint

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
}


class OpsEnum(Enum):
    """
    ENUM to hold the allowed values for operator
    """

    ADD: str = "+"
    SUBTRACT: str = "-"
    MULTIPLY: str = "*"
    DIVIDE: str = "/"
    MOD: str = "%"


Question = namedtuple("Question", ["q", "a", "s"])


class Quiz:
    def __init__(self, base: int, high: int = 9, operation: OpsEnum = "+"):
        self.base = base
        self.high = high
        self.op = operation
        self.__questions = [
            Question(q=f"{str(base)} {operation} {o} =", a=ops[operation](base, o), s=0)
            for o in range(high + 1)
        ]

    def __iter__(self):
        self.__active_idx = None
        return self

    def __next__(self):
        if self.__questions:
            self.__active_idx = randint(0, len(self.__questions) - 1)
            return self.__questions[self.__active_idx].q
        else:
            print(
                f"You mastered everything from {self.base} {self.op} 0 to {self.base} {self.op} {self.high}."
            )
            raise StopIteration

    def answer(self, resp: str):
        if self.__active_idx is not None:
            q = self.__questions[self.__active_idx]
            if int(resp) == q.a:
                print("Correct!")
                if q.s + 1 == 2:
                    _ = self.__questions.pop(self.__active_idx)
                else:
                    self.__questions[self.__active_idx] = Question(q.q, q.a, q.s + 1)
            else:
                print("Try Again!")
                self.__questions[self.__active_idx] = Question(q.q, q.a, 0)

            self.__active_idx = None

        else:
            raise Exception(
                "Previous question has been answered. Request another question before answering again."
            )


def ask_question(question: str, correct: bool = True) -> str:
    base, op, o = question.split()[:3]
    resp = ops[op](int(base), int(o))

    if randint(0, 1):
        resp += 1

    return resp


if __name__ == "__main__":
    quiz = Quiz(base=2, high=3)

    for question in quiz:
        resp = ask_question(question)
        print(question, resp)
        quiz.answer(resp)