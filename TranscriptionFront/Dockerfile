FROM node:latest

WORKDIR /Users/cedricclaessens/Documents/programming/fullstack/TransctiptionApp/TranscriptionFrontend

COPY . .

RUN npm install 

EXPOSE 4998

CMD ["npm", "run", "dev", "--", "--port", "4998", "--host"]