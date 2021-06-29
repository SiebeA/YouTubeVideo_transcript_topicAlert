"""
Check: whether api_key is (still) valid

Goal: 
    find out the metadata for when Scott talks about HOFFMAN REALITY
    
Resources:
    https://pypi.org/project/youtube-channel-transcript-api/

"""
api_key = 'AIzaSyALCUVfoSmYyXdNw127yt9-fpOfrAcOeUY' # this api key can be obtained from: https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials?folder=&organizationId=&project=turnkey-conduit-277510


#%%=======================#
'            Obtaining video ids from a specified YouTube channel                '
#========================= #


#define the channel from which you want to pull the transcripts
ScottAdams = "UCfpnY5NnBl-8L7SvICuYkYQ"
channel_Id = ScottAdams

#now the video ids need to be obtained
#the google api link acn do this, just format the api_key & channel_Id into it:
youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50"
from urllib.request import urlopen
import json #the format is in json
# store the response of URL
response = urlopen(youtubeChannelMetaDataUrl)
# storing the JSON response from url in data
data_json = json.loads(response.read()) #this holds info we need

#pulling data we need for the process of downloading transcripts:
nextPageToken = data_json['nextPageToken'] #this can give us the next 50 items


#%%=======================#
'            Pulling metadata (including IDS)                '
#========================= #
items = data_json['items'] # contains Ids, metadata, ...
#extracting from the above what we require for furthering the process:
metaDataIncIds = [(i['id']['videoId'] , 
                   i['snippet']['publishTime'][:10],
                    i['snippet']['title'],
                   ) for i in items]



date = items[0]['snippet']['publishedAt'][:10]
title = items[0]['snippet']['title']
ids = items[0]['id']['videoId']


#DEP store in DIC
metadata = {} # Date with videoID
counter = 0
for i in items:
    print(i['id']['videoId'])
    metadata[items[counter]['snippet']['publishedAt'][:10]] = i['id']['videoId']
    counter +=1
    
#NEW store in LIST
mettadata = []
for i in items:
    mettadata.append((i['snippet']['publishedAt'][:10],i['snippet']['title'],i['id']['videoId']))



#download the transcripts from the Idlist
max_videos = 5 #specify for how many videos you want to extract the transcripts
date_vids = [i[0] for i in mettadata][:max_videos]
title_vids = [i[1] for i in mettadata][:max_videos]
ids_vids = [i[2] for i in mettadata][:max_videos]
from youtube_transcript_api import YouTubeTranscriptApi
transcripts = YouTubeTranscriptApi.get_transcripts(video_ids=ids_vids,continue_after_error=True)


#extract the text from the transcript (disregarding the timestamps that are in the dic)
strings_transcripts = ""
for i in range(len(ids)):
    for key,date,title in zip(transcripts[0],date_vids,title_vids):
        strings_transcripts += date +"\n"+ title +"\n" #date and title at the start (before the series of strings that correspond with that title+date)
        # print(key)
        for i in transcripts[0][key]:
                  strings_transcripts += i['text']+" " #TODO ; Date + title before 


#TODO instead of above, create a dict with ids as keys and other metadata as values







{k: v for k, v in sorted(metaDataIncIds.items(), key=lambda item: item[1])}





counter = 0
while counter != len(ids):
        strings_transcripts += metaDataIncIds[counter] +"\n\n" #1 video title before each whole transcripts gets added to the string
#        strings_transcripts += "test"     # plus the date
        for C in transcripts[X]:
            strings_transcripts+=" "
            for D in C['text']:
                strings_transcripts+=D
#         strings_transcripts += "\n\n\n\n\n"
# print('nr of transcripts: ',strings_transcripts.count('Date'))



with open("transcripts_outputX.txt", "w",encoding="utf-8") as output:
    output.write(str(strings_transcripts))







#%% 

''' scraping videos from the specified channel   '''
#======================================================================== #






