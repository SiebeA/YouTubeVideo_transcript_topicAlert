
def quickTranscriptScraper(video_id):
    #%% throughput
    from youtube_transcript_api import YouTubeTranscriptApi
    L = YouTubeTranscriptApi.get_transcript(video_id)
    # for i in L:
    #     print(i['start'],"\n",i['text'],"\n")
    # for i in L:
        # print(i['text'] , " "  )
    string = ""
    with open("output_file_transcript.txt", "w") as f:
        for i in L:
            string += (i['text']+'\n ')
            f.write(i['text']+'\n ')
    
# altenratively: replace the new lines in the file (however it makes the colour scheme dissapear)
    # import re
    # string = re.sub("($\n)", " ", string, flags=re.MULTILINE)
    # with open("output_file_transcript2.txt", "w") as f:
    #     f.write(string)
    # print(string)
    # return string

test = quickTranscriptScraper("HbdcD5SAD7Q")        

