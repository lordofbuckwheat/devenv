import argparse
import subprocess

import requests
from packaging import version

import shared


def get_server_version(conf, t, license_id=None):
    licenses = {0}
    if license_id:
        licenses.add(license_id)
    return max(
        [version.parse(x['version']) for x in conf if x['type'] == t and set(x['license_ids']).intersection(licenses)]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-url', dest='server_url', type=str)
    parser.add_argument('--license-id', type=int, dest='license_id')
    args = parser.parse_args()
    shared.build_servers(False)
    fat_version = version.parse(
        subprocess.check_output(['/home/nikita/devenv/wd/server-dist/fat', '--version'], text=True).strip()
    )
    remote_versions = requests.post(args.server_url, {
        'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
        'controller': 'index',
        'action': 'info'
    }).json()['data']['server_distributes']
    print('remote versions', remote_versions)
    fat_remote_version = get_server_version(remote_versions, 1, args.license_id)
    thin_remote_version = get_server_version(remote_versions, 0, args.license_id)
    if fat_version > fat_remote_version:
        with open('/home/nikita/devenv/wd/server-dist/fat', 'rb') as f:
            resp = requests.post(args.server_url, {
                'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
                'controller': 'server',
                'action': 'upload',
                'type': 1,
                'version': fat_version,
                'description': fat_version,
                'server_license_id': args.license_id if args.license_id is not None else 0,
                'commit': 'asd'
            }, files={
                'file': f
            })
            print(resp.text)
        print(f'fat uploaded {fat_remote_version} -> {fat_version}')
    thin_version = version.parse(
        subprocess.check_output(['/home/nikita/devenv/wd/server-dist/thin', 'version'], text=True).strip()
    )
    if thin_version > thin_remote_version:
        with open('/home/nikita/devenv/wd/server-dist/thin', 'rb') as f:
            resp = requests.post(args.server_url, {
                'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
                'controller': 'server',
                'action': 'upload',
                'type': 0,
                'version': thin_version,
                'description': thin_version,
                'server_license_id': args.license_id if args.license_id is not None else 0,
                'commit': 'asd'
            }, files={
                'file': f
            })
            print(resp.text)
        print(f'thin uploaded {thin_remote_version} -> {thin_version}')


main()
