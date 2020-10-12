from src.ast_parsing.clean_intent import clean_intent
import unittest


class MainFileCase(unittest.TestCase):
    def setUp(self) -> None:
        self.intent = 'pandas: How can I split a pandas /df/ into halfes?'

    def test_collect_examples(self):
        cleaned_intent = clean_intent(self.intent)
        self.assertEqual('split a pandas df into halfes', cleaned_intent)

    def tearDown(self) -> None:
        self.intent = ''


if __name__ == '__main__':
    unittest.main()
