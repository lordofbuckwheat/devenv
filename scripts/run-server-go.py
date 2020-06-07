import argparse
import os
import subprocess
import json
import re
import queue
import threading
import signal


class ServerReady(Exception):
    pass


def run_inst(file, config, q, pid, i):
    inst = None
    while True:
        command = q.get()
        if command == 'start':
            if inst and inst.poll() is None:
                inst.terminate()
                inst.wait()
                print(f'server {i} interrupted')
            server_go = ['./server-go', '--secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
                         f"--config={config}"]
            f = open(file, 'w')
            print(' '.join(server_go))
            inst = subprocess.Popen(server_go, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
            print(f'server {i} started')
            pid.put(inst.pid)
        elif command == 'stop':
            if inst and inst.poll() is not None:
                print(f'server {i} already stopped')
            else:
                inst.terminate()
                inst.wait()
                print(f'server {i} stopped')
        elif command == 'status':
            st = inst.poll()
            if st is None:
                print(f'server {i} is running')
            else:
                print(f'server {i} exited with code {st}')
        elif command == 'reload':
            if inst.poll() is None:
                inst.send_signal(signal.SIGHUP)
        elif command == 'proceed':
            if inst.poll() is None:
                inst.send_signal(signal.SIGUSR1)
        q.task_done()


def create_server(file, config, i):
    q = queue.Queue()
    pid = queue.Queue()
    t = threading.Thread(target=run_inst, args=(file, config, q, pid, i), daemon=True)
    t.start()
    q.put('start')
    return pid.get(), q


def signal_handler(signum, frame):
    pass


def read_commands(servers):
    while True:
        command = input()
        parts = command.split(':')
        if parts[0] == 'stop':
            s = servers[int(parts[1])]
            s[1].put('stop')
        elif parts[0] == 'start':
            s = servers[int(parts[1])]
            s[1].put('start')
        elif parts[0] == 'status':
            for s in servers:
                s[1].put('status')
        elif parts[0] == 'reload':
            for s in servers:
                s[1].put('reload')


AUTH_KEY = 'I29WQM5iOncE1wAjR8all2oCAFvFNgnHBQOT8WEjD5Sc6esAJ141CyXz02KR7xPR'
parser = argparse.ArgumentParser()
parser.add_argument('--config', default='config.json')
parser.add_argument('--cluster', type=int)
parser.add_argument('--norace', dest='race', action='store_false')
args, _ = parser.parse_known_args()
os.chdir('/root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
go_build = ['go', 'build', '-o', '/root/wd/server-go', 'main.go']
if args.race:
    go_build.insert(2, '--race')
print(' '.join(go_build))
subprocess.run(go_build, check=True)
os.chdir('/root/wd')
servers = []
if args.cluster is not None:
    args.cluster = 7 if args.cluster > 7 else args.cluster
    with open(args.config, 'r') as f:
        config = json.load(f)
    config['Node'] = {
        'Name': f'node_0',
        'AuthKey': AUTH_KEY,
        'Master': 'node_0',
        'Nodes': {}
    }
    for i in range(args.cluster):
        j = i + 1
        config['Node']['Nodes'][f'node_{j}'] = f'https://go.tvbit.local:82{j}6'
    with open(f'config_0.json', 'w') as f:
        json.dump(config, f)
    servers.append(create_server(f'out.log', f'config_0.json', 0))
    for i in range(args.cluster):
        j = i + 1
        with open(args.config, 'r') as f:
            configRaw = f.read()
        configRaw = re.sub(r':8285(["\/])', rf':82{j}5\1', configRaw)
        configRaw = re.sub(r':8286(["\/])', rf':82{j}6\1', configRaw)
        configRaw = re.sub(r':8385(["\/])', rf':83{j}5\1', configRaw)
        configRaw = re.sub(r':8386(["\/])', rf':83{j}6\1', configRaw)
        configRaw = re.sub(r':18285(["\/])', rf':182{j}5\1', configRaw)
        configRaw = re.sub(r':18286(["\/])', rf':182{j}6\1', configRaw)
        configRaw = re.sub(r':18385(["\/])', rf':183{j}5\1', configRaw)
        configRaw = re.sub(r':18386(["\/])', rf':183{j}6\1', configRaw)
        config = json.loads(configRaw)
        config['Node'] = {
            'Name': f'node_{j}',
            'AuthKey': AUTH_KEY,
            'Master': 'node_0',
            'Nodes': {
                'node_0': 'https://go.tvbit.local:8286'
            }
        }
        for i1 in range(args.cluster):
            j1 = i1 + 1
            if i1 != i:
                config['Node']['Nodes'][f'node_{j1}'] = f'https://go.tvbit.local:82{j1}6'
        with open(f'config_{j}.json', 'w') as f:
            json.dump(config, f)
        servers.append(create_server(f'out-{j}.log', f'config_{j}.json', j))
else:
    servers.append(create_server('out.log', args.config, 0))
print('servers', servers)

t = threading.Thread(target=read_commands, args=(servers,), daemon=True)
t.start()

signal.signal(signal.SIGUSR1, signal_handler)
ready = set()
while True:
    try:
        siginfo = signal.sigwaitinfo([signal.SIGUSR1])
        print('signal received', siginfo)
        for s in servers:
            if s[0] == siginfo.si_pid:
                ready.add(siginfo.si_pid)
        if len(ready) == len(servers):
            print('all servers ready')
            for s in servers:
                s[1].put('proceed')
    except KeyboardInterrupt:
        for s in servers:
            s[1].put('stop')
            s[1].join()
        break
