import argparse
import requests
from pathlib import Path

classlist = ["Blends", "Ceramic", "Concrete", "Fabric", "Leather", "Marble", "Metal", "Misc", "Plaster", "Plastic", "Stone", "Terracotta", "Wood"]

def download_dataset(base_dir, class_names=None):
    dset_url = "https://huggingface.co/datasets/gvecchio/MatSynth/resolve/main/maps/"

    classes = class_names.split(",") if class_names else classlist
    if classes:
        for split in ["train", "test"]:
            for class_name in classes:
                r = requests.get(f"{dset_url}/{split}/{class_name}.zip")
                with open(base_dir/split/(class_name + ".zip"), "wb") as f:
                    f.write(r.content)
                if class_name in ["Ground", "Wood"]:
                    r = requests.get(dset_url + class_name + ".z01")
                    with open(base_dir/split/(class_name + ".z01"), "wb") as f:
                        f.write(r.content)
    
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Download dataset categories.")
    parser.add_argument("--base_dir", required=True, help="Base directory to save the downloaded files.")
    parser.add_argument("--class_names", help="Specify the class name to download a specific category.")
    args = parser.parse_args()

    # Call the download_dataset function with command-line arguments
    download_dataset(Path(args.base_dir), args.class_names)

# python script.py --base_dir /path/to/save --class_name Leather