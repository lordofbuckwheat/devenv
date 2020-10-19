import argparse

import shared

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
parser.add_argument('--upload', type=str)
parser.add_argument('--license-id', type=int, dest='license_id')
args = parser.parse_args()
if args.upload:
    if args.license_id:
        shared.build_and_upload_servers(args.upload, args.license_id)
    else:
        shared.build_and_upload_servers(args.upload)
else:
    shared.build_servers(args.dev)
