
from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests

api_key = "AIzaSyDZlegWZl3Mbi7xGPgOnB3qbQXD5EkbSCg"

# Set up YouTube channel ID and transcript export directory
channel_id = "UCfpnY5NnBl-8L7SvICuYkYQ"
transcript_dir = os.path.join(os.getcwd(), 'transcripts')

# download the last 10 videos from the channel
url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&maxResults=10&order=date&type=video&key={}".format(channel_id, api_key)
response = requests.get(url).json() # this is a dictionary



# Extract the transcript text for each video
for item in response['items']:
    video_id = item['id']['videoId']
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Create the transcript export file
    filename = video_id + ".txt"
    filepath = os.path.join(transcript_dir, filename)

    # Write the transcript text to the export file
    with open(filepath, "w", encoding="utf-8") as f:
        for line in transcript:
            f.write(line['text'] + '\n')
