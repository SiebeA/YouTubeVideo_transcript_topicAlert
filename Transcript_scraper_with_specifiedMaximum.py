#%%=======================#
'            User input:                '
#========================= #

        # you can add some channels, for easy switching the input to the program:
channel_Id = "UCfpnY5NnBl-8L7SvICuYkYQ" #Scott adams
# channel_Id = "UCNAxrHudMfdzNi6NxruKPLw" #sam harris
# channel_Id = "UCGaVdbSav8xWuFWTadK6loA" #vlogbrothers
# channel_Id = "UCh_dVD10YuSghle8g6yjePg" #naval
# channel_Id = "UC88A5W9XyWx7WSwthd5ykhw" #Krishnamurti
# channel_Id = "UCRhV1rWIpm_pU19bBm_2RXw" #SeanCaroll
# channel_Id = "UCjYKsjt-7EDU78KEcVbhYnQ" #Shkreli

newTranscript = False # if it were to be the first, a new txt file is created; after: the scraped transcripts are appended to the existing txt file

# input (your) API-key ; I do not explicitly write it here because otherwise people could copy it.
import os
os.chdir("/home/Insync/Convexcreate@gmail.com/GD/Engineering/Development/YouTubeVideo_transcript_topicAlert")
with open('api_key.txt', 'r') as file:
    api_key = file.read().replace('\n', '')



dir_oldTranscripts = "/home/Insync/Convexcreate@gmail.com/GD/Engineering/Python/Output"



if newTranscript is True:
    _ = input("\nconfirm that there is not already a existing transcript with 'y'\n")
    if _ != 'y':
        exit()



#%%=======================#
'  Import latest outputTranscript file if already exists + determining its latest transcript date (such that we download only new transcripts         '
#========================= #

if newTranscript == False:
    from datetime import datetime
    import os, glob, pickle
    os.chdir(dir_oldTranscripts) # dir of the formerly stored transcript files, if they exist already
    for f in glob.glob('*txt'): print(f,"\n")
    # os.startfile(os.getcwd())
   
    transcriptTextFileTitle = glob.glob('*txt') 
    channel = input("\n From the existing transcripts, which youtube channel is it that you want to scrape the new transcripts from, and append them to the txt file which are printed above?... copy (right mouse) and paste the name of that file on the following line  \n\n ")
    
    with open(channel,encoding='utf8') as file:
        a_strings_transcripts_existing = file.read()

    #determining the most recent date of the transcriptfile
    datetime_lastVid = datetime.strptime(a_strings_transcripts_existing[4:12], '%y-%m-%d')
    delta = datetime.today() - datetime_lastVid
    print( f'\n It has been *** {delta.days} *** many days since the latest transcript in our latest output file till today ')


if newTranscript==True:
    max_videos = 1000 #specify how many videos have to be incluced
else:
    max_videos = delta.days #specify how many videos have to be incluced #bug is when the channel uploads more videos per day, then some will be missed. 



#%%=======================#
'   Retrieving the Youtube videos metadate through json parsing                '
#========================= #

def json_storer(): # stores the video meta-data; including Ids required for downloading next
    counter =0
    from urllib.request import urlopen
    import json
    b_json_files = []
    youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50"
    response = urlopen(youtubeChannelMetaDataUrl)
    data_json = json.loads(response.read()) 
    b_json_files.append(data_json)
    # counter = 0
    if max_videos>50: #we require a nextpagetoken to extract additional metadata
        i = 0
        nextPageToken = ""
        # : #dep:
        from math import ceil
        while counter != (ceil(max_videos/100*2)-1) and 'nextPageToken' in b_json_files[i].keys():#dont waste quota asking for more tokens than our maxvideo count requires; (for 120 videos: 50 first token, cum100 for 1 add, cum 150 1)
            nextPageToken = b_json_files[i]['nextPageToken']
            youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50&pageToken={nextPageToken}"
            response = urlopen(youtubeChannelMetaDataUrl)
            data_json = json.loads(response.read()) 
            b_json_files.append(data_json)
            i +=1
            print(f" nextpagetoken nr.:{counter}")
            counter +=1
        print(youtubeChannelMetaDataUrl)
    return b_json_files

b_json_files = json_storer()#don't call the dic in the list, as we can append multiple dics for every 50 additional videos you'd want to extract.

#%%=======================#
'            X  2  filtering and storing the metadata that we want               '
#========================= #

