# %%Inferring_ChannelRequest_by_FirstLastName_UserInput
def Inferring_ChannelRequest_by_FirstLastName_UserInput(transcripts_dic):
   
    import re
    
    """
    Input: DICT K: STR:first and lastnames; V: STR
    Returns: 2 STRINGS: transcriptFile_Title_requested, channel_Id
    """

    for transcript in transcripts_dic.keys():
        print(transcript)
    transcript_requested = input(
        "\n Which transcript is requested? format: [firstname_lastname]: \n")

    for string in list(transcripts_dic.keys()):
        # if either of the names in input are in either of the names of the split, i.e. 'sam harris' if 'sam_har', NOT if 'sa_har'
        if transcript_requested.split('_')[0].lower() in re.split("_| ", string.lower()) or transcript_requested.split('_')[1].lower() in re.split("_| ", string.lower()):
            print(f'\n this is the inferred transcript file request:\n\n ---{string}--- \n')
            channelRequested = string
    user_confirmation = input(
        "\n Enter on the following line whether this is the right transcript txt file? yes/no\n\n")
    if user_confirmation.lower() != 'yes':
        for key in transcripts_dic.keys():
            print(key)
        channelRequested = input(
            "\n Enter the name of the transcript txt file on the following line:\n")
    channel_Id = transcripts_dic[channelRequested]

    return channelRequested, channel_Id

# %% Inferring_LatestLatestTranscriptFile_by_FirstLastName_UserInput
def Inferring_LatestLatestTranscriptFile_by_FirstLastName_UserInput(
        transcriptFile_Title_requested):
  
    import re
    import glob
    import sys

    user_confirmation = None
    os.chdir(dir_oldTranscripts)
    Old_Transcripts = [f for f in glob.glob('*txt')]

    for LatestLatestTranscriptFile in Old_Transcripts:
        if transcriptFile_Title_requested.split('_')[0].lower() in re.split("_| ", LatestLatestTranscriptFile.lower()) or transcriptFile_Title_requested.split('_')[1].lower() in re.split("_| ", LatestLatestTranscriptFile.lower()):
            print('\n We infer that this is the latest transcript file :\n\n',
                  LatestLatestTranscriptFile, '\n')
            # transcriptFile_Title_requested = LatestLatestTranscriptFile
            user_confirmation = input(
                "Enter on the following line whether this is the right transcript txt file? yes/no\n\n")
            if user_confirmation.lower() == 'yes':
                newTranscript = False  # then the transcript must also exist
            
            else:
                newTranscript = True
            break  # break out of the for loop when the first match is found

    from datetime import datetime
    with open(LatestLatestTranscriptFile, encoding='utf8') as file:
        a_strings_transcripts_existing = file.read()
        # determining the most recent date of the transcriptfile
        datetime_lastVid = datetime.strptime(
            a_strings_transcripts_existing[4:12], '%y-%m-%d')
        delta = datetime.today() - datetime_lastVid
        print(
            f'\n It has been *** {delta.days} *** days since the latest transcript in our latest output file till today ')
        _ = input('Continue? y/n \n')
        if _ == 'n':
            sys.exit(0)

    return LatestLatestTranscriptFile, newTranscript,  delta

# %% json_storer
def json_storer(newTranscript, delta):
   
    from urllib.request import urlopen
    import json
    from math import ceil
    
    """
    # stores the video meta-data; including Ids required for downloading next
    """
    counter = 0

    if newTranscript == True:
        max_videos = 1000  # specify how many videos are included
    else:
        max_videos = delta.days  # specify how many videos have to be incluced #bug is when the channel uploads more videos per day, then some will be missed.

    b_json_files = []
    youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50"
    response = urlopen(youtubeChannelMetaDataUrl)
    data_json = json.loads(response.read())
    b_json_files.append(data_json)
    if max_videos > 50:  # we require a nextpagetoken to extract additional metadata
        i = 0
        nextPageToken = ""
        # dont waste quota asking for more tokens than our maxvideo count requires; (for 120 videos: 50 first token, cum100 for 1 add, cum 150 1)
        while counter != (ceil(max_videos/100*2)-1) and 'nextPageToken' in b_json_files[i].keys():
            nextPageToken = b_json_files[i]['nextPageToken']
            youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50&pageToken={nextPageToken}"
            response = urlopen(youtubeChannelMetaDataUrl)
            data_json = json.loads(response.read())
            b_json_files.append(data_json)
            i += 1
            print(f" nextpagetoken nr.:{counter}")
            counter += 1
        print(youtubeChannelMetaDataUrl)
    return b_json_files, max_videos

# %% youtubeMetaDataExtractor
def youtubeMetaDataExtractor(max_videos):
    """
    Returns
    -------
    date_vids : list
    title_vids : list
    ids_vids : list
    fail : list
        If e.g. the video-id value is not present in the dic, an exeption will be made
            and the dict will be appended to dict={fail} instead of dict={metaDataYoutubeVideo}
    """
    fail = []
    metaDataYoutubeVideo = []
    for i in b_json_files:
        try:
            for ii, key in enumerate(i['items']):  # ii is just for debuggin
                metaDataYoutubeVideo.append(
                    (key['snippet']['publishedAt'][:10], key['snippet'], key['id']['videoId']))
        except:
            fail.append(i)

    date_vids = [i[0] for i in metaDataYoutubeVideo][:max_videos]
    title_vids = [i[1]['title'] for i in metaDataYoutubeVideo][:max_videos]
    ids_vids = [i[2] for i in metaDataYoutubeVideo][:max_videos]

    return date_vids, title_vids, ids_vids, fail

