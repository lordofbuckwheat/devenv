import json
import os
import subprocess

os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
subprocess.run(['go', 'build', '--tags=dev', '-o', '/home/nikita/devenv/wd/server-go-thin', '.'], check=True)
os.chdir('/home/nikita/devenv/wd')
with open('config.json', 'r') as f:
    cfg = json.load(f)
cfg['Node'] = {
    'ServerAddress': 'go.tvbit.local:4567',
    'AuthKey': 'AUTH_KEY'
}
with open('config_slave.json', 'w') as f:
    json.dump(cfg, f)
subprocess.run(['ls', '-la'], check=True)
thin = subprocess.Popen(['./server-go-thin', 'slave', '--config=config_slave.json'])
thin.wait()
