import PyPDF2
import pdftotext
import re


class PDFTextReader:

    def __init__(self, file_path):
        pypdf2_reader = PyPDF2Reader(file_path)
        pdftotext_reader = PDFToTextReader(file_path)

        self.readers = [pypdf2_reader, pdftotext_reader]
        

    def get_num_pages(self):
        num_of_pages = 0

        for reader in self.readers:
            pages = reader.get_num_pages()
            if pages > num_of_pages:
                num_of_pages = pages
        
        return num_of_pages


    def extract_page_text(self, page_index):
        best_extract = ''

        for reader in self.readers:
            extract = reader.extract_page_text(page_index)
            current_best_score, current_score = self._score_extracts(best_extract, extract)

            if current_score > current_best_score:
                best_extract = extract
                
        return best_extract


    def _score_extracts(self, extract1, extract2):
        columns1 = self._calculate_columns(extract1) + 1
        columns2 = self._calculate_columns(extract2) + 1

        lenght1 = self._calculate_lenght(extract1) + 1
        lenght2 = self._calculate_lenght(extract2) + 1

        max_length = max([lenght1, lenght2])
        max_columns = max([columns1, columns2])

        score1 = (1.1 - columns1 / max_columns) * (lenght1 / max_length)
        score2 = (1.1 - columns2 / max_columns) * (lenght2 / max_length)

        #print('len1 ' + str(lenght1) + ' len2 ' + str(lenght2))
        #print('cols1 ' + str(columns1) + ' cols2 ' + str(columns2))
        #print('s2: ' + str(score2) + ' s1: ' + str(score1))

        return score1, score2

    
    def _calculate_lenght(self, extract):
        return len(re.sub('\\s+', '', extract))


    def _calculate_columns(self, extract):
        columns = 0
        for line in extract.split('\n'):
            columns += self._countnonoverlappingrematches('\\s{3,}', line.strip())
        return columns


    def _countnonoverlappingrematches(self, pattern, thestring):
        return re.subn(pattern, '', thestring)[1]



class PyPDF2Reader:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract_page_text(self, page_index):
        with open(self.file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfFileReader(pdf_file)
            return reader.getPage(page_index).extractText()
    
    def get_num_pages(self):
        with open(self.file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfFileReader(pdf_file)
            return reader.getNumPages()


class PDFToTextReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract_page_text(self, page_index):
        with open(self.file_path, 'rb') as pdf_file:
            pdf = pdftotext.PDF(pdf_file)
            return pdf[page_index]
    
    def get_num_pages(self):
        with open(self.file_path, 'rb') as pdf_file:
            pdf = pdftotext.PDF(pdf_file)
            return len(pdf)
