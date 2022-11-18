from flask import Flask, send_file, Response, make_response, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import youtube_dl
import os, shutil
from request_manager import YtDownloadManager, TranscriptionManager, UrlRequest

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
downloadyt_args.add_argument("format", type=str, help="The format of the video, mp3 or mp4.")


class RequestProgress(Resource):
    def get(self, index):
        global request_threads
        response = make_response(request_threads[index].progress, 200)
        response.mimetype = "text/plain"

        return response


class RequestResult(Resource):
    def get(self, index):
        base_path = f"Requests/{index}/"
        filename = os.listdir(base_path)[0]

        response = make_response(send_file(base_path + filename, as_attachment=True, download_name=filename))
        response.headers['Access-Control-Expose-Headers'] = "Content-Disposition"

        return response

# YouTube URL --> Transcription
class TranscribeYT(Resource):
    def post(self):
        global request_index

        args = transcribeyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            return "URL submitted was invalid...", 500

        index = request_index
        path = f"Requests/{index}"

        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            os.mkdir(path)

        request_threads[index] = TranscriptionManager(UrlRequest(args["video_url"], f"Result.txt", index))
        request_threads[index].start()

        request_index = request_index + 1

        return {"request-number": str(index)}


# YouTube Downloader
class DownloadYT(Resource):
    def post(self):
        global request_index
        
        args = downloadyt_args.parse_args()

        if is_supported(args["video_url"]) == False:
            return Response("URL submitted was invalid...", status=500)

        if args["format"] != "mp3" and args["format"] != "mp4":
            return Response("Format is not an options. Please use mp3 or mp4.", 500)
        
        file_format = args["format"]
        index = request_index
        path = f"Requests/{index}"

        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            os.mkdir(path)

        request_threads[index] = YtDownloadManager(UrlRequest(args["video_url"], f"Result.{file_format}", index), file_format)
        request_threads[index].start()

        request_index = request_index + 1
        
        return {"request-number": str(index)}
            


api.add_resource(DownloadYT, "/downloadyt")
api.add_resource(TranscribeYT, "/transcribeyt")
api.add_resource(RequestProgress, "/rprogress/<int:index>")
api.add_resource(RequestResult, "/rdownload/<int:index>")

# only used when not in docker container
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4999, debug=True)
