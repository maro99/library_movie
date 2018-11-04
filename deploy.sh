#!/usr/bin/env bash

# requirements만들기
pipenv lock --requirements > requirements.txt

# .secrets와 requriements를 starging area에 추가.
git add -f .secrets/ requirements.txt

# eb deploy 실행.
eb deploy --profile fc-8th-eb-second --staged

# .secrets와 requirements를 staging area에서 제거
git reset HEAD requirements.txt, .secrets

# requriements.txt 삭제
rm -f requirements.txt