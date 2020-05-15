import os
import shutil
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--version', dest='version', required=True)
args, _ = parser.parse_known_args()

os.chdir('/root/app/electron-core')
subprocess.run(['npm', 'install'], check=True)
subprocess.run(['npm', 'run', 'dist'], check=True)
shutil.rmtree('/root/wd/linux-client-build', ignore_errors=True)
os.mkdir('/root/wd/linux-client-build')

shutil.move('dist/linux-unpacked', '/root/wd/linux-client-build/electron-dist')
os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/wd/linux-client-build/tvbit-client', '.']
subprocess.run(go_build, check=True)
os.chdir('/root/wd/linux-client-build')
subprocess.run(['tar', '-czvf', f'tvbit_{args.version}_amd64.tar.gz', 'electron-dist', 'tvbit-client'], check=True)

shutil.rmtree('/root/wd/linux-client-build/electron-dist', ignore_errors=True)
shutil.move('/root/app/electron-core/dist/linux-armv7l-unpacked', '/root/wd/linux-client-build/electron-dist')
os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/wd/linux-client-build/tvbit-client', '.']
my_env = os.environ.copy()
my_env['GOOS'] = 'linux'
my_env['GOARCH'] = 'arm'
subprocess.run(go_build, check=True, env=my_env)
os.chdir('/root/wd/linux-client-build')
subprocess.run(['tar', '-czvf', f'tvbit_{args.version}_arm.tar.gz', 'electron-dist', 'tvbit-client'], check=True)

shutil.rmtree('/root/wd/linux-client-build/electron-dist', ignore_errors=True)
shutil.move('/root/app/electron-core/dist/linux-ia32-unpacked', '/root/wd/linux-client-build/electron-dist')
os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/wd/linux-client-build/tvbit-client', '.']
my_env = os.environ.copy()
my_env['GOOS'] = 'linux'
my_env['GOARCH'] = '386'
subprocess.run(go_build, check=True, env=my_env)
os.chdir('/root/wd/linux-client-build')
subprocess.run(['tar', '-czvf', f'tvbit_{args.version}_386.tar.gz', 'electron-dist', 'tvbit-client'], check=True)

shutil.rmtree('/root/wd/linux-client-build/electron-dist', ignore_errors=True)
shutil.move('/root/app/electron-core/dist/linux-arm64-unpacked', '/root/wd/linux-client-build/electron-dist')
os.chdir('/root/app/linux-client')
go_build = ['go', 'build', '-o', '/root/wd/linux-client-build/tvbit-client', '.']
my_env = os.environ.copy()
my_env['GOOS'] = 'linux'
my_env['GOARCH'] = 'arm64'
subprocess.run(go_build, check=True, env=my_env)
os.chdir('/root/wd/linux-client-build')
subprocess.run(['tar', '-czvf', f'tvbit_{args.version}_arm64.tar.gz', 'electron-dist', 'tvbit-client'], check=True)
