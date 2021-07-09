
"""
Check: whether api_key is (still) valid

Application goal:
    I follow Scott adams on Youtube. Scott covers a wide range of topics, some which I want to evade, some which I do not want to miss. I want to match the exact videos in which He talks about this or that, or X times about this or that. 
    Even deeper: 2 words close together appearance in a video; i.e. whenever "Naval" & "bitcoin" occur in between 100 characters, I get a list of episodes in which that condition is satisfied
    feature: for every new video in which condition (x1,x2,xN) is satisfied, get a notification. 
    
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


max_videos = 220
# api_key = input('enter time in format hh:mm')
channel_Id = "UCfpnY5NnBl-8L7SvICuYkYQ" #Scott adams
# channel_Id = "UCNAxrHudMfdzNi6NxruKPLw" #sam harris
# channel_Id = "UCGaVdbSav8xWuFWTadK6loA" #vlogbrothers


'          1  Json parsing                '
#TODO scrape less than 10 tokens when maximum is less than that



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
        # while 'nextPageToken' in b_json_files[i].keys():
        while counter != (ceil(max_videos/100*2)):
            nextPageToken = b_json_files[i]['nextPageToken']
            youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50&pageToken={nextPageToken}"
            response = urlopen(youtubeChannelMetaDataUrl)
            data_json = json.loads(response.read()) 
            b_json_files.append(data_json)
            i +=1
            counter +=1
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

# dic = {i: (f,d) for i,f,d in zip(date_vids,ids_vids,title_vids)} #more consise alternative



def transcriptDownloader(listofVideoIds):
    import time
    start_time = time.time() 
    from youtube_transcript_api import YouTubeTranscriptApi
    transcripts = YouTubeTranscriptApi.get_transcripts(video_ids=ids_vids[:150],continue_after_error=True)
    print('time it took:', time.time() - start_time)
    return transcripts

transcripts = transcriptDownloader(ids_vids)


#%%=======================#
'      organizing the downloaded transcripts; filter out text (not timestamps)'
#========================= #

def textTranscriptExtractor():
    import time
    start_time = time.time() 
    a_strings_transcripts = ""
    counter = 0
    # for i in range(10): #(len(transcripts[0])):
    for key,date,title,idd in zip( transcripts[0],date_vids,title_vids,ids_vids):
        print(date)
        a_strings_transcripts += str(counter)+"\n" + date +"\n"+idd+"\n"+ title +"\n\n" 
        for i in transcripts[0][key]:
            a_strings_transcripts += i['text']+" "
        a_strings_transcripts +="\n\n" 
        counter +=1
    print('time it took:', time.time() - start_time)
    return a_strings_transcripts

a_strings_transcripts = textTranscriptExtractor()
print(len(a_strings_transcripts))


#export if u want
with open("output_file.txt", "w",encoding="utf-8") as text_file:
    text_file.write(a_strings_transcripts)
    

# import pickle
# with open('metaDataYoutubeVideo.pickle', 'wb') as handle:
#     pickle.dump(metaDataYoutubeVideo, handle, protocol=pickle.HIGHEST_PROTOCOL)



