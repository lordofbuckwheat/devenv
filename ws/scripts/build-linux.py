import os
import shutil
import subprocess

os.chdir('/root/app/electron-core')
if not os.path.exists('node_modules'):
    subprocess.run(['npm', 'install'], check=True)
subprocess.run(['npm', 'run', 'dist'], check=True)
shutil.rmtree('/root/go-wd/electron-dist')
shutil.move('dist', '/root/go-wd/electron-dist')
