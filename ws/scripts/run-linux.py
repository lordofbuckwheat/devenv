import argparse
import os
import signal
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-r', dest='redirect', action='store_true')
parser.add_argument('--norace', dest='race', action='store_false')
args, unknown = parser.parse_known_args()
os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/go-wd/linux-client', '.']
if args.race:
    go_build.insert(2, '--race')
print('gobuild', go_build)
subprocess.run(go_build, check=True)
os.chdir('/root/go-wd')
signal.signal(signal.SIGINT, lambda signum, frame: print('Signal handler called with signal', signum))
if args.redirect:
    print('redirecting to /root/go-wd/linux-client.log')
    with open('/root/go-wd/linux-client.log', "w") as outfile:
        subprocess.run(['./linux-client'] + unknown, stdout=outfile, stderr=subprocess.STDOUT, check=True)
else:
    subprocess.run(['./linux-client'] + unknown, check=True)
