import argparse
import os
import subprocess
from pathlib import Path
from threading import Thread

import requests


def no_interrupt():
    subprocess.run(
        ['./server-go-thin', 'run', '--secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S'],
        check=True
    )


AUTH_KEY = 'I29WQM5iOncE1wAjR8all2oCAFvFNgnHBQOT8WEjD5Sc6esAJ141CyXz02KR7xPR'
parser = argparse.ArgumentParser()
parser.add_argument('--cluster', type=int)
args, _ = parser.parse_known_args()

os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
subprocess.run(['go', 'build', '-o', '/home/nikita/devenv/wd/server-go-thin', '.'], check=True)
os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
subprocess.run(['go', 'build', '-o', '/home/nikita/devenv/wd/server-go-dist', 'main.go'], check=True)
os.chdir('/home/nikita/devenv/wd')
for p in Path(".").glob("tvbit_1_*"):
    p.unlink(True)
Path('fatserver.txt').unlink(True)
version = subprocess.check_output(['./server-go-dist', '--version'], text=True).strip()
with open('server-go-dist', 'rb') as f:
    r = requests.post('https://master.tvbit.local:10443', {
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
t = Thread(target=no_interrupt)
t.start()
t.join()
