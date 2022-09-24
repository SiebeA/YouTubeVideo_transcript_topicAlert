

wordOfInterest = 'rogan'
chars_of_Context = 200


#%%=======================#
'  Importing (all) transcripts-sets              '
#========================= #
import os, glob
import time
# import pandas as pd
import re
# from collections import Counter
# import spacy
"""
    - Also return the surrounding words of the match
    - Frequency dict without stop words
    - Frequency NER
    - Corpus: each video is a seperate file, then TFIDF analysis
"""

print(os.getcwd())
os.chdir("/home/siebe/Insync/convexcreate@gmail.com/GD/Engineering/Python/Output")

# create a dictionary of all the transcripts-sets

transcripts_dic = {}
for f in glob.glob('*.txt'):
    with open(f, encoding='utf8') as file: 
        transcripts_dic[f] = file.read()
del f, file

# or when the last script is executed, load the string file:




#%%=======================#
'            REGEX return episode where a key word was mentioned:                 '
#========================= #



# MATCH the Title etc of the video in which the pattern occurs
regex = r"(\d{{4}}-\d+-\d+\n.+\n.+)\n\n.+(?={})".format(wordOfInterest) #this regex returns the first match (in first parantheses: title, date, id)c of the 2nd match (2nd parenthesis) 

_transcript_requested = 'ScottAdams'
a_strings_transcripts = transcripts_dic['transcript_Real Coffee with Scott Adams_between_2022-09-03_and_2019-05-17.txt']
# for 1 set of transcripts:
a_matches_metadata = re.findall(regex, a_strings_transcripts) #it returns the date and title 
del regex
# for _ in a_matches_metadata: print(_,'\n')


#%% =============================================================================
# OPTINAL: word statistics
# =============================================================================
# words = re.findall('\w+', a_strings_transcripts)
# terms = set(words)
# =============================================================================


# MATCH the context of the patterns
wordOfInterestψContext = f"(.{chars_of_Context})({wordOfInterest})(\s.{chars_of_Context})"# matches X chars before and after the word of interest
wordOfInterestψContext = re.sub('\.(\d+)\)', r'.{\1})', wordOfInterestψContext) # substituting/adding the curly brackets (in)

a_matches_KeywordψContext = re.findall(wordOfInterestψContext, a_strings_transcripts)
# del a_strings_transcripts
# it APPENDS, so delete file after use, or find a way to not append duplicate lines

#%%
import os # remove the old output file, otherwise old matches are present
output_file = None
try:
    os.remove(output_file.name)
except:
    pass

counter = 0
error = []
with open(f"SearchRequest{_transcript_requested}+'{wordOfInterest}.txt", "a") as output_file:
    for match in a_matches_KeywordψContext:
        try:
            print(match,'\n\n')
            # _start = time.time() # for measuring time
            # _end = time.time()
            # print(_end - _start)
            
            SearchPattern = match[0][-50:]
            regex = "(\d\d\d\d-\d\d-\d\d\n.+\n.+\n)\n.+{}".format(SearchPattern)
            
            # first search the key to identify the corresponding metadata then write the metadata to the string
            MetaData_string = re.search(regex,a_strings_transcripts)
            MetaData_string = MetaData_string.group(1)
            VideoID = re.search("\n(.+)\n",MetaData_string).group(1)
            VideoURL = "https://www.youtube.com/watch?v="+VideoID
            MetaData_string = re.sub("\n.+\n", "\nhttps://www.youtube.com/watch?v="+VideoID+"\n", MetaData_string)
            
            
            output_file.write(MetaData_string + "\n")
            # 2nd write the context + wordOfInterest + context:
            output_file.write(match[0]+match[1]+match[2] + "\n\n\n") # create 1 string per match, + newLine
            counter +=1
            print(f"\n {counter} of {len(a_matches_KeywordψContext)}")
        except AttributeError: # occurs when the searchPattern cannot be found
            print("error")
            error.append(SearchPattern)
try: del wordOfInterestψContext,regex,VideoID,VideoURL 
except: pass
        
# matching a group of the pattern; ie context before, the word, or context after ; each is parenthesized in the {wordOfInterestψContext} variable. 



#%% =============================================================================
# Return the metadata for every wordOfInterest match
# =============================================================================

# create a search pattern by the last X chars before the wordOfInterest, and use that to match the 0th group, which is the metaData information
word = a_matches_KeywordψContext[0][0][-50:]
_ = "(\d\d\d\d-\d\d-\d\d\n.+\n.+\n)\n.+{}".format(word)
result = re.search(_,a_strings_transcripts)
result = result.group(1)





# # =============================================================================
# #  NER counter
# # =============================================================================

#     #match the paragraphs with corresponding ID
# regex = r"(\d\n\d+-\d+-\d+\n)(.+)\n(.+\n\n)(.+)"
# matches = re.finditer(regex, a_strings_transcripts, re.MULTILINE) #beware of generator : needs to be reinitated after use
# a_matches_metadatas = [(match.group(2),match.group(4))  for match in matches] #match ID and text
# #convert to dic:
# dict={}
# for a,b in a_matches_metadatas:
#     dict.setdefault(a, []).append(b)
# del a,b
# # explanation: how is it sorted? ; date chronological, despite when you look in the variable explorer (when it's sorted alphabetically)

#     # nlping the latest transcript (ie index 0)

# nlp = spacy.load("en_core_web_sm")
# doc = nlp(dict[list(dict.keys())[0]][0])

#     #NER summarizing
# labels, Counter = [ent.label_ for ent in doc.ents], 
# Counter(labels)
# items = [ent.text for ent in doc.ents if not (ent.label_ =='CARDINAL')]
# a_nerCounter = pd.DataFrame(Counter(items).most_common(10), columns =['ner', 'occurence']) #1st argument = list of tuples with a coupleTuple
#     #now scale to all the transcripts:
# listOf_a_nerCounter = []
# for key in list(dict.keys())[:5]:
#     doc = nlp(dict[key][0])
#     labels = [ent.label_ for ent in doc.ents]
#     Counter(labels)
#     items = [ent.text for ent in doc.ents]
#     a_nerCounter = pd.DataFrame(Counter(items).most_common(10), columns =['ner', 'occurence']) #1st argument =
#     listOf_a_nerCounter.append((key, pd.DataFrame(Counter(items).most_common(10), columns =['ner', 'occurence'])))
# #TODO: id in the list with the df
