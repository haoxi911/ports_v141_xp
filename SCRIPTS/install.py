#
# 2019-09-19. Created by Hao Xi (haoxi911@gmail.com)
# 
# This script accepts a folder path as the only parameter, it will search
# through all the ports in this repo, and merge all the contents from each
# port into the specified folder.
# 
# In other words, it will combine all the common folders like 'include', 'lib',
# and 'bin', and provides a single path for Visual Studio to load.
#
# Usage:
#       pip3 install tqdm 
#       python3 install.py <path-to-dst-folder>
#

import os
import re
import sys
import shutil
import urllib.request 
import zipfile
from tqdm import tqdm

def downloadport(port_dir):
  '''Download a port package into the local folder.'''
  url = None # download url
  readme = os.path.join(port_dir, 'README.md')
  if os.path.exists(readme):
   with open(readme, 'r') as file:
      text = file.read()
      matches = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text)
      for item in matches:
        if item.endswith('.zip'):
          url = item
          break
  if url:
    filename = url.split('/')[-1]
    filepath = os.path.join(port_dir, filename)
    if not os.path.exists(filepath):
      print('Downloading %s' % filepath)
      class downloadprogress(tqdm): # progress report
        def update_to(self, b=1, bsize=1, tsize=None):
          if tsize is not None:
              self.total = tsize
          self.update(b * bsize - self.n)
      with downloadprogress(unit='B', unit_scale=True, miniters=1, desc=filename) as t:
        urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)
    if not os.path.exists(filepath):
      print('Warning: port download failed [%s]' % url)
    else:
      print('Extracting %s' % filepath)
      with zipfile.ZipFile(filepath, 'r') as zip_ref:
          zip_ref.extractall(port_dir)
  else:
    print('Warning: port download url not found [%s]' % port_dir)

def copytree(root_src_dir, root_dst_dir):
  '''Copy files from source folder and merge into destination folder.'''
  for src_dir, _unused1, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
      os.makedirs(dst_dir)
    for item in files:
      _unused2, ext = os.path.splitext(item)
      if ext in ['.txt', '.md', '.zip']: # skip by file ext
        continue
      src_file = os.path.join(src_dir, item)
      dst_file = os.path.join(dst_dir, item)
      if os.path.exists(dst_file):
        print('Warning: file [%s] already exists.' % dst_file)
      else:
        shutil.copy(src_file, dst_dir)

repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst_dir = None
if len(sys.argv) > 1:
  dst_dir = os.path.realpath(sys.argv[1])
else:
  dst_dir = os.path.join(repo_dir, 'PORTS')
if not os.path.exists(dst_dir):
  os.makedirs(dst_dir)

for port in os.scandir(repo_dir):
  if port.name.islower() and port.name[0] != '.':
    if port.name in ['aws-sdk-cpp', 'vmime']:
      downloadport(port.path)
    copytree(port.path, dst_dir)