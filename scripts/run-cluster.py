import argparse
import copy
import json
import queue
import shutil
import signal
import subprocess
import threading
from pathlib import Path
from typing import List

import shared


class Node:

    def __init__(self, path: Path, subcommand, name):
        q = queue.Queue()
        pid = queue.Queue()
        t = threading.Thread(target=Node.run_inst, args=(path / 'thin', q, pid, subcommand, name), daemon=True)
        t.start()
        q.put('start')
        self.name = name
        self.pid = pid.get()
        self.queue = q

    @staticmethod
    def run_inst(path: Path, q, pid, subcommand, name):
        inst = None
        while True:
            command = q.get()
            if command == 'start':
                if inst and inst.poll() is None:
                    inst.terminate()
                    inst.wait()
                    print(f'node {name} interrupted')
                server_go = [
                    str(path), subcommand, '--log-mode=1',
                    '--secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S'
                ]
                print(' '.join(server_go))
                inst = subprocess.Popen(server_go, start_new_session=True, cwd=path.parent)
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


def read_commands(servers: List[Node]):
    while True:
        command = input()
        parts = command.split(' ')
        action = parts[0]
        if action == 'status':
            for s in servers:
                s.queue.put('status')
        else:
            node = None
            for s in servers:
                if s.name == parts[1]:
                    node = s
            if node is None:
                print('invalid node name')
                continue
            if action == 'start':
                node.queue.put('start')
            elif action == 'stop':
                node.queue.put('stop')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, required=True)
    args, _ = parser.parse_known_args()

    shared.build_and_upload_servers()

    servers = []
    base_path = Path.cwd() / 'cluster'
    shutil.rmtree(base_path, ignore_errors=True)
    with open('config.json', 'r') as f:
        config_origin = json.load(f)

    for i in range(args.size):
        config = copy.deepcopy(config_origin)
        if i == 0:
            path = base_path / 'master'
            subcommand = 'master'
            config['Node'] = {
                'Name': 'node_0',
                'Nodes': {}
            }
            for j in range(1, args.size):
                config['Node']['Nodes'][f'node_{j}'] = f'https://go.tvbit.local:85{j:02}'
            shutil.copytree('keys', path / 'keys')
        else:
            path = base_path / str(i)
            subcommand = 'slave'
            config['Node'] = {
                'ServerAddress': f'go.tvbit.local:85{i:02}'
            }
        config['StatisticsApi']['ServerAddress'] = f'go.tvbit.local:83{i:02}'
        config['StatisticsApi']['ServerAddressSSL'] = f'go.tvbit.local:84{i:02}'
        config['StatisticsApi']['ExternalServerAddress'] = f'http://go.tvbit.local:83{i:02}'
        config['StatisticsApi']['ExternalServerAddressSSL'] = f'https://go.tvbit.local:84{i:02}'
        config['Api']['ServerAddress'] = f'go.tvbit.local:81{i:02}'
        config['Api']['ServerAddressSSL'] = f'go.tvbit.local:82{i:02}'
        config['Api']['ExternalServerAddress'] = f'go.tvbit.local:81{i:02}'
        config['Api']['SecureWebSocketURL'] = f'wss://go.tvbit.local:82{i:02}/ws'
        config['Api']['ApiURL'] = f'http://go.tvbit.local:81{i:02}/api'
        config['Api']['SecureApiURL'] = f'https://go.tvbit.local:82{i:02}'
        path.mkdir(parents=True, exist_ok=True)
        shutil.copy2('server.key', path)
        shutil.copy2('server-dist/thin', path)
        with open(path / 'config.json', 'w') as f:
            json.dump(config, f)
        servers.append(Node(path, subcommand, f'node_{i}'))

    t = threading.Thread(target=read_commands, args=(servers,), daemon=True)
    t.start()

    print('servers', servers)
    signal.sigwait([signal.SIGINT])
    print('sigint received')
    for s in servers:
        s.queue.put('stop')
        s.queue.join()


main()
