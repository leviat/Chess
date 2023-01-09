FROM node:latest

WORKDIR /opt/frontend
COPY ./package*.json .

RUN yarn install

EXPOSE 5173

CMD ["yarn", "dev"]