import re

from bs4 import BeautifulSoup
import requests

from wiktionaryparserru.utils import ResponseCode, STATUSES


class WiktionaryParser:
    MISSING_SYMBOL = "—"
    SEMANTICS_SPLIT_SYMBOL = "◆"
    SEMANTICS_ID = "Семантические_свойства"
    MORPHOLOGY_ID = "Морфологические_и_синтаксические_свойства"

    def __init__(self) -> None:
        self.result = dict()
        self.url = "https://ru.wiktionary.org/w/index.php?title={}"

    def _set_morphology(self, soup: BeautifulSoup) -> None:
        morph_title = soup.find(id=self.MORPHOLOGY_ID)
        morph_text = morph_title.find_next("p").find_next("p").get_text()
        morph_text = "".join(re.findall("[-0-9А-яё.,! ]+", morph_text))
        self.result["morphology"] = morph_text

    def _set_definitions(self, soup: BeautifulSoup) -> None:
        self.result["definitions"] = list()
        semantic_title = soup.find(id=self.SEMANTICS_ID)
        definition_text = semantic_title.find_next("ol")

        for item in definition_text.find_all("li"):
            text = item.get_text()
            if text:
                text = "".join(re.findall("[-◆А-яё.,! ]+", text))
                text_split = text.split(self.SEMANTICS_SPLIT_SYMBOL)
                self.result["definitions"].append({
                    "value": text_split[0].strip(),
                    "example": text_split[1].strip()
                })

    def _set_synonyms(self, soup: BeautifulSoup) -> None:
        self.result["synonyms"] = list()
        semantic_title = soup.find(id=self.SEMANTICS_ID)
        synonyms_text = semantic_title.find_next("ol").find_next("ol")

        for item in synonyms_text.find_all("li"):
            text = " ".join(re.findall("[-0-9А-яё.,! ]+", item.get_text())).strip()
            if text and text != self.MISSING_SYMBOL:
                self.result["synonyms"].append(text)

    def _set_antonyms(self, soup: BeautifulSoup) -> None:
        self.result["antonyms"] = list()
        semantic_title = soup.find(id=self.SEMANTICS_ID)
        synonyms_text = semantic_title.find_next("ol").find_next("ol").find_next("ol")

        for item in synonyms_text.find_all("li"):
            text = " ".join(re.findall("[-0-9А-яё.,! ]+", item.get_text())).strip()
            if text and text != self.MISSING_SYMBOL:
                self.result["antonyms"].append(text)

    def process_html_page(self, page: str) -> dict:
        soup = BeautifulSoup(page, features="html.parser")
        self._set_morphology(soup)
        self._set_definitions(soup)
        self._set_synonyms(soup)
        self._set_antonyms(soup)
        return self.result

    def make_request(self, word: str) -> dict:
        response = requests.get(self.url.format(word))
        if response.status_code == ResponseCode.SUCCESS.value:
            return self.process_html_page(response.text)
        # might throw exception if code is missing
        self.result = {**self.result, **STATUSES[response.status_code]}
        return self.result
