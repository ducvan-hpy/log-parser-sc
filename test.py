#! /usr/bin/env python3

import unittest

from parser import (
    Multiple5Condition,
    ContainsDollarCondition,
    DotEndingCondition,
    CurlBracketStartingCondition,
    DefaultCondition,
    compute_line,
)

class TestParser(unittest.TestCase):
    def test_multiple_5(self):
        testcases = [
            (0, True),
            (1, False),
            (5, True),
            (10, True),
            (11, False),
        ]

        for lc, expected in testcases:
            self.assertEqual(Multiple5Condition.is_valid(lc, ''), expected)

    def test_dollar(self):
        testcases = [
            ('', False),
            ('$', True),
            ('abc $ def', True),
            ('abc def', False),
        ]

        for line, expected in testcases:
            self.assertEqual(ContainsDollarCondition.is_valid(0, line), expected)

    def test_dot(self):
        testcases = [
            ('.', True),
            ('a.b', False),
            ('', False),
            ('ab c.', True),
        ]

        for line, expected in testcases:
            self.assertEqual(DotEndingCondition.is_valid(0, line), expected)

    def test_json(self):
        testcases = [
            ('{', True),
            ('{abc}', True),
            ('a{b', False),
            ('', False),
            ('}', False),
        ]

        for line, expected in testcases:
            self.assertEqual(CurlBracketStartingCondition.is_valid(0, line), expected)

    def test_default(self):
        testcases = [
            ((0, 'Match 756 has started'), True),
            ((5, ''), True),
            ((10, 'line 10'), True),
            ((11, 'line 11'), True),
        ]

        for (lc, line), expected in testcases:
            self.assertEqual(DefaultCondition.is_valid(lc, line), expected)

    def test_renders(self):
        # ((lc, line), expected)
        testcases = [
            ((0, 'Match 42 has started'), 'Multiple de 5'),
            ((1, '{"player": {"first_name": "Json", "Age": 42}, "team": "Python"}'),
             '{"player": {"first_name": "Json", "Age": 42}, "team": "Python", "pair": false}'),
            ((2, '{"player": {"first_name": "Even", "Age": 24}, "team": "Pair"}'),
             '{"player": {"first_name": "Even", "Age": 24}, "team": "Pair", "pair": true}'),
            ((3, ''), 'Rien à afficher'),
            ((4, 'Dollar suc$esfully run'), 'Dollar_suc$esfully_run'),
            ((6, '{"player": {"first_name": "Dot", "Age": 42}, "team": "Python"}.'),
             '{"player": {"first_name": "Dot", "Age": 42}, "team": "Python"}.'),
        ]

        for (lc, line), expected in testcases:
            self.assertEqual(compute_line(lc, line), expected)


if __name__ == '__main__':
    unittest.main()
