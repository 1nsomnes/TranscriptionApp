FROM python:3.10.8-bullseye

RUN apt-get update && apt-get install ffmpeg -y

RUN pip install flask==2.2.2 \
    pip install flask_restful==0.3.9 \ 
    pip install Flask-Cors==3.0.10 \
    pip install youtube_dl==2021.12.17 \
    pip install git+https://github.com/openai/whisper.git \
    pip install setuptools-rust==1.5.2 \
    pip install gunicorn 

COPY . . 

#recent update to youtube messed up the way the extractor works
#implemented the solution found here: https://forum.videohelp.com/threads/408650-No-longer-able-to-download-videos-with-youtube-dl-exe 
#and copied it into my container
RUN rm /usr/local/lib/python3.10/site-packages/youtube_dl/extractor/youtube.py
COPY ./youtube.py /usr/local/lib/python3.10/site-packages/youtube_dl/extractor
RUN rm ./youtube.py


EXPOSE 4999

#CMD ["gunicorn", "--bind", "0.0.0.0:4999", "wsgi:app"] stops mid process with wsgi and gunicorn 
CMD ["python3", "app.py"]