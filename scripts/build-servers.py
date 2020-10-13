import argparse
import shared

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
parser.add_argument('--upload', type=str)
args = parser.parse_args()
if args.upload:
    shared.build_and_upload_servers(args.upload)
else:
    shared.build_servers(args.dev)
