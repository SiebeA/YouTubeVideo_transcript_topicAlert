from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_key = "AIzaSyDZlegWZl3Mbi7xGPgOnB3qbQXD5EkbSCg"
max_request = 10

# Set up YouTube channel ID and transcript export directory
channel_id = "UCfpnY5NnBl-8L7SvICuYkYQ"
transcript_dir = os.path.join(os.getcwd(), 'transcripts')

# Download the last 10 videos from the channel
url = "https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults={}".format(api_key, channel_id, max_request)
response = requests.get(url).json()

# Extract the transcript text for each video and write it to a file
for item in response['items']:
    video_id = item['id']['videoId']
    video_title = item['snippet']['title']
    video_date = item['snippet']['publishedAt'][:10]  # Extract the date from the datetime string
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # Create the transcript export file with the video title and date in the filename
    filename = "{}_{}.txt".format(video_date, video_title)
    # replace invalid characters in the filename
    filename = filename.replace(':', ';').replace('?', '')
    filepath = os.path.join(transcript_dir, filename)

    # Write the transcript text to the export file
    with open(filepath, "w", encoding="utf-8") as f:
        for line in transcript:
            f.write(line['text'] + '\n')

    # Log the filename of the transcript that was created
    logging.info("Transcript exported to file: {}".format(filepath))

# Log a message indicating that the script has finished
logging.info("Script finished.")
