FROM                nadcdc/fc-8th-eb-docker:base
MAINTAINER          nadcdc4@gmail.com

#이하 production에서 복사.

ENV             PROJECT_DIR     /srv/project
ENV                 BUILD_MODE              production

#nginx ,supervisor install
ENV                 DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}


# Copy projects files
COPY            .   ${PROJECT_DIR}
#WORKDIR         ${PROJECT_DIR}

# 로그파일 기록 위한 폴더 생성
RUN             mkdir /var/log/django


# Ngnix config
RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx.conf \
                  /etc/nginx/nginx.conf && \

            # available에 nginx_app.conf파일 복사
            cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx_app.conf \
                        /etc/nginx/sites-available/ && \

            # 이미 sites-enabled에 있던 모든 내용 삭제
            rm -f   /etc/nginx/sites-enabled/* && \

            # available에 있는 nginx_app.conf를 enabled로 링크.
            ln -sf  /etc/nginx/sites-available/nginx_app.conf \
                   /etc/nginx/sites-enabled


# Supervisor 설정복사
RUN             cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/supervisor.conf \
                        /etc/supervisor/conf.d

# 7000번 포트 open
EXPOSE          7000


# RUN supervisor
CMD             supervisord -n