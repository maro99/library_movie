#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

MODES = ['base', 'local', 'dev', 'production']


def get_mode():
    # ./build.py --mode <mode>
    # ./build.py -m <mode>
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mode',
        help='Docker build mode [{}]'.format(', '.join(MODES)),
    )
    args = parser.parse_args()

    # 모듈 호출에 옵션으로 mode를 전달한 경우
    if args.mode:
        mode = args.mode.strip().lower()
    # 사용자 입력으로 mode를 선택한 경우
    else:
        while True:
            print('Select mode')
            for index, mode_name in enumerate(MODES, start=1):
                print(f' {index}. {mode_name}')
            selected_mode = input('Choice: ')
            try:
                mode_index = int(selected_mode) - 1
                mode = MODES[mode_index]
                break
            except IndexError:
                print('1 ~ 2번을 입력하세요')
    return mode


def mode_function(mode):
    if mode in MODES:
        cur_module = sys.modules[__name__]
        getattr(cur_module, f'build_{mode}')()
    # if mode == 'base':
    #     build_base()
    # elif mode == 'local':
    #     build_local()
    # elif mode == 'dev':
    #     build_dev()
    else:
        raise ValueError(f'{MODES}에 속하는 모드만 가능합니다')


def build_base():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)
        # docker build
        subprocess.call('docker build -t eb-docker:base -f Dockerfile.base .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


def build_local():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)
        # docker build
        subprocess.call('docker build -t eb-docker:local -f Dockerfile.local .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


def build_dev():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements --dev > requirements.txt', shell=True)
        # docker build
        subprocess.call('docker build -t eb-docker:dev -f Dockerfile.dev .', shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


def build_production():
    try:
        # pipenv lock으로 requirements.txt생성
        subprocess.call('pipenv lock --requirements > requirements.txt', shell=True)
        # docker build
        subprocess.call('docker build -t eb-docker:production -f Dockerfile.production .',
                        shell=True)
    finally:
        # 끝난 후 requirements.txt파일 삭제
        os.remove('requirements.txt')


if __name__ == '__main__':
    mode = get_mode()
    # 선택된 mode에 해당하는 함수를 실행
    mode_function(mode)
