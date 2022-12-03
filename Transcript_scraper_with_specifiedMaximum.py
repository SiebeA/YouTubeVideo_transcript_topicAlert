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

# %% Inferring_pre_existing_transcript_file_by_FirstLastName_UserInput
def Inferring_pre_existing_transcript_file_by_FirstLastName_UserInput(
        transcriptFile_Title_requested):
  
    import re
    import glob
    
    user_confirmation = None
    os.chdir(dir_oldTranscripts)
    Old_Transcripts = [f for f in glob.glob('*txt')]

    for pre_existing_transcript_file in Old_Transcripts:
        if transcriptFile_Title_requested.split('_')[0].lower() in re.split("_| ", pre_existing_transcript_file.lower()) or transcriptFile_Title_requested.split('_')[1].lower() in re.split("_| ", pre_existing_transcript_file.lower()):
                print('\n We infer that this is the latest transcript file :\n\n',
                  pre_existing_transcript_file, '\n')
                user_confirmation = input("Enter on the following line whether this is the right transcript txt file? yes/no\n\n")
                if user_confirmation.lower() == 'yes':
                    transcriptFile_Title_requested = pre_existing_transcript_file
                    newTranscript = False
                    break
            # newTranscript = False  # then the transcript must also exist
            
        # break  # break out of the for loop when the first match is found
        
    if user_confirmation != 'yes': # if the requested channel name is not found in list old transcripts
        newTranscript = True

    if newTranscript == False:
        with open(pre_existing_transcript_file, encoding='utf8') as file:
            a_strings_transcripts_existing = file.read()
            # determining the most recent date of the transcriptfile
            datetime_lastVid = datetime.strptime(
                a_strings_transcripts_existing[4:12], '%y-%m-%d')
            delta = datetime.today() - datetime_lastVid
            print(
                f'\n It has been *** {delta.days} *** days since the latest transcript in our latest output file till today ')
            _ = input('Continue? y/n \n')
            if _ == 'n':
                exit
            return pre_existing_transcript_file, newTranscript, delta, datetime_lastVid
        
    else:
        delta = None
        pre_existing_transcript_file = False
        return pre_existing_transcript_file, newTranscript, delta, datetime_lastVid

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
        max_videos = delta.days  # specify how many videos have to be incluced #bug is when the channel uploads more videos per day, then some will be missed conversely, if <1 a day, too many will be requested

    b_json_files = []
    youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50"
    response = urlopen(youtubeChannelMetaDataUrl)
    data_json = json.loads(response.read()) # contains the data for 50 videos
    
    
    
    # if the date of the last video in the batch is moreRECENT than datetime_lastVid, then  get a new nextPageToken, otherwise stop
    

    b_json_files.append(data_json)
    if max_videos > 50:  # we require a nextpagetoken to extract additional metadata
        i = 0
        nextPageToken = ""
        # dont waste quota asking for more tokens than our maxvideo count requires; (for 120 videos: 50 first token, cum100 for 1 add, cum 150 1)
        while counter != (ceil(max_videos/100*2)-1) and 'nextPageToken' in b_json_files[i].keys():
            
            # # date of least recent video in the batch:
            last_date_batch = data_json['items'][40]['snippet']['publishedAt'][:10]
            last_date_batch = datetime.strptime(last_date_batch, '%Y-%m-%d') # convert to a datetime object
            
            
            # if statement could be added to the while, but this is for easier comprehension in the future.
            
            # a date  > == greater == moreRecent
            if last_date_batch > datetime_lastVid:
                print('\n new page token required as the least recent video in the batch is newer than the most recent transcript in our old transcript file \n')
                nextPageToken = b_json_files[i]['nextPageToken']
                youtubeChannelMetaDataUrl = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=50&pageToken={nextPageToken}"
                response = urlopen(youtubeChannelMetaDataUrl)
                data_json = json.loads(response.read())
                b_json_files.append(data_json)
                i += 1
                print(f" nextpagetoken nr.:{counter}")
                counter += 1
                
            else:
                return b_json_files, max_videos
                
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

    # convert all dates to datetime objects without time
    date_vids = [datetime.strptime(i, '%Y-%m-%d') for i in date_vids]
    date_vids = [i.date() for i in date_vids] # remove the time from the datetime objects

    for date in date_vids:
        if date <= datetime_lastVid.date():
            max_videos_adjusted = date_vids.index(date)
            print(f"max_videos = {max_videos}")
            break

    print(f'\n\n a total of {max_videos_adjusted} transcripts will be scraped\n')


    # create a dictionary with the date_vids as keys and the ids_vids and title_vids as values
    # dict_vids = {date_vids[i]: [ids_vids[i], title_vids[i]] for i in range(len(date_vids))} # IMPROVE later, use a dic instead of sepeate values


    return date_vids, title_vids, ids_vids, fail, max_videos_adjusted

