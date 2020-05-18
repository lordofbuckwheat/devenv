import argparse
import os
import subprocess
import signal

parser = argparse.ArgumentParser()
parser.add_argument('--config')
parser.add_argument('--norace', dest='race', action='store_false')
args, _ = parser.parse_known_args()
os.chdir('/root/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
go_build = ['go', 'build', '-o', '/root/wd/server-go', 'main.go']
if args.race:
    go_build.insert(2, '--race')
print(' '.join(go_build))
subprocess.run(go_build, check=True)
os.chdir('/root/wd')
server_go = ['./server-go', '--secret=ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S']
if args.config:
    server_go.append(f"--config={args.config}")
with subprocess.Popen(server_go):
    signal.signal(signal.SIGINT, lambda signum, frame: print('Signal handler called with signal', signum))
