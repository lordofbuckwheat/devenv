import os
import shutil
import subprocess

import requests


def build_servers(dev: bool):
    shutil.rmtree('/home/nikita/devenv/wd/server-dist', ignore_errors=True)
    os.mkdir('/home/nikita/devenv/wd/server-dist')

    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
    args = ['go', 'build', '-o', '/home/nikita/devenv/wd/server-dist/fat']
    if dev:
        args.append('--tags=dev')
    args.append('main.go')
    subprocess.run(args, check=True)

    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
    args = ['go', 'build', '-o', '/home/nikita/devenv/wd/server-dist/thin']
    if dev:
        args.append('--tags=dev')
    args.append('.')
    subprocess.run(args, check=True)

    os.chdir('/home/nikita/devenv/wd')


def build_and_upload_servers():
    build_servers(False)
    version = subprocess.check_output(['./server-dist/thin', 'version'], text=True).strip()
    with open('server-dist/thin', 'rb') as f:
        requests.post('https://master.tvbit.local:10443', {
            'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
            'controller': 'server',
            'action': 'upload',
            'type': 0,
            'version': version,
            'description': version,
            'server_license_id': 0,
            'commit': ''
        }, files={
            'file': f
        })

    version = subprocess.check_output(['./server-dist/fat', '--version'], text=True).strip()
    with open('server-dist/fat', 'rb') as f:
        requests.post('https://master.tvbit.local:10443', {
            'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
            'controller': 'server',
            'action': 'upload',
            'type': 1,
            'version': version,
            'description': version,
            'server_license_id': 0,
            'commit': ''
        }, files={
            'file': f
        })
