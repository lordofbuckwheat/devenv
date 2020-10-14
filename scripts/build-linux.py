import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--norace', dest='race', action='store_false')
args = parser.parse_args()
os.chdir('/root/app/electron-core')
subprocess.run(['npm', 'install'], check=True)
subprocess.run(['npm', 'run', 'dist'], check=True)
shutil.rmtree('/root/wd/electron-dist', ignore_errors=True)
shutil.move('dist/linux-unpacked', '/root/wd/electron-dist')

os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/wd/tvbit-client', '.']
if args.race:
    go_build.insert(2, '--race')
print(go_build)
subprocess.run(go_build, check=True)
