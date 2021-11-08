import json
import os
import unittest

from wiktionaryparserru.parser import WiktionaryParser
from wiktionaryparserru.utils import ResponseCode

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class TestParser(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        self.parser = WiktionaryParser()
        with open(os.path.join(__location__, "responses.json"), "r", encoding="utf-8") as file:
            self.expected_responses = json.load(file)
        super().__init__(*args, **kwargs)

    def test_regular_words(self):
        html_files = [f for f in os.listdir(os.path.join(__location__, "html_pages"))]
        for html_file in html_files:
            file_name = html_file.split(".")[0]
            file_path = os.path.join(__location__, "html_pages", html_file)
            with open(file_path, "r", encoding="utf-8") as file:
                page_data = file.read()
            response = self.parser.process_html_page(page_data)
            expected_response = self.expected_responses[file_name]
            assert response == expected_response
