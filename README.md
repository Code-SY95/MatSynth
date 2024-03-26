---
language:
- en
size_categories:
- 1K<n<10K
task_categories:
- image-to-image
- unconditional-image-generation
- image-classification
- text-to-image
paperswithcode_id: matsynth
pretty_name: MatSynth
homepage: https://gvecchio.com/matsynth/
tags:
- materials
- pbr
- 4d
- graphics
- rendering
- svbrdf
viewer: false
dataset_info:
  features:
  - name: name
    dtype: string
  - name: category
    dtype:
      class_label:
        names:
          '0': ceramic
          '1': concrete
          '2': fabric
          '3': ground
          '4': leather
          '5': marble
          '6': metal
          '7': misc
          '8': plaster
          '9': plastic
          '10': stone
          '11': terracotta
          '12': wood
  - name: metadata
    struct:
    - name: authors
      sequence: string
    - name: description
      dtype: string
    - name: height_factor
      dtype: float32
    - name: height_mean
      dtype: float32
    - name: license
      dtype: string
    - name: link
      dtype: string
    - name: maps
      sequence: string
    - name: method
      dtype: string
    - name: name
      dtype: string
    - name: physical_size
      dtype: float32
    - name: source
      dtype: string
    - name: stationary
      dtype: bool
    - name: tags
      sequence: string
    - name: version_date
      dtype: string
  - name: basecolor
    dtype: image
  - name: diffuse
    dtype: image
  - name: displacement
    dtype: image
  - name: height
    dtype: image
  - name: metallic
    dtype: image
  - name: normal
    dtype: image
  - name: opacity
    dtype: image
  - name: roughness
    dtype: image
  - name: specular
    dtype: image
  - name: blend_mask
    dtype: image
  splits:
  - name: test
    num_bytes: 6688789896.0
    num_examples: 84
  download_size: 6608046610
  dataset_size: 6688789896.0
configs:
- config_name: default
  data_files:
  - split: test
    path: data/test-*
---

# MatSynth

MatSynth is a Physically Based Rendering (PBR) materials dataset designed for modern AI applications.
This dataset consists of over 4,000 ultra-high resolution, offering unparalleled scale, diversity, and detail. 

Meticulously collected and curated, MatSynth is poised to drive innovation in material acquisition and generation applications, providing a rich resource for researchers, developers, and enthusiasts in computer graphics and related fields.

For further information, refer to our paper: ["MatSynth: A Modern PBR Materials Dataset"](https://arxiv.org/abs/2401.06056) available on arXiv.

<center>
  <img src="https://gvecchio.com/matsynth/static/images/teaser.png" style="border-radius:15px; width:80%">
</center>

## 🔍 Dataset Details

### Dataset Description

MatSynth is a new large-scale dataset comprising over 4,000 ultra-high resolution Physically Based Rendering (PBR) materials, 
all released under permissive licensing.

All materials in the dataset are represented by a common set of maps (*Basecolor*, *Diffuse*, *Normal*, *Height*, *Roughness*, *Metallic*, *Specular* and, when useful, *Opacity*), 
modelling both the reflectance and mesostructure of the material.

Each material in the dataset comes with rich metadata, including information on its origin, licensing details, category, tags, creation method, 
and, when available, descriptions and physical size. 
This comprehensive metadata facilitates precise material selection and usage, catering to the specific needs of users.

## 📂 Dataset Structure
 
The MatSynth dataset is divided into two splits: the test split, containing 89 materials, and the train split, consisting of 3,980 materials. 
To enhance accessibility and ease of navigation, each split is further organized into separate folders for each distinct category present in the dataset (Blends, Ceramic, Concrete, Fabric, Ground, Leather, Marble, Metal, Misc, Plastic, Plaster, Stone, Terracotta, Wood). 

## 🔨 Dataset Creation

The MatSynth dataset is designed to support modern, learning-based techniques for a variety of material-related tasks including, 
but not limited to, material acquisition, material generation and synthetic data generation e.g. for retrieval or segmentation. 

### 🗃️ Source Data

The MatSynth dataset is the result of an extensively collection of data from multiple online sources operating under the CC0 and CC-BY licensing framework. 
This collection strategy allows to capture a broad spectrum of materials, 
from commonly used ones to more niche or specialized variants while guaranteeing that the data can be used for a variety of usecases. 

Materials under CC0 license were collected from [AmbientCG](https://ambientcg.com/), [CGBookCase](https://www.cgbookcase.com/), [PolyHeaven](https://polyhaven.com/), 
[ShateTexture](https://www.sharetextures.com/), and [TextureCan](https://www.texturecan.com/).
The dataset also includes limited set of materials from the artist [Julio Sillet](https://juliosillet.gumroad.com/), distributed under CC-BY license.

We collected over 6000 materials which we meticulously filter to keep only tileable, 4K materials. 
This high resolution allows us to extract many different crops from each sample at different scale for augmentation. 
Additionally, we discard blurry or low-quality materials (by visual inspection). 
The resulting dataset consists of 3736 unique materials which we augment by blending semantically compatible materials (e.g.: snow over ground). 
In total, our dataset contains 4069 unique 4K materials.

### ✒️ Annotations

The dataset is composed of material maps (Basecolor, Diffuse, Normal, Height, Roughness, Metallic, Specular and, when useful, opacity) 
and associated renderings under varying environmental illuminations, and multi-scale crops.
We adopt the OpenGL standard for the Normal map (Y-axis pointing upward). 
The Height map is given in a 16-bit single channel format for higher precision.

In addition to these maps, the dataset includes other annotations providing context to each material: 
the capture method (photogrammetry, procedural generation, or approximation); 
list of descriptive tags; source name (website); source link; 
licensing and a timestamps for eventual future versioning. 
For a subset of materials, when the information is available, we also provide the author name (387), text description (572) and a physical size, 
presented as the length of the edge in centimeters (358). 

## 📜 Citation

```
@inproceedings{vecchio2023matsynth,
  title={MatSynth: A Modern PBR Materials Dataset},
  author={Vecchio, Giuseppe and Deschaintre, Valentin},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  year={2024}
}
```