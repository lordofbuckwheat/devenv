import argparse
import copy
import json
import os
import queue
import shutil
import signal
import subprocess
import threading
from pathlib import Path

import requests

AUTH_KEY = 'I29WQM5iOncE1wAjR8all2oCAFvFNgnHBQOT8WEjD5Sc6esAJ141CyXz02KR7xPR'


class Node:

    def __init__(self, path: Path, config, name):
        path.mkdir(parents=True, exist_ok=True)
        if not path.samefile('/home/nikita/devenv/wd'):
            shutil.copy2('/home/nikita/devenv/wd/server-go-thin', path)
        with open(path / 'config.json', 'w') as f:
            json.dump(config, f)
        q = queue.Queue()
        pid = queue.Queue()
        t = threading.Thread(target=Node.run_inst, args=(path / 'server-go-thin', q, pid, name), daemon=True)
        t.start()
        q.put('start')
        self.name = name
        self.pid = pid.get()
        self.queue = q

    @staticmethod
    def run_inst(path: Path, q, pid, name):
        inst = None
        while True:
            command = q.get()
            if command == 'start':
                if inst and inst.poll() is None:
                    inst.terminate()
                    inst.wait()
                    print(f'node {name} interrupted')
                os.chdir(path.parent)
                server_go = [
                    str(path), 'run', '--log-mode=1',
                    '--secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S'
                ]
                print(' '.join(server_go))
                inst = subprocess.Popen(server_go, start_new_session=True)
                print(f'node {name} started')
                pid.put(inst.pid)
            elif command == 'stop':
                if inst and inst.poll() is not None:
                    print(f'node {name} already stopped')
                else:
                    inst.terminate()
                    inst.wait()
                    print(f'node {name} stopped')
            elif command == 'status':
                st = inst.poll()
                if st is None:
                    print(f'node {name} is running')
                else:
                    print(f'node {name} exited with code {st}')
            elif command == 'reload':
                if inst.poll() is None:
                    inst.send_signal(signal.SIGHUP)
            q.task_done()

    def __repr__(self):
        return f'{self.name}: {self.pid}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cluster', type=int)
    args, _ = parser.parse_known_args()
    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
    subprocess.run(['go', 'build', '-o', '/home/nikita/devenv/wd/server-go-thin', '.'], check=True)
    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
    subprocess.run(['go', 'build', '-o', '/home/nikita/devenv/wd/server-go-dist', 'main.go'], check=True)
    os.chdir('/home/nikita/devenv/wd')
    version = subprocess.check_output(['./server-go-dist', '--version'], text=True).strip()
    with open('server-go-dist', 'rb') as f:
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
    servers = []
    base_path = Path.cwd()
    with open('config.json', 'r') as f:
        config_origin = json.load(f)
    if args.cluster is not None:
        base_path = base_path / 'cluster'
        config = copy.deepcopy(config_origin)
        shutil.rmtree(base_path, ignore_errors=True)
        config['Node'] = {
            'AuthKey': AUTH_KEY,
            'Name': 'node_0',
            'Master': 'node_0',
            'Nodes': {},
        }
        for i in range(1, args.cluster):
            config['Node']['Nodes'][f'node_{i}'] = f'https://go.tvbit.local:80{i:02}'
        master_path = base_path / 'master'
        master_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2('/home/nikita/devenv/wd/server.key', master_path)
        shutil.copytree('/home/nikita/devenv/wd/keys', master_path / 'keys')
        servers.append(Node(master_path, config, 'master'))
        for i in range(1, args.cluster):
            config = copy.deepcopy(config_origin)
            config['Node'] = {
                'AuthKey': AUTH_KEY,
                'Name': f'node_{i}',
                'Master': 'node_0',
            }
            config['StatisticsApi']['ServerAddress'] = f'go.tvbit.local:83{i:02}'
            config['StatisticsApi']['ServerAddressSSL'] = f'go.tvbit.local:83{i:02}'
            config['StatisticsApi']['ExternalServerAddress'] = f'http://go.tvbit.local:83{i:02}'
            config['StatisticsApi']['ExternalServerAddressSSL'] = f'https://go.tvbit.local:83{i:02}'
            config['Api']['ServerAddress'] = f'go.tvbit.local:82{i:02}'
            config['Api']['ServerAddressSSL'] = f'go.tvbit.local:82{i:02}'
            config['Api']['ExternalServerAddress'] = f'go.tvbit.local:82{i:02}'
            config['Api']['WebSocketURL'] = f'ws://go.tvbit.local:82{i:02}/ws'
            config['Api']['SecureWebSocketURL'] = f'wss://go.tvbit.local:82{i:02}/ws'
            config['Api']['ApiURL'] = f'http://go.tvbit.local:82{i:02}/api'
            config['Api']['SecureApiURL'] = f'https://go.tvbit.local:82{i:02}'
            servers.append(Node(base_path / str(i), config, f'node_{i}'))
    else:
        for p in base_path.glob("tvbit_1_*"):
            p.unlink(True)
        (base_path / 'fatserver.txt').unlink(True)
        servers.append(Node(base_path, config_origin, "mono"))
    print('servers', servers)
    signal.sigwait([signal.SIGINT])
    print('sigint received')
    for s in servers:
        s.queue.put('stop')
        s.queue.join()


main()
