from tqdm import tqdm


class WordAnalyzer:

    def __init__(self):
        self.current_analysis = None


    def analyze(self, keywords, sentence_iterator):
        self._initialize_analysis(keywords)

        with tqdm(total = sentence_iterator.get_position()['total-sentences']) as pbar:
            current_sentence = sentence_iterator.next()
            while current_sentence is not None:
                position = sentence_iterator.get_position()
                pbar.update(1)

                self._analyze_sentence(current_sentence, keywords, position['at-character'])
                current_sentence = sentence_iterator.next()
            
            pbar.clear()

        return self.current_analysis


    def _initialize_analysis(self, keywords):
        tqdm.monitor_interval = 0

        self.current_analysis = Analysis()
        for keyword in keywords:
            self.current_analysis.word_counts[keyword] = []


    def _analyze_sentence(self, sentence, keywords, global_index):
        used_keywords = self._get_used_keywords(sentence, keywords, global_index)
        
        self._update_word_counts(used_keywords)
        #self._update_used_together(used_keywords)

    
    def _update_word_counts(self, used_keywords):
        for keyword in used_keywords:
            self.current_analysis.word_counts[keyword] += used_keywords[keyword]


    def _get_used_keywords(self, sentence, keywords, global_index):
        used_keywords = {}

        words = sentence.split(' ')
        for i in range(len(words)):
            for keyword in keywords:
                local_index = self._is_keyword_used(keyword, keywords, words, i)
                if local_index:
                    if keyword not in used_keywords:
                        used_keywords[keyword] = []

                    word = ' '.join(words[local_index[0]:local_index[1]])
                    used_keywords[keyword].append(word)
        
        return used_keywords

    
    def _update_used_together(self, used_keywords):
        self.current_analysis.used_together.append(used_keywords)
    

    def _is_keyword_used(self, keyword, keywords, words, word_index):
        synonyms = keywords[keyword]['synonymes']

        for synonym in synonyms:
            index = self._is_synonym_used(synonym, words, word_index)
            if index:
                return index
        
        return None

    
    def _is_synonym_used(self, synonym, words, word_index):
        synonym_parts = synonym.split(' ')
        for i in range(len(synonym_parts)):
            if word_index + i >= len(words) or synonym_parts[i] not in words[word_index + i]:
                return None
        
        return [word_index, word_index + len(synonym_parts)]


class Analysis:
    
    def __init__(self):
        self.word_counts = {}
        self.used_together = []
