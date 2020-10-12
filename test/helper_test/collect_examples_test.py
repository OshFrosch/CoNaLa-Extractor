from src.helper.collect_examples import collect_examples
from src.ast_parsing.parse_python import parse_code_string
import unittest
import os


class MainFileCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ast = parse_code_string('print("Hi")')
        with open('test.json', 'w') as f:
            for i in range(20):
                if i % 2 == 0:
                    f.write('target\n')
                else:
                    f.write(self.ast + '\n')
        f.close()

    def test_collect_examples(self):
        examples = collect_examples('test.json')
        self.assertEqual(len(examples), 10)
        self.assertEqual(type(examples), list)
        self.assertEqual(len(examples[0]), 2)
        self.assertEqual(type(examples[0]), list)
        self.assertEqual(examples[0][0], 'target')
        self.assertEqual(type(examples[0][1]), list)

    def tearDown(self) -> None:
        os.remove('test.json')


if __name__ == '__main__':
    unittest.main()
