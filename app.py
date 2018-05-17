from PDFSentenceReader import PDFSentenceReader
from WordAnalyzer import WordAnalyzer
from CSVWriter import CSVWriter

import matplotlib.pyplot as plt
import json
import math
import re


def read_keywords(file_path):
    file = open(file_path, 'r')
    keywords = json.loads(file.read())
    return keywords


def analyse_pdf(keywords_file_path, pdf_file_path, temp_file_path):
    reader = PDFSentenceReader()
    reader.open(pdf_file_path, temp_file_path)

    analyzer = WordAnalyzer()
    analysis = analyzer.analyze(read_keywords(keywords_file_path), reader)

    reader.close()
    return analysis


def analyse_ops(keywords_file_path, ops_file_path, math_ops_part_file_path, year):
    print('Analyzing ops ' + ops_file_path + ' and ' + math_ops_part_file_path + '...')

    print('Now analyzing ops ' + ops_file_path)
    math_ops_analysis = analyse_pdf(keywords_file_path, math_ops_part_file_path, './data/math-ops-' + str(year) + '-temp.txt')
    
    print('Now analyzing ops ' + math_ops_part_file_path)
    ops_analysis = analyse_pdf(keywords_file_path, ops_file_path, './data/ops-' + str(year) + '-temp.txt')
    
    print('Analysis for ' + ops_file_path + ' and ' + math_ops_part_file_path + ' done')

    # Return analyze results
    return { ops_file_path: ops_analysis, math_ops_part_file_path: math_ops_analysis }


def write_words_summarry_csv(ops_analyzes, keywords):
    csvWriter = CSVWriter('./data/words.csv', delimiter=';')
    csvWriter.open()

    # Write headers
    headers = ['keyword']
    for analysis in ops_analyzes:
        headers += list(analysis.keys())

    csvWriter.write_row(headers)

    # Collect categories
    categories = {}
    for keyword in keywords:
        category = keywords[keyword]['category']

        if not category in categories:
            categories[category] = []
        
        categories[category].append(keyword)
    
    # Sort keywords by category - alphabets
    category_list = list(categories.keys())
    category_list.sort()

    keyword_list = []
    for category in category_list:
        category_keywords = categories[category]
        category_keywords.sort()
        keyword_list += category_keywords

    # Write data
    for keyword in keyword_list:
        row = []
        for header in headers:
            if header == 'keyword':
                formated = keyword
                formated = re.sub('\\-\n', '', formated)
                formated = formated.replace('\n', ' ')
                row.append(formated)
            else:
                for analysis in ops_analyzes:
                    if header in analysis:
                        row.append(','.join(analysis[header].word_counts[keyword]))
        
        csvWriter.write_row(row)

    csvWriter.close()


def write_csv_summary(ops_analyzes, keywords):
    csvWriter = CSVWriter('./data/summary.csv')
    csvWriter.open()

    # Write headers
    headers = ['keyword']
    for analysis in ops_analyzes:
        headers += list(analysis.keys())
    headers.append('category')

    csvWriter.write_row(headers)

    # Collect categories
    categories = {}
    for keyword in keywords:
        category = keywords[keyword]['category']

        if not category in categories:
            categories[category] = []
        
        categories[category].append(keyword)
    
    # Sort keywords by category - alphabets
    category_list = list(categories.keys())
    category_list.sort()

    keyword_list = []
    for category in category_list:
        category_keywords = categories[category]
        category_keywords.sort()
        keyword_list += category_keywords

    # Write data
    for keyword in keyword_list:
        row = []
        for header in headers:
            if header == 'keyword':
                formated = keyword
                formated = re.sub('\\-\n', '', formated)
                formated = formated.replace('\n', ' ')
                row.append(formated)
            elif header == 'category':
                row.append(keywords[keyword]['category'])
            else:
                for analysis in ops_analyzes:
                    if header in analysis:
                        row.append(len(analysis[header].word_counts[keyword]))
        
        csvWriter.write_row(row)
    
    csvWriter.close()


if __name__ == '__main__':
    ops_2004_analysis = analyse_ops('./data/keywords.json', './data/ops-2004.pdf', './data/math-ops-2004.pdf', 2004)
    ops_2014_analysis = analyse_ops('./data/keywords.json', './data/ops-2014.pdf', './data/math-ops-2014.pdf', 2014)

    write_csv_summary([ops_2004_analysis, ops_2014_analysis], read_keywords('./data/keywords.json'))
    write_words_summarry_csv([ops_2004_analysis, ops_2014_analysis], read_keywords('./data/keywords.json'))
