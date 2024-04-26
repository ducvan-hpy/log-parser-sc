#! /usr/bin/env python3

from abc import ABC, abstractmethod
import json

class Condition(ABC):
    @abstractmethod
    def is_valid(lc: int, line: str) -> bool:
        pass

    @abstractmethod
    def render(lc: int, line: str) -> str:
        pass

class Multiple5Condition(Condition):
    def is_valid(lc: int, line: str) -> bool:
        return lc % 5 == 0

    def render(lc: int, line: str) -> str:
        return "Multiple de 5"


class ContainsDollarCondition(Condition):
    def is_valid(lc: int, line: str) -> bool:
        return "$" in line

    def render(lc: int, line: str) -> str:
        line = line.replace(" ", "_")
        return line


class DotEndingCondition(Condition):
    def is_valid(lc: int, line: str) -> bool:
        try:
            return line[-1] == "."
        except IndexError:
            return False

    def render(lc: int, line: str) -> str:
        return line


class CurlBracketStartingCondition(Condition):
    def is_valid(lc: int, line: str) -> bool:
        try:
            return line[0] == "{"
        except IndexError:
            return False

    def render(lc: int, line: str) -> str:
        data = json.loads(line)
        data["pair"] = lc % 2 == 0
        return json.dumps(data, ensure_ascii=False)


class DefaultCondition(Condition):
    def is_valid(lc: int, line: str) -> bool:
        return True

    def render(lc: int, line: str) -> str:
        return "Rien à afficher"


CONDITION_CLASSES = [
    Multiple5Condition,
    ContainsDollarCondition,
    DotEndingCondition,
    CurlBracketStartingCondition,
    DefaultCondition,
]

def parse_file(filename: str) -> None:
    lc = 0
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            for cc in CONDITION_CLASSES:
                if cc.is_valid(lc, line):
                    print("{} : {}".format(lc, cc.render(lc, line)))
                    break
            lc += 1


if __name__ == "__main__":
    filename = "data.log"
    parse_file(filename)
