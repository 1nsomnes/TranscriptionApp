# transcriber


[![Transcriber Demo](https://github.com/user-attachments/assets/e2f88e14-7a57-4307-9fd1-44f947377a08)](https://www.youtube.com/watch?v=x13DVv8h8Ac&ab_channel=Insomnes)
<sub> transcriber brief demo (no audio) </sub>
<br><br>
Transcriber takes YouTube links and allows you to transcribe them using [OpenAI's Whisper](https://github.com/openai/whisper). It also enables users to download mp3 and mp4 versions of YouTube videos however, be aware that this is against _YouTube ToS_ which is why this project is not actually used. The original goal was to help my dad get transcriptions for Buddhist talks which he likes to read and take notes on. As an additional exercise I've also added the follwing features:
- Threaded requests. Each request is threaded, you can download multiples videos and transcriptions simultaneously
- Multi Request Tracking. You can track all you requests on the home page and each request has it's own page.
- Request progress tracking. You get live updates about the progress of request, albeit a bit unstrctured. 

There are some features that I wanted to implement but never got around to it like live transcription (among a couple of other things that you'll notice).

## Stack & Technology 

For this project I used Python and Flask as a backend and Vue.js for the frontend. Additionally, the frontend and backend are designed to run in their own [Docker](https://www.docker.com/) containers and the whole project is orchestrated using [Docker Compose](https://docs.docker.com/compose/). For the transcription, I used OpenAI whisper. At the time this was super cool because it had come out a couple of weeks earlier, it was state of the art, and ChatGPT-3.0 had not come out yet. Alas, tech grow's old fast and so has this project, but I am still happy with my work! 
   
I wrote the HTML/CSS on this project completely on my own and I tried to make it look good-- most of my previous projects have looked horrendous. As such I tried to follow some basic design principles from Deiter Rams' [10 Principles of Good Design](https://www.heurio.co/dieter-rams-10-principles-of-good-design). I am no Picasso but for a person of my design sense I am quite happy with how it turned out.

## Running Transcriber
You must have docker ~~and the docker-compose CLIs~~ installed in order for this application to work. Once you have done so run
```
docker-compose up —build
```
and both services should go up after being built. The front end can be accessed on your localhost at port 4998 (`localhost:4998`). And if you would like to make API calls you may at `localhost:4999`. I have not documented the API however it is fairly straight forward and is located in `app.py`


