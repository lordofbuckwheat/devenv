import os
import shutil
import subprocess

import requests
from packaging import version


def get_server_version(conf, t, license_id=None):
    licenses = {0}
    if license_id:
        licenses.add(license_id)
    seq = [version.parse(x['version']) for x in conf if x['type'] == t and set(x['license_ids']).intersection(licenses)]
    return max(seq) if len(seq) else version.parse('')


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


def build_and_upload_servers(server_url, forced, license_id=None):
    build_servers(False)
    fat_version = version.parse(
        subprocess.check_output(['/home/nikita/devenv/wd/server-dist/fat', '--version'], text=True).strip()
    )
    thin_version = version.parse(
        subprocess.check_output(['/home/nikita/devenv/wd/server-dist/thin', 'version'], text=True).strip()
    )
    remote_versions = requests.post(server_url, {
        'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
        'controller': 'index',
        'action': 'info'
    }).json()['data']['server_distributes']
    fat_remote_version = get_server_version(remote_versions, 1, license_id)
    fat_remote_global_version = get_server_version(remote_versions, 1)
    thin_remote_version = get_server_version(remote_versions, 0, license_id)
    thin_remote_global_version = get_server_version(remote_versions, 0)
    if fat_remote_version < fat_version <= fat_remote_global_version:
        raise Exception('invalid fat version')
    if thin_remote_version < thin_version <= thin_remote_global_version:
        raise Exception('invalid thin version')
    print('remote versions', remote_versions)
    print(f'fat version {fat_remote_version} -> {fat_version}')
    print(f'fat global version {fat_remote_global_version}')
    print(f'thin version {thin_remote_version} -> {thin_version}')
    print(f'thin global version {thin_remote_global_version}')
    print('license_id', license_id)
    if not forced:
        while True:
            choice = input('continue? [y/n]')
            if choice == 'y':
                break
            elif choice == 'n':
                return
    if fat_version > fat_remote_version:
        with open('/home/nikita/devenv/wd/server-dist/fat', 'rb') as f:
            resp = requests.post(server_url, {
                'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
                'controller': 'server',
                'action': 'upload',
                'type': 1,
                'version': fat_version,
                'description': fat_version,
                'server_license_id': license_id if license_id is not None else 0,
                'commit': 'head'
            }, files={
                'file': f
            })
            print(resp.text)
        print('fat uploaded')
    if thin_version > thin_remote_version:
        with open('/home/nikita/devenv/wd/server-dist/thin', 'rb') as f:
            resp = requests.post(server_url, {
                'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
                'controller': 'server',
                'action': 'upload',
                'type': 0,
                'version': thin_version,
                'description': thin_version,
                'server_license_id': license_id if license_id is not None else 0,
                'commit': 'head'
            }, files={
                'file': f
            })
            print(resp.text)
        print('thin uploaded')