# %% transcriptDownloader
def transcriptDownloader(ids_vids, date_vids, title_vids, max_videos_adjusted):
    '''
    Downloading the actual Transcripts using thw YoutubeData-API

    '''
    from youtube_transcript_api import YouTubeTranscriptApi
    transcripts = YouTubeTranscriptApi.get_transcripts(
        video_ids=ids_vids[:max_videos_adjusted], continue_after_error=True)

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
    """
    Returns
    -------
    new_transcripts_str : STR
        Extracts the texts, and organizes the text by putting the correct
            video-details at the top. format:
                index of transcript
                Date of transcript/video
                video-id
                video-title
    """
    counter = 0
    new_transcripts_str = ""
    # for i in range(10): #(len(transcripts[0])):
    for key, date, title, idd in zip(transcripts[0], date_vids, title_vids, ids_vids):
        if max_videos > 200:
            print(date)
        new_transcripts_str += str(counter)+"\n" + \
            str(date) + "\n"+idd+"\n" + title + "\n\n"
        for i in transcripts[0][key]:  # so all the
            # the text is written under the date,id,title
            new_transcripts_str += i['text']+" "
        new_transcripts_str += "\n\n"
        counter += 1
    print('the dates of the added transcripts hereabove\n ')
    return new_transcripts_str

# %% export
def exporter(pre_existing_transcript_file, transcripts):
   
    import re
    import os
    
    """
    Parameters
    ----------
    pre_existing_transcript_file : str
        DESCRIPTION.
    transcripts : tuple

    Returns
    -------
    None. either updates the pre-existing transcripts text file on dir, or creates a new one
    """
    if newTranscript == False:
        # we need the dates of the preexisting file in order to open it (and write the new transcripts to ti)
        datesinTextFile = re.findall(
            "\d{4}-\d{2}-\d{2}", pre_existing_transcript_file)
        
        # OPEN pre-existing transcript file:
        with open(pre_existing_transcript_file, "r", encoding="utf-8") as text_file:
            pre_existing_transcript_str = text_file.read()
        
        # EXPORT only the new transcripts
        datesinTextFile = re.findall(
            "\d{4}-\d{2}-\d{2}", new_transcripts_str)
        # latest_transcript_date = new_transcripts_str[2:12]
        with open(f'Transcript_batches/Transcript_batchesnew_transcripts_str_{channelRequested}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt', "w", encoding="utf-8") as text_file:
            # dont overwrite the file, but append to it
            text_file.write(new_transcripts_str)
        
    
    
    
        updated_transcript  = transcripts + pre_existing_transcript_str
    
        with open(f'transcript_{channelRequested}_between_{datesinTextFile[0]}_and_{datesinTextFile[-1]}.txt', "w", encoding="utf-8") as text_file:
            # dont overwrite the file, but append to it
            text_file.write(updated_transcript)

    else:
        print('else')
        datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", transcripts)



    # will be used to name the transcript file with earliest and latest transcript date in the title
    # datesinTextFile = re.findall("\d{4}-\d{2}-\d{2}", transcripts)
    
    datesin_preExisting_TextFile = re.findall(
        "\d{4}-\d{2}-\d{2}", pre_existing_transcript_str)
    datesin_preExisting_TextFile = datesin_preExisting_TextFile[-1]
    
    os.rename(os.path.abspath(text_file.name),
              f'transcript_{channelRequested}_between_{datesinTextFile[0]}_and_{datesin_preExisting_TextFile}.txt')
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
    import time
    from datetime import datetime

    os.chdir("/home/Insync/Convexcreate@gmail.com/GD/Engineering/Development/PY_YouTubeVideo_transcript_topicAlert")
    with open('api_key.txt', 'r') as file:
        api_key = file.read().replace('\n', '')
    dir_oldTranscripts = "Output/"

    # FUNCTIONS:
    start_time = time.time()
    channelRequested, channel_Id = Inferring_ChannelRequest_by_FirstLastName_UserInput(
        transcripts_dic)
    print('time it took to infer the channel in secs:',round(time.time() - start_time))    

    start_time = time.time()
    pre_existing_transcript_file, newTranscript, delta,datetime_lastVid = Inferring_pre_existing_transcript_file_by_FirstLastName_UserInput(
        channelRequested)
    print('time it took to infer the latest transcript in secs:',round(time.time() - start_time))

    start_time = time.time()
    b_json_files, max_videos = json_storer(newTranscript, delta)
    print('time it took to store the json files in secs:',round(time.time() - start_time))

    start_time = time.time()
    date_vids, title_vids, ids_vids, fail, max_videos_adjusted = youtubeMetaDataExtractor(
        max_videos)
    print('time it took to extract the metadata in secs:',round(time.time() - start_time))

    start_time = time.time()
    transcripts = transcriptDownloader(
        ids_vids, date_vids, title_vids, max_videos_adjusted)
    print('time it took to download the transcripts in secs:',round(time.time() - start_time))

    start_time = time.time()
    new_transcripts_str = textTranscriptExtractor(transcripts)
    print('time it took to extract the text in secs:',round(time.time() - start_time))

    start_time = time.time()
    exporter(pre_existing_transcript_file, new_transcripts_str)
    print('time it took to export the text in secs:',round(time.time() - start_time))
