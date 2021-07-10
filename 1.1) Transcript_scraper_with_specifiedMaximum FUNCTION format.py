
"""
Check: whether api_key is (still) valid

Goal: 
    find out the metadata for when Scott talks about HOFFMAN REALITY
    
Common bugs:
    - when transcript is unavaible for a given ID, the next transcript is being written under the ID that was unavailable
"""



#%%=======================#
'            User input:                '
#========================= #
api_key = 'AIzaSyA3ALHnyYZ4Ns1dGhwhMkfX4yPhqD-3lLE'
# 

#%%=======================#
'            X                '
#========================= #


max_videos = 100
# api_key = input('enter time in format hh:mm')
channel_Id = "UCfpnY5NnBl-8L7SvICuYkYQ" #Scott adams
# channel_Id = "UCNAxrHudMfdzNi6NxruKPLw" #sam harris
# channel_Id = "UCGaVdbSav8xWuFWTadK6loA" #vlogbrothers


'          1  Json parsing                '
#TODO scrape less than 10 tokens when maximum is less than that
def json_storer(): # stores the video meta-data; including Ids required for downloading next
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
        while 'nextPageToken' in b_json_files[i].keys():
            print(i)
            nextPageToken = b_json_files[i]['nextPageToken']
            youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50&pageToken={nextPageToken}"
            response = urlopen(youtubeChannelMetaDataUrl)
            data_json = json.loads(response.read()) 
            b_json_files.append(data_json)
            i +=1
            # counter +=1
            # if counter ==3:
            #     break
        print(youtubeChannelMetaDataUrl)
        return b_json_files

b_json_files = json_storer()#don't call the dic in the list, as we can append multiple dics for every 50 additional videos you'd want to extract.

#%%=======================#
'            X  2  storing the metadata that we require               '
#========================= #
'                        '

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


# filteredMetaData = [ [i[0] for i in metaDataYoutubeVideo][:max_videos],[i[1]['title'] for i in metaDataYoutubeVideo][:max_videos],[i[2] for i in metaDataYoutubeVideo][:max_videos] ]

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
    transcripts = YouTubeTranscriptApi.get_transcripts(video_ids=ids_vids[:150],continue_after_error=True)
    print('time it took:', time.time() - start_time)
    return transcripts

transcripts = transcriptDownloader(ids_vids)# i0=succesfull i2=unsuccesful in transcript extraction


#%%=======================#
'            correction for missing transcripts                '
#========================= #
# sometimes a transcript is missing, then we need to make new lists of the other transcript meta data, otherwise wrong transcripts are attributed to the wrong metaData

dic = {i: (f,d) for i,f,d in zip(ids_vids,date_vids,title_vids)} #more consise alternative #TODO make a pop loop in case more than 1 transcripts are missing
dic.pop(transcripts[1][0])

ids_vids = [i[0] for i in dic.items()]
date_vids = [i[1][0] for i in dic.items()]
title_vids = [i[1][1] for i in dic.items()]



#%%=======================#
'      organizing the downloaded transcripts; filter out text (not timestamps)'
#========================= #
#Scneario: 1st transcript is missing ; 
# correct:  date-id-title combination
#  incorrect: transcript 
def textTranscriptExtractor():
    import time
    start_time = time.time()
    a_strings_transcripts = ""
    counter = 0
    # for i in range(10): #(len(transcripts[0])):
    for key,date,title,idd in zip( transcripts[0],date_vids,title_vids,ids_vids):
        a_strings_transcripts += str(counter)+"\n" + date +"\n"+idd+"\n"+ title +"\n\n" 
        for i in transcripts[0][key]: #so all the 
            a_strings_transcripts += i['text']+" " #the text is written under the date,id,title
        a_strings_transcripts +="\n\n" 
        counter +=1
    print('time it took:', time.time() - start_time)
    return a_strings_transcripts

a_strings_transcripts = textTranscriptExtractor()
print(len(a_strings_transcripts))


#export if u want
with open("output_file2.txt", "w",encoding="utf-8") as text_file:
    text_file.write(a_strings_transcripts)
    

# import pickle
# with open('metaDataYoutubeVideo.pickle', 'wb') as handle:
#     pickle.dump(metaDataYoutubeVideo, handle, protocol=pickle.HIGHEST_PROTOCOL)



