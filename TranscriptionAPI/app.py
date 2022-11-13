from flask import Flask, send_file, Response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import youtube_dl
import whisper
import os, shutil
import threading
from request_manager import YtDownloadManager, UrlRequest

request_threads = {}
request_index = 1

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
        global request_threads
        return request_threads[1].progress

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
    def post(self):
        global request_index
        
        args = downloadyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            return Response("URL submitted was invalid...", status=500)

        index = request_index
        path = f"Requests/{index}"

        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            os.mkdir(path)
        

        request_threads[index] = YtDownloadManager(UrlRequest(args["video_url"], "Result.mp4", index))
        request_threads[index].start()

        request_index = request_index + 1
        
        return {"request-number": str(index)}
            


api.add_resource(DownloadYT, "/downloadyt")
api.add_resource(TranscribeYT, "/transcribeyt")
api.add_resource(RequestProgress, "/rprogress")

# only used when not in docker container
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4999, debug=True)
