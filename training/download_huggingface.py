import os
import sys
import logging
from huggingface_hub import snapshot_download

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('data_raw/huggingface', exist_ok=True)
os.makedirs('logs', exist_ok=True)

log_file = os.path.join('logs', 'huggingface_download.log')
logging.basicConfig(
    filename=log_file,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

DATASETS = [
    {
        "repo_id": "Project-AgML/rice_leaf_disease_classification",
        "local_name": "rice_leaf_disease_classification"
    },
    {
        "repo_id": "Project-AgML/rice_leaf_disease_classification_india",
        "local_name": "rice_leaf_disease_classification_india"
    },
    {
        "repo_id": "Project-AgML/MH_SoyaHealthVision_disease_classification_leaf",
        "local_name": "MH_SoyaHealthVision_disease_classification_leaf"
    },
    {
        "repo_id": "Project-AgML/SoyNet_leaf_health_classification",
        "local_name": "SoyNet_leaf_health_classification"
    }
]

def check_or_download(item):
    repo_id = item["repo_id"]
    local_dir = os.path.join("data_raw", "huggingface", item["local_name"])
    os.makedirs(local_dir, exist_ok=True)

    data_dir = os.path.join(local_dir, "data")
    if os.path.exists(data_dir):
        parquet_files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
        if len(parquet_files) > 0:
            logger.info(f"[EXISTS] {repo_id} already has {len(parquet_files)} parquet files in {data_dir}. Skipping redownload.")
            return True

    logger.info(f"Downloading {repo_id} to {local_dir}...")
    try:
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            max_workers=4
        )
        logger.info(f"[SUCCESS] Downloaded {repo_id}")
        return True
    except Exception as e:
        logger.error(f"[ERROR] Failed to download {repo_id}: {e}")
        return False

def main():
    logger.info("=" * 60)
    logger.info("HUGGING FACE DATASET DOWNLOAD SUMMARY CHECK")
    logger.info("=" * 60)
    summary = {}
    for item in DATASETS:
        res = check_or_download(item)
        summary[item["repo_id"]] = "COMPLETE / READY" if res else "FAILED / INCOMPLETE"

    for k, v in summary.items():
        logger.info(f"Dataset {k}: {v}")

if __name__ == '__main__':
    main()
