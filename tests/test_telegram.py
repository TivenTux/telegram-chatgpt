import unittest
from src import telegram_ai


class TestTelegramBot(unittest.TestCase):
    def test_cleanupname(self):
        '''
        Tests that it can remove special characters from names.
        '''
        data = 'Pangolin&% ! #_-|;;'
        expected = 'Pangolin'
        result = telegram_ai.cleanupname(data)
        self.assertEqual(result, expected)

    def test_withoutname_final_prompt(self):
        '''
        Tests that it can process a prompt without user name.
        '''
        usern = telegram_ai.get_username('WrongData')
        data = 'What is a pangolin?'
        expected = 'Below is a conversation between a user and an AI assistant named Phoenix.\nPhoenix was made by Tiven and provides helpful answers.\nUser: What is a pangolin?\nPhoenix:'
        result = telegram_ai.final_prompt(usern, data)
        self.assertEqual(result, expected)

    def test_withname_final_prompt(self):
        '''
        Tests that it can process a prompt with name.
        '''
        usern = 'George'
        data = 'What is a pangolin?'
        expected = 'Below is a conversation between a user named George and an AI assistant named Phoenix.\nPhoenix was made by Tiven and provides helpful answers.\nGeorge: What is a pangolin?\nPhoenix:'
        result = telegram_ai.final_prompt(usern, data)
        self.assertEqual(result, expected)