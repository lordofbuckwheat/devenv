import json
import os
import subprocess
import time

import psutil
import requests


def wait_for_it(url):
    while True:
        try:
            print(requests.get(url, {'action': 5}))
            break
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(1)


def send_request(url, params):
    resp = requests.post(url, files=params)
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    else:
        print('request', url, params, resp)


def main():
    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
    subprocess.run(['go', 'build', '--tags=dev', '-o', '/home/nikita/devenv/wd/server-go-thin', '.'], check=True)
    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
    subprocess.run(['go', 'build', '--tags=dev', '-o', '/home/nikita/devenv/wd/server-go-dist', 'main.go'], check=True)
    os.chdir('/home/nikita/devenv/wd')

    with open('config.json', 'r') as f:
        cfg = json.load(f)
    auth_key = 'AUTH_KEY'
    cfg['Node'] = {
        'ServerAddress': 'go.tvbit.local:4567',
        'AuthKey': auth_key
    }
    with open('config_slave.json', 'w') as f:
        json.dump(cfg, f)
    subprocess.run(['ls', '-la'], check=True)
    process = subprocess.Popen(['./server-go-thin', 'slave', '--config=config_slave.json', '--log-mode=1'])
    url = 'https://go.tvbit.local:4567/node-service'
    wait_for_it(url)

    # self-update
    with open('server-go-thin', 'rb') as f:
        send_request(url, {
            'action': (None, 2),
            'file': ('server-go-thin_new', f),
            'sign': (None, auth_key)
        })
    process.wait()
    wait_for_it(url)
    time.sleep(1)

    # send node names
    send_request(url, {
        'action': (None, 1),
        'data': (None, json.dumps({
            'Name': 'node_1',
            'Master': 'node_0',
            'Nodes': {
                'node_0': 'https://go.tvbit.local:4567',
                'node_1': 'https://go.tvbit.local:4567'
            }
        })),
        'sign': (None, auth_key)
    })
    time.sleep(1)

    # send fat server update
    with open('server-go-dist', 'rb') as f:
        send_request(url, {
            'action': (None, 3),
            'file': ('fat-server_new', f),
            'sign': (None, auth_key)
        })
    time.sleep(1)

    for proc in psutil.process_iter():
        if proc.name() == 'server-go-thin':
            print(proc.pid)
            proc.terminate()
            proc.wait()


main()
