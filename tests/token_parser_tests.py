#!/usr/bin/env python

import unittest

import token_parser


class ParserTokenisationCase(unittest.TestCase):

    def setUp(self):
        self.parser = token_parser


    def test_parses_command_1(self):
        
        strg = "add_task: task: Finish project date: 031014"
        tokens = "add_task: task: date:".split()

        response_dict = { "command": "add_task:", "task": "Finish project", "date": "031014"}

        self.assertEqual(self.parser.parse_with_tokens(strg, tokens), response_dict)



if __name__ == "__main__":

    unittest.main()