upload_id = json_url_read_items_dict = json_url_read['items'][0]['contentDetails']['relatedPlaylists']['uploads']




    
#%%
def videoIDTitleANDdate_Extractor():
    #======================================================================== #
    ''' scraping videos from a channel Scott Adams   '''
    #======================================================================== #
    api_key = 'AIzaSyAst2W7w4-a_RSe9NI7FppcL1pnXRTpJJg' # this api key can be obtained from: https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials?folder=&organizationId=&project=turnkey-conduit-277510
    import urllib.request
    import json
    # create a playlist of all the videos uploaded by the channel:
    ChannelId =f"https://www.googleapis.com/youtube/v3/channels?id={channel_Id}&key={api_key}&part=contentDetails"
    json_url = urllib.request.urlopen(ChannelId)
    json_url_read = json.loads(json_url.read())
    
    upload_id = json_url_read_items_dict = json_url_read['items'][0]['contentDetails']['relatedPlaylists']['uploads']

#%%
videoIDTitleANDdate_Extractor()

#%%
    #use that uploadID in the url2:ID=... till &  to scrape all video IDS and others of those videos:
    
    
items = []
X = 0
url3 = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={upload_id}&key={api_key}&part=snippet&maxResults=50'
json_url3 = urllib.request.urlopen(url3)
json_url_read3 = json.loads(json_url3.read())

while X < 20:
    json_url3 = urllib.request.urlopen(url3)
    json_url_read3 = json.loads(json_url3.read())
    if 'nextPageToken' in json_url_read3.keys():
        nextPageToken = json_url_read3['nextPageToken'] # if run out you get previous?
        url3 = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={upload_id}&key={api_key}&part=snippet&maxResults=50&pageToken={nextPageToken}'
    items.append(json_url_read3['items'])
    X +=1


# looping through the items (ITEMS INCLUDES TITLES)
i=0
z=0
for X in items:
#    print (items[i][z]['snippet']['title']) #LIST INDEX OUT oF range
    for D in X:
#            print  (D['snippet']['title'],D['snippet']['publishedAt'][:10]) #FIRST 1 = TITLE, 2nd = DATE
        z +=1
        if z ==50:
            z=0
    i+=1

#date of 1 file:
date = items[0][0]['snippet']['publishedAt'][:10]

#%%
    # =============================================================================
    # creating a DICT with keys=videoIDs & value = Title+Date
    # =============================================================================
counter = 0
videoIdList = []
date = []
videoTitle=[]   
for D in items:
#    print (D)
    for X in D:
        videoIdList.append ( X['snippet']['resourceId']['videoId'])
        date.append (       X['snippet']['publishedAt'][:10]) #10 refers to the first 10 characters, which omits the non date info
        videoTitle.append ( X['snippet']['title'] +'\n\n Date: '+ date[counter])
        counter +=1
        # return dict(zip(videoIdList, videoTitle))

#%%
videoIDTitleANDdate = videoIDTitleANDdate_Extractor()
idList_specifiedNumber = list(videoIDTitleANDdate)[videoSubset]

#%%   just insert video ids here?
from youtube_transcript_api import YouTubeTranscriptApi
    
# passing the idlist
hallo = videoIdList[:5]

import time
start_time = time.time() #plus counting the time



transcripts_w_timestamps =YouTubeTranscriptApi.get_transcripts(video_ids=hallo,continue_after_error=True)

transcripts_w_timestamps = transcripts_w_timestamps[0]

print('time it took:', time.time() - start_time)


#transcripts_w_timestamps = transcripts_w_timestamps[0]
    


##exracting ranscript-text from dic and concatenating to a string
#transcript_string =""
#for y in transcripts[0]:
#    transcript_string += (X['text'])

#create a list of video ids, serving as keys for next para
idlist = list(transcripts_w_timestamps.keys())


# =============================================================================
# #extracting the texts from the seperate DICTS in transcripts
# =============================================================================
strings_transcripts = ""
for X in idlist:
        strings_transcripts += videoIDTitleANDdate[X] +"\n\n" #1 video title before each whole transcripts gets added to the string
#        strings_transcripts += "test"     # plus the date
        for C in transcripts_w_timestamps[X]:
            strings_transcripts+=" "
            for D in C['text']:
                strings_transcripts+=D
        strings_transcripts += "\n\n\n\n\n"
print('nr of transcripts: ',strings_transcripts.count('Date'))

with open("transcripts_outputX.txt", "w",encoding="utf-8") as output:
    output.write(str(strings_transcripts))


