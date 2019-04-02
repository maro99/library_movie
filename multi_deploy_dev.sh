#!/usr/bin/env bash

# 프론트 프로젝트 로컬로 클론 해옴.
git clone git@github.com:maro99/library_movie_frontend.git front

# 도커 빌드
./build.py -m dev

# 도커 런
docker run --rm -it -p 8000:80 eb-docker:dev

# 프론트 프로젝트 로컬에서 제거.
rm -rf front
