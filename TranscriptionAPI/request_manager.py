import os
import threading;
import youtube_dl

class UrlRequest:
    def __init__(self, url:str, filename:str, request_num:int):
        self.url = url
        self.filename = filename

class YtDownloadManager(threading.Thread):
    progress = "Loading..."
    request_info:UrlRequest

    def progressUpdate(self,d):
        global progress
        progress = d

    def __init__(self, request_info:UrlRequest):
        self.request_info = request_info
        super().__init__()

    def run(self):
        global request_info
        global progressUpdate

        mp4_opts = {
            'format': 'bestvideo[height<=?720]+bestaudio[ext=m4a]/best',
            'outtmpl': f'Requests/{str(request_info.request_num)}/{request_info.filename}',
            'progress_hooks': [progressUpdate]
        }
        
        with youtube_dl.YoutubeDL(mp4_opts) as ydl:
                ydl.download((request_info.url,)) #use when python only recognizes first letter of string

class TranscriptionManager(threading.Thread):
    progress = "Loading..."

    def __init__(self, request_info:UrlRequest):
        
        super().__init__()