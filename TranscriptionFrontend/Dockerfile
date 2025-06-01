FROM node:latest

# stop node from stopping because it takes too much memory
ENV NODE_OPTIONS="--max-old-space-size=4096"

COPY . .
RUN npm install 

EXPOSE 4998

CMD ["npm", "run", "dev", "--", "--port", "4998", "--host"]
