import argparse
import os
import signal
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-r', dest='redirect', action='store_true')
parser.add_argument('--norace', dest='race', action='store_false')
parser.add_argument('--server_url', dest='server_url', default='https://go.tvbit.local:8286')
parser.add_argument('--account_key', dest='account_key', default='FqakvRXAJWgxs3IJhap97kYu0CRklFlomg40sbq1YVErm9o2XkNGPwtR3bGnEVEG0rwE3m3BzsaH+FR2ow7nH8NS2qojZB9w40ImLJ1H/r5U8EhJQKkFX/JI1XZHPuuex4gAB5+ZuH2spB8HQ3onXOamciDsAQ1WMDxVV7f7dr4EIMD6cj8axJ2dArz09Jhzp1wK6+kh/DEELDp1RI0PMNqQK5a/hc3uN/7WVkmOxTMFfrnBRHvPJLPAx2F1f2ozylEoEhNrXiMj5VApe3385KVm7mhlLaygtKe8TqF7r3DOCOTqmDACF+gcixi/vWmrEN7NiVFwPuVuUC42FBkcvNzMnUJCckGmEkhOkiUWMxd26WtrBLLYlwg6wrKfR38SNk2xhxfcu5EshhxAhs+s761Qdlo9D0IYM2NFFjCXQDusB53AoTysseFwn4JLUbYzbGXa81wBwXUn8MbvJeuA8+8S31LV1RLf6uGP22DyHAX8wsa9ZAwaBP1sQgn3AJvXRSAGEOFBvje6yuuyeY8dJkynhZ9xB9KzXLCWHsrzbvLfaRpvLoGSZji2Ew640HMfidi6OB1cgE5ALZxdTPAgc4ZvwhaFpdYNuYjSXtzhyr5jX81620HffMG0Iyo0PR2cGgoTBYyKj4EGvO7ilgdZgB7I6r1YxhqjQWepCf9Mr6o=')
args, unknown = parser.parse_known_args()
os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/go-wd/linux-client', '.']
if args.race:
    go_build.insert(2, '--race')
print(go_build)
subprocess.run(go_build, check=True)
os.chdir('/root/go-wd')
signal.signal(signal.SIGINT, lambda signum, frame: print('Signal handler called with signal', signum))
command = ['./linux-client', 'start', f"--server_url='{args.server_url}'", f"--account_key='{args.account_key}'"] + unknown
print(command)
if args.redirect:
    print('redirecting to /root/go-wd/linux-client.log')
    with open('/root/go-wd/linux-client.log', "w") as outfile:
        subprocess.run(command, stdout=outfile, stderr=subprocess.STDOUT, check=True)
else:
    subprocess.run(command, check=True)
