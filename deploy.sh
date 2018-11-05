#!/usr/bin/env bash

# .secrets를 starging area에 추가.
git add -f .secrets/

# eb deploy 실행.
eb deploy --profile fc-8th-eb-second --staged

# .secrets를 staging area에서 제거
git reset HEAD  .secrets/

