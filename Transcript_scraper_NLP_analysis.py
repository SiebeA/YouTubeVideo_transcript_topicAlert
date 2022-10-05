
#%%=======================#
'  Importing (all) transcripts-sets              '
#========================= #

def transcript_dic():
    import os, glob
    """
        - Also return the surrounding words of the match
        - Frequency dict without stop words
        - Frequency NER
        - Corpus: each video is a seperate file, then TFIDF analysis
    """
    print(os.getcwd())
    os.chdir("/home/siebe/Insync/convexcreate@gmail.com/GD/Engineering/Python/Output")
    # os.chdir("G:\\.shortcut-targets-by-id\\1aIirQdvbeZM3DsX_qz7FEEv7LiFQQ9Y3\\Engineering\\Python\Output")
    
    # create a dictionary of all the transcripts-sets
    transcripts_dic = {}
    for f in glob.glob('*.txt'):
        with open(f, encoding='utf8') as file: 
            transcripts_dic[f] = file.read()
    del f, file
    return transcripts_dic

# or when the last script is executed, load the string file:

#%%=======================#
'            REGEX return episode where a key word was mentioned:                 '
#========================= #

def FindAll_wordOfInterest(wordOfInterest:str,transcripts_dic:dict,transcriptFile_requested:str):
    '''
    Parameters
    ----------
    wordOfInterest : STR
        DESCRIPTION.
    transcripts_dic : DICT
        DESCRIPTION.

    Returns
    -------
    a_metadata_of_matches : Match_object
        DESCRIPTION.
    '''

    # MATCH the Title etc of the video in which the pattern occurs
    regex = r"(\d{{4}}-\d+-\d+\n.+\n.+)\n\n.+(?={})".format(wordOfInterest) #this regex returns the first match (in first parantheses: title, date, id)c of the 2nd match (2nd parenthesis) 
    
    a_strings_transcripts = transcripts_dic[transcriptFile_requested]
    a_strings_transcripts = a_strings_transcripts.lower() # maximize recall VIDEO ID REQUIRES case sensitive, so links dont work
    # for 1 set of transcripts:
    import re
    a_metadata_of_matches = re.findall(regex, a_strings_transcripts) #it returns the date and title 
    del regex
    # for _ in a_metadata_of_matches: print(_,'\n')
    return a_metadata_of_matches,a_strings_transcripts



#%% =============================================================================
# OPTINAL: word statistics
# =============================================================================
# words = re.findall('\w+', a_strings_transcripts)
# terms = set(words)
# =============================================================================

def FindAll_contextYwordOfInterest(a_strings_transcripts,chars_of_Context,wordOfInterestψContext):
    '''
    

    Parameters
    ----------
    a_strings_transcripts : STR
        DESCRIPTION.
    chars_of_Context : INT
        DESCRIPTION.
    wordOfInterestψContext : STR
        DESCRIPTION.

    Returns
    -------
    a_matches_KeywordψContext : STR
        DESCRIPTION.

    '''
    wordOfInterestψContext = f"(.{chars_of_Context})({wordOfInterest})(.{chars_of_Context})"# matches X chars before and after the word of interest
    wordOfInterestψContext = re.sub('\.(\d+)\)', r'.{\1})', wordOfInterestψContext) # substituting/adding the curly brackets (in)
    
    a_matches_KeywordψContext = re.findall(wordOfInterestψContext, a_strings_transcripts)
    # del a_strings_transcripts
    # it APPENDS, so delete file after use, or find a way to not append duplicate lines
    return a_matches_KeywordψContext

#%%
def Create_SearchResult_File(a_matches_KeywordψContext):
    """
    

    Parameters
    ----------
    a_matches_KeywordψContext : TYPE
        DESCRIPTION.

    Returns
    -------
    VideoURL : TYPE
        DESCRIPTION.

    """
    import os # remove the old output file, otherwise old matches are present
    output_file = None
    try:
        os.remove(output_file.name)
    except:
        pass
    counter = 0
    error = []
    with open(f"SearchResults/SearchRequest{_transcript_requested}+'{wordOfInterest}.txt", "a") as output_file:
        output_file.truncate(0) # removes all text in the file?
        for match in a_matches_KeywordψContext:
            try:
                print(match,'\n\n')
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
                output_file.write(match[0]+"<<<<<"+match[1]+">>>>>"+match[2] + "\n\n\n") # create 1 string per match, + newLine
                counter +=1
                print(f"\n {counter} of {len(a_matches_KeywordψContext)}")
            except AttributeError: # occurs when the searchPattern cannot be found
                print("AttributeError")
                error.append(SearchPattern)
                
                return VideoURL

# see 'proposed_Ner_counter.py'

# # =============================================================================
# #  NER counter
# # =============================================================================

#     #match the paragraphs with corresponding ID
# regex = r"(\d\n\d+-\d+-\d+\n)(.+)\n(.+\n\n)(.+)"
# matches = re.finditer(regex, a_strings_transcripts, re.MULTILINE) #beware of generator : needs to be reinitated after use
# a_metadata_of_matchess = [(match.group(2),match.group(4))  for match in matches] #match ID and text
# #convert to dic:
# dict={}
# for a,b in a_metadata_of_matchess:
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

# =============================================================================
# 
# =============================================================================

#%%
wordOfInterest = 'eminem' # Only lowercase will return matches
chars_of_Context = 200
_transcript_requested = 'scott_adams' # input-format: Firstname_Lastname

if __name__ == '__main__':
    import re

    transcripts_dic = transcript_dic()
    for string in list(transcripts_dic.keys()):
        # print(string)
        if _transcript_requested.split('_')[0].lower() in re.split("_| ", string.lower()) or _transcript_requested.split('_')[1].lower() in re.split("_| ", string.lower()):
            print('\n this is the inferred transcript file request:',string,'\n')
            transcriptFile_requested = string
    user_confirmation = input("Enter on the following line whether this is the right transcript txt file? yes/no\n")
    if user_confirmation.lower() != 'yes':
        print(transcripts_dic.keys())
        transcriptFile_requested = input("\nEnter the name of the transcript txt file on the following line:\n")
        
    a_matches_KeywordψContext,a_strings_transcripts = FindAll_wordOfInterest(wordOfInterest,transcripts_dic,transcriptFile_requested)
    
    a_Context_of_matches = FindAll_contextYwordOfInterest(a_strings_transcripts,chars_of_Context,wordOfInterest)
    
    Create_SearchResult_File(a_Context_of_matches)
