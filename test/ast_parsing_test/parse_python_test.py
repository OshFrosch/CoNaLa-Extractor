from src.ast_parsing.parse_python import parse_code_string
import json
import unittest


class MainFileCase(unittest.TestCase):
    def setUp(self) -> None:
        self.snippet = 'import numpy as np\n' \
                  'list = np.array([1,2,3,4])\n' \
                  'reverse_list = list.reverse\n' \
                  'print(list)\n'

    def test_parse_code_string(self):
        ast = parse_code_string(self.snippet)
        ast = json.loads(ast)
        root = ast[0]
        self.assertEqual(type(ast) is list, True)
        self.assertEqual(type(root) is dict, True)
        self.assertEqual(root['type'] == 'Module', True)
        self.assertEqual(len(root['children']) > 0, True)

        for node in ast:
            self.assertEqual('type' in node.keys(), True)
            if 'children' in node.keys():
                children = node['children']
                self.assertEqual(type(children), list)
                for child in children:
                    self.assertEqual(child <= len(ast), True)
                    self.assertEqual(ast[child] is not None, True)
            if 'value' in node.keys():
                self.assertEqual(type(node['value']), str)

    def tearDown(self) -> None:
        self.snippet = ''


if __name__ == '__main__':
    unittest.main()
