FROM golang:1.12.17-alpine3.11 AS build

VOLUME /build

WORKDIR /app

COPY . .

RUN apk add --no-cache git gcc upx -q \
  && go test \
  && GOOS=linux GOARCH=386 go build -a -gcflags=all="-l -B" -ldflags="-w -s" -o /build/build.run . \
  && upx --best --ultra-brute /build/build.run \
  && stat -c %s /build/build.run

CMD [ "" ]