def youtubeMetaDataExtractor():
    success = 0
    fail = []
    metaDataYoutubeVideo = []
    for i in b_json_files:
        try: 
            for key in i['items']:
                metaDataYoutubeVideo.append((key['snippet']['publishedAt'][:10],key['snippet'],key['id']['videoId']))
                success+=1
        except:
            'whatever'
            fail.append(i)
            # print(key['id']['videoId'])
    # print(f'{success} times success')
    # print(f'{fail} times fail')
    return metaDataYoutubeVideo, fail

metaDataYoutubeVideo,fail = youtubeMetaDataExtractor()

# Some of the metadata of the videos, before correction of the ones for which no transcript is available:
date_vids = [i[0] for i in metaDataYoutubeVideo][:max_videos]
title_vids = [i[1]['title'] for i in metaDataYoutubeVideo][:max_videos]
ids_vids = [i[2] for i in metaDataYoutubeVideo][:max_videos]



#%%=======================#
'          3  Downloading with API'
#========================= #

"""
2 variables necessary:
    - ids_vids
    - max_videos
"""

def transcriptDownloader(listofVideoIds):
    import time
    start_time = time.time()
    
    from youtube_transcript_api import YouTubeTranscriptApi
    transcripts = YouTubeTranscriptApi.get_transcripts(video_ids=ids_vids[:max_videos],continue_after_error=True)
    
    print('time it took in secs to download the transcripts :', round(time.time() - start_time))
    
    return transcripts

transcripts = transcriptDownloader(ids_vids)# i0=succesfull i2=unsuccesful in transcript extraction

#%%=======================#
'            correction for missing transcripts                '
#========================= #
# sometimes a transcript is missing, then we need to make new lists of the other transcript meta data, otherwise wrong transcripts are attributed to the wrong metaData s.a. date or ID

dic = {i: (f,d) for i,f,d in zip(ids_vids,date_vids,title_vids)} #storing date and title as keys corresponding to the ids\values



for i in transcripts[1]:
    try:
        dic.pop(i)
    except:
        continue

#after correction, some of the videos metadata:
ids_vids = [i[0] for i in dic.items()]
date_vids = [i[1][0] for i in dic.items()]
title_vids = [i[1][1] for i in dic.items()]



#%%=======================#
'      organizing the downloaded transcripts; filter out text (not timestamps)'
#========================= #
#
def textTranscriptExtractor():
    import time
    start_time = time.time()
    counter = 0
    transcript_txtFile = ""
    # for i in range(10): #(len(transcripts[0])):
    for key,date,title,idd in zip( transcripts[0],date_vids,title_vids,ids_vids):
        transcript_txtFile += str(counter)+"\n" + date +"\n"+idd+"\n"+ title +"\n\n" 
        for i in transcripts[0][key]: #so all the 
            transcript_txtFile += i['text']+" " #the text is written under the date,id,title
        transcript_txtFile +="\n\n" 
        counter +=1
    print('time it took to extract the text in secs:', round(time.time() - start_time))
    return transcript_txtFile


if newTranscript == True:
    a_strings_transcripts = textTranscriptExtractor()
else:
    a_strings_transcripts = textTranscriptExtractor()
    a_strings_transcripts = a_strings_transcripts + a_strings_transcripts_existing
# |
# a_strings_transcriptsNew = textTranscriptExtractor()
# aaa = a_strings_transcriptsNew + a_strings_transcripts



#%% =============================================================================
# #export if necessary:
# =============================================================================
import re
if newTranscript != True:
    datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", a_strings_transcripts_existing) # we need the dates of the preexisting file in order to open it (and write the new transcripts to ti)
else:
    datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", a_strings_transcripts)

channelTitle = metaDataYoutubeVideo[0][1]['channelTitle'] # just for passing ti to the output file name

with open(f'/home/Insync/Convexcreate@gmail.com/GD/Engineering/Python/Output/transcript_{channelTitle}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt', "w",encoding="utf-8") as text_file:
    text_file.write(a_strings_transcripts)
    import os
    datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", a_strings_transcripts) # will be used to name the transcript file with earliest and latest transcript date in the title
    os.rename(os.path.abspath(text_file.name),f'/home/Insync/Convexcreate@gmail.com/GD/Engineering/Python/Output/transcript_{channelTitle}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt')
    # print("Output File: {}".format(os.path.abspath(text_file.name)), f'/home/Insync/Convexcreate@gmail.com/GD/Engineering/Python/Output/transcript_{channelTitle}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt')


# #export the date last, the most recent date will be used to determine how many transcripts need to be scraped for the next time (see first section where the pickle is loaded)
# with open('C:\\Users\\siebe\\GD\\Engineering\\.Python\\output\\dateVids.pickle', 'wb') as handle:
#     pickle.dump(date_vids, handle, protocol=pickle.HIGHEST_PROTOCOL)


