import argparse

import shared

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
args, _ = parser.parse_known_args()
shared.build_servers(args.dev)
