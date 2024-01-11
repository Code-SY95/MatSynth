import argparse
import requests
from pathlib import Path

classlist = ["Blends", "Ceramic", "Concrete", "Fabric", "Leather", "Marble", "Metal", "Misc", "Plaster", "Plastic", "Stone", "Terracotta", "Wood"]

def download_stream(url, dest_file):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def download_dataset(base_dir, class_names=None):
    dset_url = "https://huggingface.co/datasets/gvecchio/MatSynth/resolve/main/maps"

    classes = class_names.split(",") if class_names else classlist
    if classes:
        for split in ["train", "test"]:
            dest_dir = base_dir/split
            dest_dir.mkdir(parents=True, exist_ok=True)

            for class_name in classes:
                req = f"{dset_url}/{split}/{class_name}.zip"
                download_stream(req, dest_dir/(class_name + ".zip"))

                if class_name in ["Ground", "Wood"] and split == "train":
                    req = f"{dset_url}/{split}/{class_name}.z01"
                    download_stream(req, dest_dir/(class_name + ".z01"))
    
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Download dataset categories.")
    parser.add_argument("--base_dir", required=True, help="Base directory to save the downloaded files.")
    parser.add_argument("--class_names", help="Specify the class name to download a specific category.")
    args = parser.parse_args()

    # Call the download_dataset function with command-line arguments
    download_dataset(Path(args.base_dir), args.class_names)

# python script.py --base_dir /path/to/save --class_name Leather