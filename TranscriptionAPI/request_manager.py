import os
import threading;
import youtube_dl
import whisper

class UrlRequest:
    def __init__(self, url:str, filename:str, request_num:int):
        self.url = url
        self.filename = filename
        self.request_num = request_num

class YtDownloadManager(threading.Thread):
    progress = "Loading..."
    request_info:UrlRequest
    vformat:str

    def progressUpdate(self,d):
        #print("hook called", flush=True) #flush lets it print to the main thread
        self.progress = d

    def __init__(self, request_info:UrlRequest, vformat:str):
        self.request_info = request_info
        self.vformat = vformat
        super().__init__()

    def run(self):
        mp4_opts = {
            'format': 'bestvideo[height<=?720]+bestaudio[ext=m4a]/best',
            'outtmpl': 'Requests/' + str(self.request_info.request_num) + '/%(title)s.%(ext)s',
            'progress_hooks': [self.progressUpdate]
        }
        mp3_opts = {
            'ignoreerrors': True,
            'outtmpl': 'Requests/' + str(self.request_info.request_num) + '/%(title)s.%(ext)s', #ext will not work wihtout this formatting
            'format': 'bestaudio/best',
            'no_check_certificate': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'prefer_ffmpeg': True,
            'progress_hooks': [self.progressUpdate]
            
        }

        if self.vformat == "mp3":
            opts = mp3_opts
        else:
            opts = mp4_opts

        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download((self.request_info.url,)) #use when python only recognizes first letter of string

        self.progress = "done"
        

class TranscriptionManager(threading.Thread):
    progress = "Loading..."
    request_info:UrlRequest

    def progressUpdate(self,d):
        #print("hook called", flush=True) #flush lets it print to the main thread
        self.progress = d

    def __init__(self, request_info:UrlRequest):
        self.request_info = request_info
        super().__init__()

    def run(self):
        mp3_opts = {
            'ignoreerrors': True,
            'outtmpl': 'Requests/' + str(self.request_info.request_num) + '/%(title)s.%(ext)s', #ext will not work wihtout this formatting
            'format': 'bestaudio/best',
            'no_check_certificate': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'prefer_ffmpeg': True,
            'progress_hooks': [self.progressUpdate]
        }

        with youtube_dl.YoutubeDL(mp3_opts) as ydl:
            ydl.download((self.request_info.url,))

        self.progress = "Machine Learning Algorithms Running..."

        base_path = f"Requests/{self.request_info.request_num}/"
        path = base_path + os.listdir(base_path)[0]

        model = whisper.load_model("base")
        result = model.transcribe(path)

        os.remove(path)

        text_file = open(base_path + "Transcription.txt", "w")
        text_file.write(result["text"])
        text_file.close()

        self.progress = "done"

