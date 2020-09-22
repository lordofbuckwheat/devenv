import os
import subprocess

os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
subprocess.run(['go', 'build', '--tags=dev', '-o', '/home/nikita/devenv/wd/server-go-dist', 'main.go'], check=True)
print('success')
