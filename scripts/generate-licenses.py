import argparse

import requests

parser = argparse.Paparser = argparse.ArgumentParser()
parser.add_argument('--count', type=int, default=1)
parser.add_argument('--account-id', dest='account_id', type=int, required=True)
parser.add_argument('--server-url', dest='server_url', type=str, required=True)
args = parser.parse_args()
for i in range(args.count):
    resp = requests.post(args.server_url, {
        'master_key': 'ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S',
        'controller': 'license',
        'action': 'generate',
        'type': 1,
        'account_id': args.account_id,
        'expires': 0
    }, files={})
    print(resp.text)
print('done')
