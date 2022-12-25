# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:18.8.0 as build-stage


WORKDIR /app
COPY package*.json /app/
COPY ./nginx.conf ./nginx.conf
RUN npm install

COPY ./ /app/

# Comment out the next line to disable tests
# RUN npm run test:unit
RUN npm i -g vite
RUN npm run build
# ARG FRONTEND_ENV=production

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15

COPY ./nginx-backend-not-found.conf ./backend-not-found.conf
COPY --from=build-stage /app/dist/ /usr/share/nginx/html

COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
