import os
import sys
import urllib.request
import time

url = "https://services.gradle.org/distributions/gradle-8.11.1-bin.zip"
target_dir = os.path.expanduser("~/.gradle/wrapper/dists/gradle-8.11.1-bin")
os.makedirs(target_dir, exist_ok=True)

# Also find or create hash dir
subdirs = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
if subdirs:
    dest_dir = os.path.join(target_dir, subdirs[0])
else:
    dest_dir = target_dir

dest_file = os.path.join(dest_dir, "gradle-8.11.1-bin.zip")
print(f"Downloading {url} to {dest_file}...")

def reporthook(count, block_size, total_size):
    if count % 1000 == 0:
        percent = int(count * block_size * 100 / total_size)
        mb = (count * block_size) / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        print(f"Downloaded {mb:.1f} MB of {total_mb:.1f} MB ({percent}%)")

try:
    urllib.request.urlretrieve(url, dest_file, reporthook)
    print(f"Successfully downloaded to {dest_file} ({os.path.getsize(dest_file)/(1024*1024):.1f} MB)")
except Exception as e:
    print(f"Download failed: {e}")
