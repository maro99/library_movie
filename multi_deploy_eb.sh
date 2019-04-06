#!/usr/bin/env bash

# .secrets를 starging area에 추가.
git add -f .secrets/

# 프론트 프로젝트 로컬로 클론 해옴.
git clone git@github.com:maro99/library_movie_frontend.git front

rm -rf front/.git

# root_url dev환경 맞게 변경
cat front/js/address_variable_eb.js > front/js/address_variable.js

# 프론트 프로젝트 git에 추가.
git add -f front

# eb deploy 실행.
eb deploy --profile fc-8th-eb-second --staged

# .secrets를 staging area에서 제거
git reset HEAD  .secrets/

# front를 staging area에서 제거
git reset HEAD front

# 프론트 프로젝트 로컬에서 제거.
rm -rf front