FROM nginx:1.21-alpine

WORKDIR /app/

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir staticfiles