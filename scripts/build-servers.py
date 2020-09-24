import os
import shutil
import subprocess

shutil.rmtree('/home/nikita/devenv/wd/server-dist', ignore_errors=True)
os.mkdir('/home/nikita/devenv/wd/server-dist')
os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
subprocess.run(['go', 'build', '--tags=dev', '-o', '/home/nikita/devenv/wd/server-dist/fat.ex', 'main.go'], check=True)
os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
subprocess.run(['go', 'build', '--tags=dev', '-o', '/home/nikita/devenv/wd/server-dist/thin.ex', '.'], check=True)
print('success')
