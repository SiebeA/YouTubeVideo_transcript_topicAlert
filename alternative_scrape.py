from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Now the logging level is set to INFO, and the INFO and DEBUG messages will be printed



# source the api key from: "X:\My Drive\Engineering\Development\YouTubeVideo_transcript_topicAlert\api_key.txt"
with open("api_key.txt", "r") as f:
    api_key = f.read()

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

channel_requested = "scott_adams"
next_page_token = None

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
# (?<!^)(Dr )*[A-Z][a-zA-Z]{2,} [A-Z][a-zA-Z]{2,}|(?<!^)(Dr )*[A-Z][a-zA-Z]+

# leftoff
# - 
# - check how much quota
# - check whether it breaks when max is reached;