import math
import pprint
from typing import Dict
from collections import defaultdict


CHARSET_RU = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
class FileReader:
    def __init__(self, filename: str, encoding: str = "utf-8"):
        self.filename = filename
        self.encoding = encoding

    def read(self) -> str:
        with open(self.filename, "r", encoding=self.encoding) as file:
            return file.read()


class Preprocessor:
    @staticmethod
    def preprocess(char: str) -> str:
        if "а" <= char <= "я" or "А" <= char <= "Я":
            return char.lower()
        elif char in {"Ё", "ё"}:
            return "е"
        else:
            return " "

    @classmethod
    
    def format(cls, text: str, no_space: bool=False) -> str:
        #formatted = "".join([cls.preprocess(char) for char in text if char != ' ' ])
        formatted = "".join([cls.preprocess(char) for char in text])
        text = text.replace(' ', '') if no_space else text
        text = ' '.join(text.split())
        cleaned_text = " ".join(formatted.split())
        return cleaned_text


class NGramCounter:
    @staticmethod
    def count(text: str, ngram: int = 1, intersection: bool = True) -> Dict[str, int]:
        counter = defaultdict(int)
        step = 1 if intersection else ngram
        for i in range(0, len(text) - ngram + 1, step):
            ngram_str = text[i : i + ngram]
            counter[ngram_str] += 1
        result = dict(sorted(counter.items()))
        return result


class TextAnalyzer:
    def __init__(
        self,
        file_reader: FileReader,
        preprocessor: Preprocessor,
        ngram_counter: NGramCounter,
    ):
        self.file_reader = file_reader
        self.preprocessor = preprocessor
        self.ngram_counter = ngram_counter
        self.text = self.file_reader.read()

    #def analyze(self):
        #formatted_text = self.preprocessor.format(self.text)
        #char_frequencies = self.ngram_counter.count(formatted_text)
        #bigram_frequencies = self.ngram_counter.count(formatted_text, ngram=2)
        #bigram_frequencies_no_intersect = self.ngram_counter.count(
        #formatted_text, ngram=2, intersection=False
        #)
        #return char_frequencies, bigram_frequencies, bigram_frequencies_no_intersect


    def analyze(self):
        formatted_text = self.preprocessor.format(self.text, no_space=True)
        char_frequencies = self.ngram_counter.count(formatted_text, intersection=False)
        bigram_frequencies = self.ngram_counter.count(formatted_text, ngram=2)
        bigram_frequencies_no_intersect = self.ngram_counter.count(
            formatted_text, ngram=2, intersection=False
        )
        return char_frequencies, bigram_frequencies, bigram_frequencies_no_intersect

    def sum_entropy(self, data):
        amount = sum(data.values())
        t = [data[k] / amount for k in data.keys()]
        return -sum(a * math.log2(a) for a in t)

    @staticmethod
    def print_frequencies(frequencies: Dict[str, int]) -> None:
        total_symbols = sum(frequencies.values())
        freq_dict = {}
        for symbol, count in frequencies.items():
            frequency = round(count / total_symbols, 4)
            freq_dict[symbol] = frequency
        pprint.pprint(freq_dict)

    @staticmethod
    def print_bigram_frequencies(
        char_frequencies: Dict[str, int], bigram_frequencies: Dict[str, int]
    ) -> None:
        total_bigrams = sum(bigram_frequencies.values())
        alphabet = list(char_frequencies.keys())
        bigram_freq_matrix = {}

        for left_char in alphabet:
            row = {}
            for right_char in alphabet:
                key = f"{left_char}{right_char}"
                frequency = bigram_frequencies.get(key, 0) / total_bigrams
                row[right_char] = f"{frequency:2.2e}" if frequency else f"{0:8d}"
            bigram_freq_matrix[left_char] = row

        pprint.pprint(bigram_freq_matrix)

    #def print_entropy(
        #self, char_frequencies, bigram_frequencies, bigram_frequencies_no_intersect
    #):
        #H1 = self.sum_entropy(char_frequencies)
        #H2=self.sum_entropy(char_frequencies)
        #H2_intersect = self.sum_entropy(bigram_frequencies) / 2
        #H2_no_intersect = self.sum_entropy(bigram_frequencies_no_intersect) / 2
        #entropy_values = {
            #"H1": H1, 
            #"H2_with_intersection": H2_intersect,
            #"H2_without_intersection": H2_no_intersect, 
        #}
        #pprint.pprint(entropy_values)

    def print_entropy(
        self, char_frequencies, bigram_frequencies, bigram_frequencies_no_intersect
    ):
        H1 = self.sum_entropy(char_frequencies)
        H2_intersect = self.sum_entropy(bigram_frequencies) / 2
        H2_no_intersect = self.sum_entropy(bigram_frequencies_no_intersect) / 2
        entropy_values = {
            "H1": H1,
            "H2_with_intersection": H2_intersect,
            "H2_without_intersection": H2_no_intersect,
        }
        pprint.pprint(entropy_values)
