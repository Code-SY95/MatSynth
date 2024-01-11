import argparse
from pathlib import Path

import torchvision.transforms.functional as TF
from PIL import Image
from tqdm import tqdm

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Assemble renders.")
    parser.add_argument("--source_dir", required=True, help="Directory where the dataset is stored.")
    args = parser.parse_args()

    source_dir = Path(args.source_dir)

    # Find all materials
    for render_dir in tqdm([x for x in source_dir.glob("**/renders/")]):
        passes_dir = render_dir/"passes"
        num_renders = len(list(passes_dir.glob("*diffuse.png")))
        
        for i in range(num_renders):
            diff_path = passes_dir/f"render_{i:02d}_diffuse.png"
            glossy_path = passes_dir/f"render_{i:02d}_glossy.png"

            full_path = render_dir/f"render_{i:02d}.png"

            diffuse = TF.to_tensor(Image.open(diff_path))
            glossy = TF.to_tensor(Image.open(glossy_path))

            diffuse = TF.adjust_gamma(diffuse, 2.2)
            glossy = TF.adjust_gamma(glossy, 2.2)

            render = diffuse + glossy

            render = TF.adjust_gamma(render, 1/2.2)
            render = TF.to_pil_image(render)
            render.save(full_path)