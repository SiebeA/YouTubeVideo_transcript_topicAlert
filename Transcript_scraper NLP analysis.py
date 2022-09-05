
# paramaters:





import os, glob, pickle
import pandas as pd
import re
from collections import Counter
# import spacy
"""
    - Also return the surrounding words of the match
    - Frequency dict without stop words
    - Frequency NER
    - Corpus: each video is a seperate file, then TFIDF analysis
"""


print(os.getcwd())
# os.chdir("C:\\Users\\siebe\\GD\\Engineering\\.Python\\output")
transcripts_dic = {}
for f in glob.glob('*.txt'):
    with open(f, encoding='utf8') as file: 
        transcripts_dic[f] = file.read()
del f, file

# or when the last script is executed, load the string file:



#%%=======================#
'            REGEX return episode where a key word was mentioned:                 '
#========================= #
wordOfInterest = '1984'
regex = r"(\d{{4}}-\d+-\d+\n.+\n.+)\n\n.+(?={})".format(wordOfInterest) #this regex returns the first match (in first parantheses: title, date, id)c of the 2nd match (2nd parenthesis) 


a_strings_transcripts = transcripts_dic['transcript_Real Coffee with Scott Adams_between_2022-09-03_and_2019-05-17.txt']
# for 1 set of transcripts:
a_matches = re.findall(regex, a_strings_transcripts) #it returns the date and title 
for i in a_matches: print(i,'\n')

# =============================================================================
# #match the context of the patternz
# =============================================================================

wordOfInterestψContext = r"(.{{200}})({})(\s.{{200}})".format(wordOfInterest)# matches X chars before and after the word of interest

aa_matches = re.findall(wordOfInterestψContext, a_strings_transcripts)
for match in aa_matches: print(match,'\n\n')
# matching a group of the pattern; ie context before, the word, or context after ; each is parenthesized in the {wordOfInterestψContext} variable. 


# =============================================================================
#  NER counter
# =============================================================================

    #match the paragraphs with corresponding ID
regex = r"(\d\n\d+-\d+-\d+\n)(.+)\n(.+\n\n)(.+)"
matches = re.finditer(regex, a_strings_transcripts, re.MULTILINE) #beware of generator : needs to be reinitated after use
a_matchess = [(match.group(2),match.group(4))  for match in matches] #match ID and text
#convert to dic:
dict={}
for a,b in a_matchess:
    dict.setdefault(a, []).append(b)
del a,b
# explanation: how is it sorted? ; date chronological, despite when you look in the variable explorer (when it's sorted alphabetically)

    # nlping the latest transcript (ie index 0)

nlp = spacy.load("en_core_web_sm")
doc = nlp(dict[list(dict.keys())[0]][0])

    #NER summarizing
labels, Counter = [ent.label_ for ent in doc.ents], 
Counter(labels)
items = [ent.text for ent in doc.ents if not (ent.label_ =='CARDINAL')]
a_nerCounter = pd.DataFrame(Counter(items).most_common(10), columns =['ner', 'occurence']) #1st argument = list of tuples with a coupleTuple
    #now scale to all the transcripts:
listOf_a_nerCounter = []
for key in list(dict.keys())[:5]:
    doc = nlp(dict[key][0])
    labels = [ent.label_ for ent in doc.ents]
    Counter(labels)
    items = [ent.text for ent in doc.ents]
    a_nerCounter = pd.DataFrame(Counter(items).most_common(10), columns =['ner', 'occurence']) #1st argument =
    listOf_a_nerCounter.append((key, pd.DataFrame(Counter(items).most_common(10), columns =['ner', 'occurence'])))
#TODO: id in the list with the df