# %% transcriptDownloader
def transcriptDownloader(ids_vids, date_vids, title_vids, max_videos):
    '''
    Downloading the actual Transcripts using thw YoutubeData-API

    '''
    import time
    start_time = time.time()

    from youtube_transcript_api import YouTubeTranscriptApi
    transcripts = YouTubeTranscriptApi.get_transcripts(
        video_ids=ids_vids[:max_videos], continue_after_error=True)

    print('time it took in secs to download the transcripts :',
          round(time.time() - start_time))

    '''
    correcting for missing transcripts
    '''
    # when a transcript is missing, we need to make new lists of the other transcript meta data, otherwise wrong transcripts are attributed to the wrong metaData s.a. date or ID

    # storing date and title as keys corresponding to the ids\values
    dic = {i: (f, d) for i, f, d in zip(ids_vids, date_vids, title_vids)}

    for i in transcripts[1]:
        try:
            dic.pop(i)
        except:
            continue

    # after correction, some of the videos metadata:
    ids_vids = [i[0] for i in dic.items()]
    date_vids = [i[1][0] for i in dic.items()]
    title_vids = [i[1][1] for i in dic.items()]

    return transcripts


#%%=======================#
'      organizing the downloaded transcripts; filter out text (not timestamps)'
#========================= #
def textTranscriptExtractor(transcripts):
    import time
    """
    Returns
    -------
    transcript_txtFile : STR
        Extracts the texts, and organizes the text by putting the correct
            video-details at the top. format:
                index of transcript
                Date of transcript/video
                video-id
                video-title
    """
    start_time = time.time()
    counter = 0
    transcript_txtFile = ""
    # for i in range(10): #(len(transcripts[0])):
    for key, date, title, idd in zip(transcripts[0], date_vids, title_vids, ids_vids):
        transcript_txtFile += str(counter)+"\n" + \
            date + "\n"+idd+"\n" + title + "\n\n"
        for i in transcripts[0][key]:  # so all the
            # the text is written under the date,id,title
            transcript_txtFile += i['text']+" "
        transcript_txtFile += "\n\n"
        counter += 1
    print('time it took to extract the text in secs:',
          round(time.time() - start_time))
    return transcript_txtFile

# %% export
def exporter(LatestLatestTranscriptFile, transcripts):
   
    import re
    import os
    
    """
    Parameters
    ----------
    LatestLatestTranscriptFile : str
        DESCRIPTION.
    transcripts : tuple
        DESCRIPTION.

    Returns
    -------
    None. either updates the pre-existing transcripts text file on dir, or creates a new one
    """
    if newTranscript != True:
        # we need the dates of the preexisting file in order to open it (and write the new transcripts to ti)
        datesinTextFile = re.findall(
            "\d{4}-\d{2}-\d{2}", LatestLatestTranscriptFile)
    else:
        datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", transcripts)

    with open(f'transcript_{channelRequested}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt', "w", encoding="utf-8") as text_file:
        text_file.write(transcripts)

    # will be used to name the transcript file with earliest and latest transcript date in the title
    datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", transcripts)
    os.rename(os.path.abspath(text_file.name),
              f'transcript_{channelRequested}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt')
    # print("Output File: {}".format(os.path.abspath(text_file.name)), f'Output/transcript_{channelTitle}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt')

# %% ==========================================================
# Execute
# ==========================================================
# go to a youtube page > 'inspect' > r'channelId'
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
    "jordan_peterson": "UCL_f53ZEJxp8TtlOkHwMV9Q"}

if __name__ == '__main__':

    import os
    os.chdir("/home/Insync/Convexcreate@gmail.com/GD/Engineering/Development/D_YouTubeVideo_transcript_topicAlert")
    with open('api_key.txt', 'r') as file:
        api_key = file.read().replace('\n', '')
    dir_oldTranscripts = "Output/"

    # FUNCTIONS:
    channelRequested, channel_Id = Inferring_ChannelRequest_by_FirstLastName_UserInput(
        transcripts_dic)

    LatestLatestTranscriptFile, newTranscript, delta = Inferring_LatestLatestTranscriptFile_by_FirstLastName_UserInput(
        channelRequested)

    b_json_files, max_videos = json_storer(newTranscript, delta)

    date_vids, title_vids, ids_vids, fail = youtubeMetaDataExtractor(
        max_videos)

    transcripts = transcriptDownloader(
        ids_vids, date_vids, title_vids, max_videos)

    transcripts = textTranscriptExtractor(transcripts)

    # i0=succesfull i2=unsuccesful in transcript extraction
    transcripts = transcriptDownloader(
        ids_vids, date_vids, title_vids, max_videos)

    transcripts_str = textTranscriptExtractor(transcripts)

    exporter(LatestLatestTranscriptFile, transcripts_str)
