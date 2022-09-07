# YouTubeVideo_transcript_topicAlert


## TODO
- Source the Api key from a txt file, now it cannot be seen on GitHub
- Create executable script, such as `automate.sh`
- Create .venv:
    - youtube_transcript_api
- inability to handle >1 videos per day


## Application goal:

  Say you follow a channel, or podcast on Youtube, you are interested in particular topics that they cover, but since they put out hours of content every X days, you want to be more efficient with the attention you allocate to the channel, then this script can help you.

 Returns the video's metadata, matches of keywords and their context (and keyword combinations) of a specificed Youtube channel.

 You do need a Youtube data API (freely available via https://console.cloud.google.com/)

Still under development, but functional until and including:

file: Transcript_scraper_with_specifiedMaximum.py
file: Transcript_scraper NLP analysis.py

* The transcripts are downloaded with the YoutubeDataAPI
  + maximum number of videos can be specified
  + If it's the first time a channel is specified, a new txt file is created ; else: the transcripts of the new videos are appended to the pre-existing txt file of the channel's exported transcripts
* The transcripts are neatly organized in a String, with the MetaData above it; plus, the txt files with all the transcripts are saved to disk under the channel's name and the dates of oldest and newest transcripts
* user-inputted keyword returns the videos in which the keyword occurred.
* (more functionality coming)


## the full pipeline:
1. Transcript scraper scripts
2. IE: Information extraction
3.
