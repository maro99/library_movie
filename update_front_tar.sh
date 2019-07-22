#!/usr/bin/env bash  

# 프론트 프로젝트 로컬로 클론 해옴.
git clone git@github.com:maro99/library_movie_frontend.git front

rm -rf front/.git

# root_url  배포환경 맞게 변경
cat front/js/address_variable_eb.js > front/js/address_variable.js

# front.tar로 압축     
tar -cvf front.tar front   

# 프론트 프로젝트 로컬에서 제거.
rm -rf front





