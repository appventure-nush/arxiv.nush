FROM python:3.9-slim-buster as builder

COPY . .
RUN pwd && ls -l

FROM nginx:alpine
EXPOSE 80
COPY --from=builder /dist /usr/share/nginx/html