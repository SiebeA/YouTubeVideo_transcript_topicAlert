#!C:\Users\Siebe\venvs\.requests\Scripts\python.exe
# the first line is for windows to know which interpreter to use

import sys
from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Now the logging level is set to INFO, and the INFO and DEBUG messages will be printed



# source the api key from: "X:\My Drive\Engineering\Development\YouTubeVideo_transcript_topicAlert\api_key.txt"
with open("api_key.txt", "r") as f:
    api_key = f.read()

max_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 6
channel_requested = sys.argv[2] if len(sys.argv) > 2 else "scott_adams"

max_request = 6 # for scott adams; after 6 there are leaps in video date
youtube_url = "https://www.youtube.com/"

transcripts_dic = {
    "scott_adams": "UCfpnY5NnBl-8L7SvICuYkYQ",
    "sam_harris": "UCNAxrHudMfdzNi6NxruKPLw",
    "martin_shkreli": "UCjYKsjt-7EDU78KEcVbhYnQ",
    "peter_attia": "UC8kGsMa0LygSX9nkBcBH1Sg",
    "tim_ferris": "UCznv7Vf9nBdJYvBagFd",
    "peter_schiff": "",
    "investor_podcast": "",
    "sean_caroll": "UCRhV1rWIpm_pU19bBm_2RXw",
    "na_val": "UCh_dVD10YuSghle8g6yjePg",
    "jordan_peterson": "UCL_f53ZEJxp8TtlOkHwMV9Q",
    "andrew_huberman": "UCkZjTZNvuxq1CYMS3cwZa1Q"
}

path = os.getcwd()
transcript_dir = os.path.join(path, 'transcripts')

if not os.path.exists(transcript_dir):
    os.makedirs(transcript_dir)
    print("Directory", transcript_dir, "Created ")

channel_dir = os.path.join(transcript_dir, channel_requested)

if not os.path.exists(channel_dir):
    os.makedirs(channel_dir)
    print("Directory", channel_dir, "Created ")

os.chdir(channel_dir)


# ============================================
#  Determine Delta between today and last transcript       
# ============================================
# list all the filenames in the directory
filenames = os.listdir()
# sort them from old to new
filenames.sort()
filenames.reverse()
latest_filename = filenames[1]
# get the date of the latest transcript
latest_date = latest_filename[:10]
# datetime object of today's date
from datetime import date, datetime
today = date.today()
# convert the date of the latest transcript to datetime object
latest_date = datetime.strptime(latest_date, '%Y-%m-%d').date()
# calculate the difference between today and the latest transcript
delta = today - latest_date

# ask the user and ask whether to change the max_requests to the delta (y or n)
if delta.days > 0:
    print(f"Last transcript is from {latest_date} which is {delta.days} days ago.")
    print(f"Change max_requests to {delta.days}? (y or n)")
    answer = input()
    if answer == "y":
        max_request = delta.days
        print(f"max_requests changed to {max_request}")
    else:
        print(f"max_requests remains {max_request}")
# ============================================


counter = 0
while counter < max_request:
    counter += 1
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={transcripts_dic[channel_requested]}&part=snippet,id&order=date&maxResults={max_request}"
    # if next_page_token:
    #     url += f"&pageToken={next_page_token}"

    response = requests.get(url).json()

    # if there is a error message in the response, print it and exit
    if 'error' in response.keys():
        logging.error(response['error']['message'])
        exit()

    # print the length of the items in response
    # print(len(response['items']))

    for item in response['items']:
        counter += 1
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_date = item['snippet']['publishedAt'][:10]

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except:
            logging.warning(f"Video {video_id} with date: {video_date} does not have a transcript.")
            continue

        filename = f"{video_date}_{video_title}.txt"
        a = filename
        # delete characters that are not allowed in filenames
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            filename = filename.replace(char, '')

        print(filename)

        # first create a new text file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Url to video: {youtube_url}watch?v={video_id}\n\n")
            for line in transcript:
                url_youtube = f"https://youtu.be/{item['id']['videoId']}?t="
                timestamp = int(line['start'])
                f.write(line['text'] + "  " + url_youtube + str(timestamp) + '\n')

        logging.info(f"Transcript exported to file: {filename}")
        # provide a log of nth video out of max request
        if response['items'].index(item) % 10 == 0:
            logging.info(f"Video {response['items'].index(item)} out of {max_request} exported.")

        logging.info(f"the date of the video is: {video_date}")

        
    # next_page_token = response.get('nextPageToken')
    # if not next_page_token:
    #     break

logging.info("Script finished.")
#

# get a list of mentioned Proper names

# remove weblinks with re: 
# \s*http.+

# extract all proper names from the text (they are cased by YoutubeTranscriptApi)
# (?<!^)(Dr )*[A-Z][a-zA-Z]{2,} [A-Z][a-zA-Z]{2,}|(?<!^)(Dr )*[A-Z][a-zA-Z]+

# leftoff / TODO
# - scan the output folder to see the date of the latest transcript; prompt the user to adapt the max request