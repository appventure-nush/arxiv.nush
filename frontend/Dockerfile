FROM busybox:musl

RUN adduser -D static
USER static
WORKDIR /home/static

COPY /dist .
EXPOSE 3000
CMD ["busybox", "httpd", "-f", "-v", "-p", "3000"]