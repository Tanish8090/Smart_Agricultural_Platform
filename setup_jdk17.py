import os
import sys
import zipfile
import urllib.request
import time

jdk_dir = os.path.expanduser("~/.jdks")
os.makedirs(jdk_dir, exist_ok=True)
dest_dir = os.path.join(jdk_dir, "jdk-17")
zip_path = os.path.join(jdk_dir, "microsoft-jdk-17.zip")

url = "https://aka.ms/download-jdk/microsoft-jdk-17.0.12-windows-x64.zip"

if not os.path.exists(dest_dir) or not os.path.exists(os.path.join(dest_dir, "bin", "java.exe")):
    print(f"Downloading OpenJDK 17 from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    t0 = time.time()
    with urllib.request.urlopen(req) as resp, open(zip_path, 'wb') as f:
        total = int(resp.headers.get('Content-Length', 0))
        downloaded = 0
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0 and (downloaded // (1024*1024)) % 25 == 0:
                print(f"  {downloaded / (1024*1024):.1f} / {total / (1024*1024):.1f} MB ({(downloaded/total)*100:.1f}%)")
    print(f"Downloaded in {time.time()-t0:.1f}s. Extracting to {jdk_dir}...")
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Check root folder name in zip
        names = zf.namelist()
        root_folder = names[0].split('/')[0]
        zf.extractall(jdk_dir)
        extracted_root = os.path.join(jdk_dir, root_folder)
        if os.path.exists(extracted_root) and extracted_root != dest_dir:
            if os.path.exists(dest_dir):
                import shutil
                shutil.rmtree(dest_dir)
            os.rename(extracted_root, dest_dir)
            
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print(f"[OK] OpenJDK 17 ready at: {dest_dir}")
else:
    print(f"[OK] OpenJDK 17 already exists at: {dest_dir}")
