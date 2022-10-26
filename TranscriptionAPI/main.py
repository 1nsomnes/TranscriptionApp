from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
import youtube_dl
import whisper
import os 

app = Flask(__name__)
api = Api(app)
CORS(app) #allow cors 

ydl_opts = {
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

transcribe_req_args = reqparse.RequestParser()
transcribe_req_args.add_argument("video_url", type=str, help="YouTube video URL to transcribe from.", required=True)
transcribe_req_args.add_argument("translate", type=str, help="Should the transcription be translated (null for no, two letter language identifier for yes).", required=True)

class Transcribe(Resource):
  def post(self):
    args = transcribe_req_args.parse_args()

    if is_supported(args["video_url"]) == False:
      return {"whisper-response" : "YouTube URL provided is invalid."}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([args["video_url"]])
      info_dict = ydl.extract_info(args["video_url"])
      
      path = "Downloads/" + info_dict.get("title", None) + ".mp3"

    model = whisper.load_model("base")
    result = model.transcribe(path)

    os.remove(path)

    return { "whisper-response" : result["text"] }

api.add_resource(Transcribe, "/transcribe")

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=4999, debug=True)