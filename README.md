# YouTubeVideo_transcript_topicAlert

Application goal:

  Say you follow a channel, or podcast on Youtube, you are interested in particular topics that they cover, but since they put out hours of content every X days, you want to be more efficient with the attention you allocate to the channel, then this script can help you. 

 Returns the video's metadata, matches of keywords and their context (and keyword combinations) of a specificed Youtube channel. 
 
 You do need a Youtube data API (freely available via https://console.cloud.google.com/)
 
Still under development, but functional until and including: 

file: Transcript_scraper_with_specifiedMaximum.py
    1. The transcripts are downloaded with the YoutubeDataAPI
      - maximum number of videos can be specified
      - If it's the first time a channel is specified, a new txt file is created ; else: the transcripts of the new videos are appended to the old one 
    2. The transcripts are neatly organized in a String, with the MetaData above it; plus, the txt files with all the transcripts are saved to disk under the channel's name and the dates of oldest and newest transcripts
file: Transcript_scraper NLP analysis.py
    3. user-inputted keyword returns the videos in which the keyword occurred. 
   
 
