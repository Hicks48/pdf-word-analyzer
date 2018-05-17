from PDFTextReader import PDFTextReader
import re


class PDFSentenceReader:

    def __init__(self):
        self.temp_file = None
        self.current_sentence = 0
        self.current_character = 0
        self.total_sentences = 0


    def open(self, pdf_file_path, temp_file_path):
        self._pdf_to_text(pdf_file_path, temp_file_path)
        self.total_sentences = self._calculate_sentences_in_temp_file(temp_file_path)

        self.temp_file = open(temp_file_path, 'r')


    def next(self):
        sentence = []
        current_character = self.temp_file.read(1)
        while current_character and current_character != '.':
            self.current_character += 1
            sentence.append(current_character)
            current_character = self.temp_file.read(1)
        
        self.current_character += 1
        self.current_sentence += 1

        if not current_character:
            return None

        return ''.join(sentence)


    def get_position(self):
        return { 'at-character': self.current_character, 'at-sentence': self.current_sentence, 'total-sentences': self.total_sentences }


    def close(self):
        self.temp_file.close()


    def _calculate_sentences_in_temp_file(self, temp_file_path):
        sentences = 0
        temp_file = open(temp_file_path, 'r')

        character = temp_file.read(1)
        while character:
            if character == '.':
                sentences += 1
            character = temp_file.read(1)

        temp_file.close()
        return sentences


    def _pdf_to_text(self, pdf_file_path, temp_file_path):
        # Write all text as formated to a file
        reader = PDFTextReader(pdf_file_path)
        temp_file = open(temp_file_path, 'w')

        num_pages = reader.get_num_pages()
        for i in range(num_pages):
            temp_file.write(self._get_page_text(i, reader))
        
        temp_file.close()


    def _get_page_text(self, page_index, reader):
        #temp2 = open('./data/temp2.txt', 'a')
        text = reader.extract_page_text(page_index)
        #temp2.write(text)
        #temp2.close()
        return self._format_text(text)


    def all_text_to_single_column(self, text):
        pass


    def _format_text(self, text):
        # Turn text to lower case
        formated = text.lower()

        # Remove all commas
        formated = formated.replace(',', '')

        # Combine senteces broken with linebreaks
        formated = re.sub('\\s*\\-\\s*\n+\\s*', '', formated)
        formated = re.sub('\\s*\n+\\-\\s*', '', formated)

        # Replace all line breaks with spaces
        formated = formated.replace('\n', ' ')

        # Remove consecutive whitespaces and return
        return re.sub(' +', ' ', formated)
