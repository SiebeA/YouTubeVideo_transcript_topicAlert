
"""
    - Also return the surrounding words of the match
    - Frequency dict without stop words
    - Frequency NER
    - Corpus: each video is a seperate file, then TFIDF analysis
"""

import os, glob, pickle
print(os.getcwd())
os.chdir("C:\\Users\\siebe\\GD\\Engineering\\.Python\\")
for f in glob.glob('*.txt'): print(f)

with open("outputFile_Sam Harris_2021-07-09_2015-08-12.txt",encoding='utf8') as file:
    a_strings_transcripts = file.read()


#%%=======================#
'            REGEX return episode where a key word was mentioned:                 '
#========================= #
import re
wordOfInterest = 'suffer'
regex = r"(\d{{4}}-\d+-\d+\n.+\n.+)\n\n.+(?={})".format(wordOfInterest) #this regex returns the first match (in first parantheses: title, date, id)c of the 2nd match (2nd parenthesis) 
matches = re.findall(regex, a_strings_transcripts) #it returns the date and title 
for i in matches: print(i,'\n')

# =============================================================================
# #match the context of the pattern
# =============================================================================

wordOfInterestψContext = r"(.{{200}})({})(\s.{{200}})".format(wordOfInterest)

matches = re.findall(wordOfInterestψContext, a_strings_transcripts)
for match in matches: print(match,'\n')
#TODO  integrate

# matching a group of the pattern:
for match in re.finditer(wordOfInterestψContext, a_strings_transcripts):
    print(match.group(2))


matches_list = []


#TODO NER counter
'''
from collections import Counter
labels = [ent.label_ for ent in doc.ents]
Counter(labels)
'''


#%%=======================#
'            NLP                '
#========================= #

import spacy
# set up a pipeline with the name "nlp"
nlp = spacy.load("en_core_web_sm")

import spacy



doc= nlp(a_strings_transcripts)
spacy_stoptokens = spacy.lang.en.stop_tokens.STOP_tokenS

print([(ent.orth_, ent.label_) for ent in doc.ents[:10]])

tokens = [token.text for token in doc if not token.is_stop]



#%%=======================#
'            fd                '
#========================= #

# making a frequency dictionary
fd1={}
for token in tokens:
    if token in fd1:
        fd1[token]=fd1[token]+1
    else:
        fd1[token]=1



