FROM node:20-alpine AS build
WORKDIR /app
COPY ./app/index.html /app/index.html
COPY ./app/package.json /app/package.json
COPY ./app/vite.config.js /app/vite.config.js
COPY /app/src /app/src
RUN npm install
RUN npm run build

FROM nginx:stable-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]