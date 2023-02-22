FROM node:latest

COPY . .

RUN npm install 

EXPOSE 4998

CMD ["npm", "run", "dev", "--", "--port", "4998", "--host"]