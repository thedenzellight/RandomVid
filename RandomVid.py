from __future__ import unicode_literals
import sys
import os
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import random
from pytube import YouTube as Youtube
import urllib.request
import re
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def create_txt(name):
    try:
        os.system(f'echo.>"e:\\Games\\dataproject\\subtitles\\{name}.txt"')
    except OSError as e:
        print(f"Could not create txt file for {name}.txt")

x = 0
a = int(input("Number of videos to get: "))

while x != a:
    try:
        
        
        path_to_word = 'words.txt'

        wordopen = open(path_to_word).read().splitlines()

        word = random.choice(wordopen)


        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+word)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        video_id = random.choice(video_ids)
        
        link = "https://www.youtube.com/watch?v="+video_id
        
        yt = Youtube(link)
        
        print("Video ID: "+video_id)

        print("Video Name: "+yt.title)
        
        print("Author: "+yt.author)
        
        print("Length "+str(yt.length))
        
        print("Description: "+yt.description)
        
        print("Keywords: "+str(yt.keywords))
        
        srt = YouTubeTranscriptApi.get_transcript(video_id)

        text = ''

        create_txt(str(yt.title)+'.txt')
        
        try:
            with open(str(yt.title), 'w') as file:
                for i in srt:
                    text += i["text"]
                file.write(text+'\n')
                print("Using video named "+word)
                print('wrote subtitles of video')
                print(text[0:60])file.close()
            print("Downloading video from YouTube")
            YouTube(link).streams.first().download()
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([str(link)])
            print("Completed downloading video from YouTube")
            x += 1
        except OSError as e:
            print("[ ERROR ] Name contains bad symbols")
        except UnicodeEncodeError as e:
            print("[ ERROR ] Unicode found")
        
    except youtube_transcript_api.TranscriptsDisabled:
        print("[ ERROR ] video has no subtitles")
    except youtube_transcript_api.NoTranscriptFound:
        print(" [ERROR] Video has no subtitles")
    except youtube_transcript_api.NoTranscriptAvailable:
        print(" [ ERROR ] Video's subtitles are not avaliabe ")
