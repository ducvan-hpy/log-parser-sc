#! /usr/bin/env python3

import json

class Multiple5Condition:
    def is_valid(lc : int, line : str) -> bool:
        return lc % 5 == 0

    def render(lc : int, line : str) -> None:
        print("{} : Multiple de 5".format(lc))


class ContainsDollarCondition:
    def is_valid(lc : int, line : str) -> bool:
        return "$" in line

    def render(lc : int, line : str) -> None:
        line = line.replace(" ", "_")
        print("{} : {}".format(lc, line))


class DotEndingCondition:
    def is_valid(lc : int, line : str) -> bool:
        try:
            return line[-1] == "."
        except IndexError:
            return False

    def render(lc : int, line : str) -> None:
        print("{} : {}".format(lc, line))


class CurlBracketStartingCondition:
    def is_valid(lc : int, line : str) -> bool:
        try:
            return line[0] == "{"
        except IndexError:
            return False

    def render(lc : int, line : str) -> None:
        data = json.loads(line)
        data["pair"] = lc % 2 == 0
        print("{} : {}".format(lc, json.dumps(data, ensure_ascii=False)))


class DefaultCondition:
    def is_valid(lc : int, line : str) -> bool:
        return True

    def render(lc : int, line : str) -> None:
        print("{} : Rien à afficher".format(lc))


if __name__ == "__main__":
    condition_classes = [
        Multiple5Condition,
        ContainsDollarCondition,
        DotEndingCondition,
        CurlBracketStartingCondition,
        DefaultCondition,
    ]

    filename = "data.log"

    lc = 0

    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            for cc in condition_classes:
                if cc.is_valid(lc, line):
                    cc.render(lc, line)
                    break
            lc += 1
