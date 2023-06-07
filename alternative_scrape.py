# TODO:
# - check the delta between the video dates or the number of the episode
# - add a timestamp at the end of every line


from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s') # logging the time, level and message 
# besides info, there are also debug, warning, error, critical, which do:
# logging.info("Script started.")
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

api_key = "AIzaSyDZlegWZl3Mbi7xGPgOnB3qbQXD5EkbSCg"
max_request = 1000
youtube_url = "https://www.youtube.com/" # youtube url


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

channel_requested = "peter_attia"

# Set up YouTube channel ID and transcript export directory
path = os.getcwd()
channel_id = transcripts_dic[channel_requested]

# join: join the path and the channel name
os.path.join(path, channel_requested)

# Create a directory to store the transcripts in if it doesn't already exist
if not os.path.exists('transcripts'):
    os.makedirs('transcripts')
    os.chdir('transcripts')
    if not os.path.exists(channel_requested):
        os.makedirs(channel_requested)
        print("Directory ", channel_requested, " Created ")
os.chdir('transcripts')
if not os.path.exists(channel_requested):
        os.makedirs(channel_requested)
        print("Directory ", channel_requested, " Created ")


transcript_dir = os.path.join(os.getcwd(), 'transcripts')

# Download the last 10 videos from the channel
url = "https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults={}".format(api_key, channel_id, max_request)
response = requests.get(url).json()

# Extract the transcript text for each video and write it to a file
for item in response['items']:
    try:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_date = item['snippet']['publishedAt'][:10]  # Extract the date from the datetime string
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Create the transcript export file with the video title and date in the filename
        filename = "{}_{}.txt".format(video_date, video_title)
        # replace invalid characters in the filename
        filename = filename.replace(':', ';').replace('?', '').replace('/', '').replace('"', '').replace('|', '').replace('*', '').replace('<', '').replace('>', '').replace('\\', '')
        filepath = os.path.join(transcript_dir, filename)
    except:
        logging.warning("Video {} does not have a transcript.".format(video_id))
        continue

    # Write the transcript text to the export file:
    with open(os.path.join(channel_requested, filename), "w", encoding="utf-8") as f:
    # with open(filepath, "w", encoding="utf-8") as f:
        f.write("Url to video: {}watch?v={}\n\n".format(youtube_url, video_id))
        for line in transcript:
            url_youtube = f"https://youtu.be/{item['id']['videoId']}?t="
            # round the timestamp to the lower second
            timestamp = int(line['start']) 
            # TD for tomorrow I want to add a timestamp at the end of every line

            f.write(line['text'] + "  " + url_youtube + str(timestamp) + '\n')

    # Log the filename of the transcript that was created
    logging.info("Transcript exported to file: {}".format(filepath))

# Log a message indicating that the script has finished
logging.info("Script finished.")
