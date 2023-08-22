FROM node:14-alpine AS development
ENV NODE_ENV development

WORKDIR /app

COPY ./package.json .

COPY ./package-lock.json .

RUN yarn install

COPY . .

EXPOSE 3000

CMD [ "yarn", "start" ]

# This is intentionally for development. In the correct scenario it should use 
# docker multistage builds to reduce image size, and contain a reverse proxy on top 
# the app to serve the built static files and achive better performance and production best practices.