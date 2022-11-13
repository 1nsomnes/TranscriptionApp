# TRANSCRIBER!
This is one of hopefully many full stack applications, that I've designed. It takes MP3 files and YouTube Urls and allows you to use OpenAi's Whisper to transcribe them. Backend is designed using flask and frontend is designed using Vue. Both ends are virtualized using Docker and bundled using Docker-Compose. As this is my first project doing full stack development any feedback would be appreciated. Thanks :)  


# Running Transcriber
You must have docker and the docker-compose CLIs installed in order for this application to work. Once you have done so run
```
docker-compose up -d —build
```
and both services should go up after being built. The front end can be accessed on your localhost at port 4998 (`localhost:4998`). And if you would like to make API calls you may at `localhost:4999`. Read information below to see valid API calls.

## API 
WIP

