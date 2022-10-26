FROM python:3.10.8-bullseye

RUN apt-get update && apt-get install ffmpeg -y

RUN pip install flask==2.2.2 \
    pip install flask_restful==0.3.9 \ 
    pip install Flask-Cors==3.0.10 \
    pip install youtube_dl==2021.12.17 \
    pip install git+https://github.com/openai/whisper.git \
    pip install setuptools-rust==1.5.2
    
WORKDIR /Users/cedricclaessens/Documents/programming/python/TranscriptionApp-WhisperEnd

COPY . . 

EXPOSE 4999

CMD ["python", "main.py"]
