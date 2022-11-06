from flask import Flask, send_file, Response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import youtube_dl
import whisper
import os
import threading
from request_manager import RequestManager, UrlRequest

app = Flask(__name__)
api = Api(app)
CORS(app)  # allow cors

mp3_opts = {
    'ignoreerrors': True,
    'outtmpl': 'Downloads/%(title)s.%(etx)s',
    'format': 'bestaudio/best',
    'no_check_certificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'prefer_ffmpeg': True
}


def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False


transcribeyt_args = reqparse.RequestParser()
transcribeyt_args.add_argument(
    "video_url", type=str, help="YouTube video URL to transcribe from.", required=True)
transcribeyt_args.add_argument(
    "translate", type=str, help="Should the transcription be translated (null for no, two letter language identifier for yes).", required=True)

downloadyt_args = reqparse.RequestParser()
downloadyt_args.add_argument(
    "video_url", type=str,  help="YouTube video URL to download from.", required=True)


class RequestProgress(Resource):
    def get(self):
        return RequestManager.get_progress(1)

class RequestFilename(Resource):
    def get(self):

        return {}


class RequestResult(Resource):
    def post(self):
        
        return {}

# YouTube URL --> Transcription
class TranscribeYT(Resource):
    def post(self):
        args = transcribeyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            return "URL submitted was invalid...", 500

        # create new request

        return {"request-number", 1}

        with youtube_dl.YoutubeDL(mp3_opts) as ydl:
            ydl.download([args["video_url"]])
            info_dict = ydl.extract_info(args["video_url"])

            path = "Downloads/" + info_dict.get("title", None) + ".mp3"

        model = whisper.load_model("base")
        result = model.transcribe(path)

        os.remove(path)

        return {"whisper-response": result["text"]}


# YouTube Downloader
class DownloadYT(Resource):
    def phook(self, d):
        RequestManager.request_items[1].progress = d

    def post(self):
        args = downloadyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            return Response("URL submitted was invalid...", status=500)

        requestNum = RequestManager.create_request(UrlRequest(args["video_url"], 0, "Result.mp4"))

        mp4_opts = {
            'format': 'bestvideo[height<=?720]+bestaudio[ext=m4a]/best',
            'outtmpl': f'Requests/{str(requestNum)}/' + 'Result.%(ext)s',
            'progress_hooks': [self.phook]
        }

        def downloadYt():
            with youtube_dl.YoutubeDL(mp4_opts) as ydl:
                ydl.download((args['video_url'],)) #use when python only recognizes first letter of string

        t = threading.Thread(name="thred", target=downloadYt)
        t.setDaemon(True)
        t.start()
        
        return {"request-number": str(requestNum)}
            


api.add_resource(DownloadYT, "/downloadyt")
api.add_resource(TranscribeYT, "/transcribeyt")
api.add_resource(RequestProgress, "/rprogress")

# only used when not in docker container
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4999, debug=True)
