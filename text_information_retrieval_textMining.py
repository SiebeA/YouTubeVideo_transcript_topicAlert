
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
    os.chdir("/home/siebe/Insync/convexcreate@gmail.com/GD/Engineering/Python/Output")
    print(os.getcwd(),'\n')
    # os.chdir("G:\\.shortcut-targets-by-id\\1aIirQdvbeZM3DsX_qz7FEEv7LiFQQ9Y3\\Engineering\\Python\Output")
    
    # create a dictionary of all the transcripts-sets
    transcripts_dic = {}
    for f in glob.glob('*.txt'):
        with open(f, encoding='utf8') as file: 
            transcripts_dic[f] = file.read()
    # del f, file
    for key in transcripts_dic.keys(): print(key)
    
    
    transcript_requested = input('\nWhat is the transcript request? [format: firstName_lastname of the author] \n')
    
    for string in list(transcripts_dic.keys()):
        # print(string)
        if transcript_requested.split('_')[0].lower() in re.split("_| ", string.lower()) or transcript_requested.split('_')[1].lower() in re.split("_| ", string.lower()):
            print('\n this is the inferred transcript file request:\n\n',string,'\n')
            transcriptFile_Title_requested = string
    user_confirmation = input("Enter on the following line whether this is the right transcript txt file? yes/no\n\n")
    if user_confirmation.lower() != 'yes':
        # print(transcripts_dic.keys())
        for key in transcripts_dic.keys(): print(key)
        transcriptFile_Title_requested = input("\nEnter the name of the transcript txt file on the following line:\n")
    
    
    return transcripts_dic,transcriptFile_Title_requested,transcript_requested

# or when the last script is executed, load the string file:

#%%=======================#
'            REGEX return episode where a key word was mentioned:                 '
#========================= #

def FindAll_wordOfInterest(transcripts_dic:dict,transcriptFile_Title_requested:str):
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
    
    wordOfInterest = input("Input the wordOfInterest on the following line:\n")

    # MATCH the Title etc of the video in which the pattern occurs
    regex = r"(\d{{4}}-\d+-\d+\n.+\n.+)\n\n.+(?={})".format(wordOfInterest) #this regex returns the first match (in first parantheses: title, date, id)c of the 2nd match (2nd parenthesis) 
    
    a_strings_transcripts = transcripts_dic[transcriptFile_Title_requested]
    # a_strings_transcripts = a_strings_transcripts.lower() # maximize recall VIDEO ID REQUIRES case sensitive, so links dont work
    # for 1 set of transcripts:
    import re
    a_metadata_of_matches = re.findall(regex, a_strings_transcripts) #it returns the date and title 
    # for _ in a_metadata_of_matches: print(_,'\n')
    return a_strings_transcripts,wordOfInterest,a_metadata_of_matches



#%% =============================================================================
# OPTINAL: word statistics
# =============================================================================
# words = re.findall('\w+', a_strings_transcripts)
# terms = set(words)
# =============================================================================

def FindAll_contextYwordOfInterest(a_strings_transcripts,wordOfInterest:str,book=False):
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
    
    chars_of_Context = 200
    
    regex_wordOfInterestψContext = f"(.{chars_of_Context})({wordOfInterest})(.{chars_of_Context})"# matches X chars before and after the word of interest
    regex_wordOfInterestψContext = re.sub('\.(\d+)\)', r'.{\1})', regex_wordOfInterestψContext) # substituting/adding the curly brackets (in)
    if book: # then don't blindly match 200 chars adjoining, but the rest of the paragraph:
        regex_wordOfInterestψContext = re.sub('}','}|^.+',regex_wordOfInterestψContext)
        regex_wordOfInterestψContext = re.sub('{','{|.+$',regex_wordOfInterestψContext)

    
    a_matches_KeywordψContext = re.findall(regex_wordOfInterestψContext, a_strings_transcripts,flags=re.IGNORECASE|re.MULTILINE)
    # del a_strings_transcripts
    # it APPENDS, so delete file after use, or find a way to not append duplicate lines
    return a_matches_KeywordψContext,wordOfInterest,book

#%%
def Create_SearchResult_File(transcript_requested,wordOfInterest,a_matches_KeywordψContext,book):
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
    # import os # remove the old output file, otherwise old matches are present
    # output_file = None
    # try:
    #     os.remove(output_file.name)
    # except:
    #     pass
    counter = 0
    # error = []
    error = {'SearchPattern':[],'regex':[]}
    with open(f"SearchResults/SearchRequest{transcript_requested}+'{wordOfInterest}.txt", "a") as output_file:
        output_file.truncate(0) # this removes the CONTENT of the output_file
        for match in a_matches_KeywordψContext:
            try:
                if book != True: # then we have the metadata in Transcripts
                    print(match,'\n\n')
                    SearchPattern = match[0][-50:]
                    regex = "(\d\d\d\d-\d\d-\d\d\n.+\n.+\n)\n.+{}".format(SearchPattern)
                    
                    # first search the key to identify the corresponding metadata then write the metadata to the string
                    MetaData_string = re.search(regex,a_strings_transcripts)
                    MetaData_string = MetaData_string.group(1)
                    VideoID = re.search("\n(.+)\n",MetaData_string).group(1)
                    VideoURL = "https://www.youtube.com/watch?v="+VideoID
                    MetaData_string = re.sub("\n.+\n", "\nhttps://www.youtube.com/watch?v="+VideoID+"\n", MetaData_string)
                    
                    # METADATA write:
                    output_file.write(MetaData_string + "\n")
                # CONTEXT + WORDOFINTEREST + CONTEXT:
                output_file.write(match[0]+"<"+match[1]+">"+match[2] + "\n\n\n") # create 1 string per match, + newLine
                
                counter +=1
                print(f"\n {counter} of {len(a_matches_KeywordψContext)}")
            except AttributeError: # occurs when the searchPattern cannot be found
                print("AttributeError")
                error['SearchPattern'].append(SearchPattern), error['regex'].append(regex)
                continue
                
                return VideoURL


# #%% =============================================================================
# #  NER counter ; see 'proposed_Ner_counter.py'
# # =============================================================================

# %%===========================================================================
# Execution 
# =============================================================================

words_of_interest = ['rogan', 'fake', 'dutch', ]
case_sensitive = False # TODO

if __name__ == '__main__':
    import re

    transcripts_dic,transcriptFile_Title_requested,transcript_requested = transcript_dic()
        
    a_strings_transcripts,wordOfInterest,a_metadata_of_matches = FindAll_wordOfInterest(transcripts_dic,transcriptFile_Title_requested)
    
    a_matches_KeywordψContext,wordOfInterest,book = FindAll_contextYwordOfInterest(a_strings_transcripts,wordOfInterest)
    
    Create_SearchResult_File(transcript_requested,wordOfInterest,a_matches_KeywordψContext,book)
