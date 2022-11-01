from flask import Flask, send_file
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
import youtube_dl
import whisper
import os

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

mp4_opts = {
    'format': 'bestvideo[height<=?720]+bestaudio[ext=m4a]/best',
    'outtmpl': 'Downloads/%(title)s.%(ext)s'
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


# YouTube URL --> Transcription
class TranscribeYT(Resource):
    def post(self):
        args = transcribeyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            return {"whisper-response": "YouTube URL provided is invalid."}

        with youtube_dl.YoutubeDL(mp3_opts) as ydl:
            ydl.download([args["video_url"]])
            info_dict = ydl.extract_info(args["video_url"])

            path = "Downloads/" + info_dict.get("title", None) + ".mp3"
        print("\nTest\n")
        model = whisper.load_model("base")
        result = model.transcribe(path)

        os.remove(path)

        return {"whisper-response": result["text"]}


# YouTube Downloader
class DownloadYT(Resource):
    def post(self):
        args = downloadyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            abort(500, "Invalid url")

        with youtube_dl.YoutubeDL(mp4_opts) as ydl:
            ydl.download([args["video_url"]])
            info_dict = ydl.extract_info(args["video_url"])

            path = "Downloads/" + info_dict.get("title", None) + ".mp4"
        print("\nTest\n")
        return send_file(path, mimetype="video/mp4")


api.add_resource(DownloadYT, "/downloadyt")
api.add_resource(TranscribeYT, "/transcribeyt")

#only used when not in docker container
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4999, debug=True)
