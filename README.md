# atm. only working on Ubuntu

# What the Transcript_scraper_with_specifiedMaximum script will provide you
Execute the file in its entirety and provide input to the prompts. This will provide you with a text_file with meta-data and transcripts of all the YouTube-channel's video, in the format of:

```
*FORMAT:
index of transcript
Date of transcript/video
video-id
video-title

text of the video-transcript (N lines)
```


# Checks and HowTo:

- Check: whether your api_key is (still) valid
- Run the entire `Transcript_scraper_with_specifiedMaximum.py`to import the transcripts and create one big `txt` file (if an older txt file already exists, the new transcripts are appended to the old file)
- Set the 3 parameters at the top of the `Transcript_scraper_NLP_analysis.py` file, and then run the entire script.


# Troubleshoot
If not all transcripts seem to be imported:
​    - Newest videos have not generated a transcript yet by YouTube


## TODO

###                                   Transcript_scraper_NLP_analysis.py
- analyse the newest_transcript_batch for a channel


###                                   Transcript_scraper_with_specifiedMaximum.py
#### Need to haves:
- Store a pickle for every {newest_transcript_batch} for each channel; this should be updated every time the transcript scraper script is run; because the NLP analysis script will only process that updated newest transcript file (analyzing all will not be timely informative and slow); do cumulative_transcripts will be saved seperately for a different analysis


- IMPR-speed: textTranscriptExtractor function
- error when the script is executed on a channel that was already executed the same day (datetime referred before)
- Provide option to only download new transcript;
    - output 2 text files: {new_transcripts} {cumulative_transcripts}
- provide the youtube url in the video data
- FeatureIdea: get remote_latest_video date from a channel (https://www.googleapis.com/youtube/v3/search?key=AIzaSyDZlegWZl3Mbi7xGPgOnB3qbQXD5EkbSCg&channelId=UCNAxrHudMfdzNi6NxruKPLw&part=snippet,id&order=date&maxResults=X compare it with most_recent local_transcript_date IF it reaches X new videos THEN automatically update a transcript file of a video
- print new lines instead of one line, see if colouring works
- provide the youtube url in the video data

- Searching for 2 patterns close together
- Parametrize an option to Only import last X transcripts (if you want recent search alerts, you don't need the older transcripts')
- put multiple wordOfinterest matches in the same video under only 1 metadata
- make it faster; now the writing? is very slow.
    - Identify the bottleNeck
    - Only import last X transcripts (if you want recent search alerts, you don't need the older transcripts')
## Nice to Haves
- Not compatible for Windows yet: make it dynamic by creating the specific folders in def exporter()
- execute the script WHEN system startup
- for Transcripts, instead of cutting of at 200, cut of at a word boundary
- in [Transcript_scraper_with_specifiedMaximum]: Automatically delete the older version of the transcript file
- enable the program to search sub-word-patterns (now only whole word patterns are searchable with re.findall)
- Return a link with a timestamp embedded
- Summarizing periods in the videos, especially Scott adams, returning a time frame in which he e.g. speaks of 'ego', or 'Trump'
- inability to handle >1 videos per day
- when videos per day uploaded by a channel, it does not count towards the nubmer of videos that need to be downloaded, as the assumption is that max 1 video per day will be uploaded, is this still the case?

## Bug & resolvement (learning purposes)
- when transcript is unavaible for a given ID, the next transcript is being written under the ID that was unavailable
- '[zZ]uck' does not return matches, 'Zuckerberg' does.
    - a_matches_KeywordψContext = re.findall(wordOfInterestψContext, a_strings_transcripts) > '(.{200})(zuck)(\\s.{200})' e.g. 'zuck' is a part of a word, because the regex searches for a space surrounding it, it returns no matches.


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
