import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--norace', dest='race', action='store_false')
parser.add_argument('--server_url', dest='server_url', default='https://go.tvbit.local:18286')
parser.add_argument('--uuid', dest='uuid', default='linux-dummy')
parser.add_argument('--title', dest='title', default='linux-dummy-device')
parser.add_argument('--account_key', dest='account_key',
                    default='FqakvRXAJWgxs3IJhap97kYu0CRklFlomg40sbq1YVErm9o2XkNGPwtR3bGnEVEG0rwE3m3BzsaH+FR2ow7nH8NS2qojZB9w40ImLJ1H/r5U8EhJQKkFX/JI1XZHPuuex4gAB5+ZuH2spB8HQ3onXOamciDsAQ1WMDxVV7f7dr4EIMD6cj8axJ2dArz09Jhzp1wK6+kh/DEELDp1RI0PMNqQK5a/hc3uN/7WVkmOxTMFfrnBRHvPJLPAx2F1f2ozylEoEhNrXiMj5VApe3385KVm7mhlLaygtKe8TqF7r3DOCOTqmDACF+gcixi/vWmrEN7NiVFwPuVuUC42FBkcvNzMnUJCckGmEkhOkiUWMxd26WtrBLLYlwg6wrKfR38SNk2xhxfcu5EshhxAhs+s761Qdlo9D0IYM2NFFjCXQDusB53AoTysseFwn4JLUbYzbGXa81wBwXUn8MbvJeuA8+8S31LV1RLf6uGP22DyHAX8wsa9ZAwaBP1sQgn3AJvXRSAGEOFBvje6yuuyeY8dJkynhZ9xB9KzXLCWHsrzbvLfaRpvLoGSZji2Ew640HMfidi6OB1cgE5ALZxdTPAgc4ZvwhaFpdYNuYjSXtzhyr5jX81620HffMG0Iyo0PR2cGgoTBYyKj4EGvO7ilgdZgB7I6r1YxhqjQWepCf9Mr6o=')
args, _ = parser.parse_known_args()
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

os.chdir('/root/wd')

with open('run-linux-client.sh', 'w') as f:
    f.write('\n'.join([
        '#!/bin/bash',
        'set -eo pipefail',
        f"./tvbit-client start --server_url='{args.server_url}' --account_key='{args.account_key}' --title='{args.title}' --uuid='{args.uuid}' --electron_path='electron-dist/ui' --dev",
    ]))
os.chmod('run-linux-client.sh', 0o755)
with open('install-linux-client.sh', 'w') as f:
    f.write('\n'.join([
        '#!/bin/bash',
        'set -eo pipefail',
        f"./tvbit-client install --server_url='{args.server_url}' --account_key='{args.account_key}' --title='{args.title}' --electron_path='electron-dist/ui' --dev",
    ]))
os.chmod('install-linux-client.sh', 0o755)
