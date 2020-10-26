from src.ast_parsing.parse_python import parse_code_string
from src.preprocessing.preprocess_python import collect_all_and_save
from src.preprocessing.preprocess_python import delim_name
from src.preprocessing.preprocess_python import raw_tree_paths
from src.preprocessing.preprocess_python import collect_sample
import unittest
import json
import os


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.snippet = 'import numpy as np\n' \
                  'list = np.array([1,2,3,4])\n' \
                  'reverse_list = list.reverse\n' \
                  'print(list)\n'
        self.ast = parse_code_string(self.snippet)
        self.ast = json.loads(self.ast)
        self.target = 'ThisIs_theCool_Target_for the Test'
        self.example = [[self.target, self.ast]]

    def test_delim_name(self):
        processed_target = delim_name(self.target)
        self.assertEqual(processed_target.lower(), processed_target)
        self.assertEqual(' ' not in processed_target, True)
        self.assertEqual('|' in processed_target, True)
        self.assertEqual(processed_target.startswith('|'), False)
        self.assertEqual(processed_target.endswith('|'), False)
        self.assertEqual('this|is|the|cool|target|for|the|test', processed_target)

    def test_raw_tree_paths(self):
        paths = raw_tree_paths(self.ast, 0)
        for path in paths:
            self.assertEqual(type(path) is tuple, True)
            self.assertEqual(len(path) == 3, True)
            self.assertEqual(type(path[0]) is str, True)
            self.assertEqual(type(path[2]) is str, True)
            self.assertEqual(type(path[1]) is list, True)
            start_terminal, path_list, end_terminal = path
            self.assertEqual(len(path_list) >= 2, True)
            self.assertEqual(all(type(e) is int for e in path_list), True)
            for node in path_list:
                self.assertEqual(node < len(self.ast), True)
                self.assertEqual(self.ast[node] is not None, True)
            self.assertEqual('value' in self.ast[path_list[0]], True)
            self.assertEqual(self.ast[path_list[0]]['value'], start_terminal)
            self.assertEqual('value' in self.ast[path_list[-1]], True)
            self.assertEqual(self.ast[path_list[-1]]['value'], end_terminal)

    def test_collect_example(self):
        example = collect_sample(self.ast, self.target, 0)
        split = example.split(' ')
        self.assertEqual(split[0], delim_name(self.target))
        self.assertEqual(len(split) >= 2, True)
        self.assertEqual(len(split[1].split(',')), 3)
        self.assertEqual('|' not in split[1].split(',')[0], True)

    def test_collect_all_and_save(self):
        collect_all_and_save(self.example, 'test.txt')
        self.assertEqual(os.path.isfile('test.txt'), True)
        with open('test.txt', 'r') as f:
            for line in f:
                self.assertEqual(collect_sample(self.ast, self.target, 0), line)
        f.close()

        os.remove('test.txt')


if __name__ == '__main__':
    unittest.main()
