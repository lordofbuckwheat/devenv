import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--server-url', dest='server_url', default='http://go.tvbit.local:8285')
parser.add_argument('--node', dest='node', type=int)
parser.add_argument('--uuid', dest='uuid', default='linux-dummy')
parser.add_argument('--title', dest='title', default='linux-dummy-device')
parser.add_argument('--account_key', dest='account_key',
                    default='FqakvRXAJWgxs3IJhap97kYu0CRklFlomg40sbq1YVErm9o2XkNGPwtR3bGnEVEG0rwE3m3BzsaH+FR2ow7nH8NS'
                            '2qojZB9w40ImLJ1H/r5U8EhJQKkFX/JI1XZHPuuex4gAB5+ZuH2spB8HQ3onXOamciDsAQ1WMDxVV7f7dr4EIMD6'
                            'cj8axJ2dArz09Jhzp1wK6+kh/DEELDp1RI0PMNqQK5a/hc3uN/7WVkmOxTMFfrnBRHvPJLPAx2F1f2ozylEoEhNr'
                            'XiMj5VApe3385KVm7mhlLaygtKe8TqF7r3DOCOTqmDACF+gcixi/vWmrEN7NiVFwPuVuUC42FBkcvNzMnUJCckGm'
                            'EkhOkiUWMxd26WtrBLLYlwg6wrKfR38SNk2xhxfcu5EshhxAhs+s761Qdlo9D0IYM2NFFjCXQDusB53AoTysseFw'
                            'n4JLUbYzbGXa81wBwXUn8MbvJeuA8+8S31LV1RLf6uGP22DyHAX8wsa9ZAwaBP1sQgn3AJvXRSAGEOFBvje6yuuy'
                            'eY8dJkynhZ9xB9KzXLCWHsrzbvLfaRpvLoGSZji2Ew640HMfidi6OB1cgE5ALZxdTPAgc4ZvwhaFpdYNuYjSXtzh'
                            'yr5jX81620HffMG0Iyo0PR2cGgoTBYyKj4EGvO7ilgdZgB7I6r1YxhqjQWepCf9Mr6o=')
args = parser.parse_args()
with open('/home/nikita/devenv/wd/organization.key', 'wt') as f:
    f.write('\n'.join([
        args.account_key,
        args.server_url,
    ]))
if args.node:
    args.uuid = f'{args.uuid}_{args.node}'
    args.title = f'{args.title}_{args.node}'
subprocess.run([
    './tvbit-client', 'start', f'--server_url={args.server_url}', f'--account_key={args.account_key}',
    f'--title={args.title}', f'--uuid={args.uuid}', '--electron_path=electron-dist/ui', '--dev'
], check=True, cwd='/home/nikita/devenv/wd')
