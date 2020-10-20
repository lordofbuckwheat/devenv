import os
import shutil
import subprocess


def build_servers(dev: bool):
    shutil.rmtree('/home/nikita/devenv/wd/server-dist', ignore_errors=True)
    os.mkdir('/home/nikita/devenv/wd/server-dist')

    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go')
    args = ['go', 'build', '-o', '/home/nikita/devenv/wd/server-dist/fat']
    if dev:
        args.append('--tags=dev')
    args.append('main.go')
    subprocess.run(args, check=True)

    os.chdir('/home/nikita/devenv/app/supertvbit/gopath/src/gitlab.tvbit.co/g/server-go-thin')
    args = ['go', 'build', '-o', '/home/nikita/devenv/wd/server-dist/thin']
    if dev:
        args.append('--tags=dev')
    args.append('.')
    subprocess.run(args, check=True)

    os.chdir('/home/nikita/devenv/wd')
