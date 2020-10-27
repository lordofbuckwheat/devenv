import argparse

import shared

parser = argparse.ArgumentParser()
parser.add_argument('--server-url', dest='server_url', type=str)
parser.add_argument('--license-id', type=int, dest='license_id')
args = parser.parse_args()
shared.build_and_upload_servers(args.server_url, False, args.license_id)
