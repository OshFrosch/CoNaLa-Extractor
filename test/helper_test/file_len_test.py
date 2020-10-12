from src.helper.file_len import file_len
import unittest
import os


class MainFileCase(unittest.TestCase):
    def setUp(self) -> None:
        self.n = 10
        with open('test.txt', 'w') as f:
            for i in range(self.n):
                f.write('.\n')
        f.close()

    def test_file_len(self):
        k = file_len('test.txt')
        self.assertEqual(k, self.n)

    def tearDown(self) -> None:
        os.remove('test.txt')


if __name__ == '__main__':
    unittest.main()
