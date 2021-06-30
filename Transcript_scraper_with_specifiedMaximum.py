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
ScottAdams = "UCfpnY5NnBl-8L7SvICuYkYQ"# easier for later when storing more channel-ids
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


# for future readability:
# date = items[0]['snippet']['publishedAt'][:10]
# title = items[0]['snippet']['title']
# ids = items[0]['id']['videoId']

# deprecated:
def dicStorer():
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
for i in range(len(ids_vids)):
    for key,date,title in zip(transcripts[0],date_vids,title_vids):
        strings_transcripts += date +"\n"+ title +"\n" #date and title at the start (before the series of strings that correspond with that title+date)
        # print(key)
        for i in transcripts[0][key]:
                  strings_transcripts += i['text']+" "

#TODO nextpagetoken

