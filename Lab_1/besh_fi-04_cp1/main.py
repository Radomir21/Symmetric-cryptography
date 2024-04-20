from lib import TextAnalyzer, FileReader, Preprocessor, NGramCounter

FILENAME = "reference.txt"

if __name__ == "__main__":
    file_reader = FileReader(FILENAME)
    preprocessor = Preprocessor()
    ngram_counter = NGramCounter()
    analyzer = TextAnalyzer(file_reader, preprocessor, ngram_counter)
     #Process text
    (
        char_frequencies,
        bigram_frequencies,
        bigram_frequencies_no_intersect,
    ) = analyzer.analyze()
     #Show results
    analyzer.print_frequencies(char_frequencies)
    analyzer.print_bigram_frequencies(char_frequencies, bigram_frequencies)
    analyzer.print_entropy(char_frequencies, bigram_frequencies, bigram_frequencies_no_intersect)
    #------------------------------------------------------------------------------------------------#
    