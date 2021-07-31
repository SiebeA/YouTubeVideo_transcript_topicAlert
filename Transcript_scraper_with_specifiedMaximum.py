
"""
Check: whether your api_key is (still) valid
    
Bugs resolved:
    - when transcript is unavaible for a given ID, the next transcript is being written under the ID that was unavailable
"""


#%%=======================#
'      determining how many recent transcripts (by importing last output date                '
#========================= #


import os, glob, pickle
print(os.getcwd())
os.chdir("C:\\Users\\siebe\\GD\\Engineering\\.Python\\output")
os.startfile(os.getcwd()) #open the windows file folder
for f in glob.glob('*'): print(f)


#recover last transcript bundle file:
transcriptTextFileTitle = glob.glob('*txt')
with open(transcriptTextFileTitle[0],encoding='utf8') as file:
    a_strings_transcripts = file.read()
    content = file.readlines()
del transcriptTextFileTitle




#determining laste date
with open("dateVids.pickle", "rb") as f:
    lastDateVids = pickle.load(f)
from datetime import datetime
today = datetime.today()
datetime.today().strftime('%Y-%m-%d')
datetime_lastVid = datetime.strptime(lastDateVids[0], '%Y-%m-%d')
datetime_lastVid = datetime.strptime(a_strings_transcripts[4:12], '%y-%m-%d')
delta = today - datetime_lastVid
print( 'this many days since the latest transcript in our latest output file: ', delta.days)





"""
get date
use date to determine how many videos thus tokens
download that number of videos

| 
save the date files list

"""


#%%=======================#
'            User input:                '
#========================= #
api_key = 'AIzaSyDZlegWZl3Mbi7xGPgOnB3qbQXD5EkbSCg' # input (your) API-key ()
# 

max_videos = delta.days #specify how many videos have to be incluced

        # you can add some channels, for easy switching the input to the program:
channel_Id = "UCfpnY5NnBl-8L7SvICuYkYQ" #Scott adams
# channel_Id = "UCNAxrHudMfdzNi6NxruKPLw" #sam harris
# channel_Id = "UCGaVdbSav8xWuFWTadK6loA" #vlogbrothers
# channel_Id = "UCh_dVD10YuSghle8g6yjePg" #naval



#%%=======================#
'   Retrieving the Youtube videos metadate through json parsing                '
#========================= #

def json_storer(): # stores the video meta-data; including Ids required for downloading next
    counter =0
    from urllib.request import urlopen
    import json
    b_json_files = []
    youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=20"
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
            print(counter)
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
# sometimes a transcript is missing, then we need to make new lists of the other transcript meta data, otherwise wrong transcripts are attributed to the wrong metaData

dic = {i: (f,d) for i,f,d in zip(ids_vids,date_vids,title_vids)} #more consise alternative #TODO make a pop loop in case more than 1 transcripts are missing


# dic.pop(transcripts[1][0])


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

def textTranscriptExtractor():
    import time
    start_time = time.time()
    a_strings_transcripts = ""      #output file
    counter = 0
    # for i in range(10): #(len(transcripts[0])):
    for key,date,title,idd in zip( transcripts[0],date_vids,title_vids,ids_vids):
        a_strings_transcripts += str(counter)+"\n" + date +"\n"+idd+"\n"+ title +"\n\n" 
        for i in transcripts[0][key]: #so all the 
            a_strings_transcripts += i['text']+" " #the text is written under the date,id,title
        a_strings_transcripts +="\n\n" 
        counter +=1
    print('time it took to extract the text in secs:', round(time.time() - start_time))
    return a_strings_transcripts

a_strings_transcripts = textTranscriptExtractor()

# =============================================================================
# #export if necessary:
# =============================================================================
channelTitle = metaDataYoutubeVideo[0][1]['channelTitle'] # just for passing ti to the output file name
with open(f'C:\\Users\\siebe\\GD\\Engineering\\.Python\\output\\transcripts_{channelTitle}_between_{date_vids[0]}_and_{date_vids[-1]}.txt', "w",encoding="utf-8") as text_file:
    text_file.write(a_strings_transcripts)


#export the date last, the most recent date will be used to determine how many transcripts need to be scraped for the next time (see first section where the pickle is loaded)
import pickle
with open('C:\\Users\\siebe\\GD\\Engineering\\.Python\\output\\dateVids.pickle', 'wb') as handle:
    pickle.dump(date_vids, handle, protocol=pickle.HIGHEST_PROTOCOL)


