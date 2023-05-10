"""Creates a toy dataset from the not yet fully loaded MIMIC-CXR dataset."""

import os
import sys
import re
from pathlib import Path

#from tqdm import tqdm
from typing import Generator, Tuple, List, Dict, Any, Optional

# from magma.datasets.convert_datasets import convert_dataset

DATAROOT = Path("/srv/scratch1/nbodenmann/mimic-cxr/physionet.org/files/mimic-cxr-jpg/2.0.0/")

def find_studies(dataroot, search_until=None):
    """Find studies with multiple jpgs, single jpgs, and no jpgs.

    Args:
        dataroot (str): Path to the MIMIC-CXR dataset.
        search_until (int): Number of single jpg studies to search for. If None, search
            until all studies are retrieved.

    Returns:
        multi_jpg_studies (list): List of studies with multiple jpgs.
        single_jpg_studies (list): List of studies with single jpgs.
        no_jpg_studies (list): List of studies with no jpgs (incomplete download)
    """
    multi_jpg_studies = []
    single_jpg_studies = []
    no_jpg_studies = []

    # pbar = tqdm(total=search_until)

    try:
        for root, dirs, files in os.walk(dataroot):
            if search_until is not None and len(single_jpg_studies) >= search_until:
                break
            
            if not Path(root).name.startswith("s"):
                continue
            
            jpgs = [f for f in files if f.endswith(".jpg")]
            if len(jpgs) > 1:
                # print(root)
                multi_jpg_studies.append(root)
            elif len(jpgs) == 1:
                #pbar.update(1)
                single_jpg_studies.append(root)
            else:
                no_jpg_studies.append(root)

    except KeyboardInterrupt:
        pass

    print('Studies')
    print('Multi jpg studies:  ', len(multi_jpg_studies))
    print('Single jpg studies: ', len(single_jpg_studies))
    print('No jpg studies:     ', len(no_jpg_studies))

    return multi_jpg_studies, single_jpg_studies, no_jpg_studies


# Only look for single JPG studies for the dummy dataset
_, _, no_jpg_studies = find_studies(DATAROOT, search_until=5000)

def get_img_and_report_path(studypath):
    """Get the path to the image and report for a given study.

    Args:
        studypath (str): Path to the study.

    Returns:
        img_path (str): Path to the image.
        report_path (str): Path to the report.
    """
    studypath = Path(studypath)

    studyname = studypath.stem

    img_path =  [f for f in studypath.glob("*.jpg")][0]
    report_path = studypath.parent / f"{studyname}.txt"

    return img_path, report_path

section_re = re.compile(r"\s*([A-Z ]+):(.*)")
white_re = re.compile(r"\s+")

def extract_caption(report_path):
    """Extract the caption from a report.

    Args:
        report_path (str): Path to the report.

    Returns:
        caption (str): Caption of the report.
    """
    with open(report_path, "r") as f:
        content = f.read()

    # If a paragraph starts with uppercase words followed by a colon, use the uppercased words as a key
    # and the following paragraph as the value.
    report_dict = {}

    current_key = None

    for line in content.split("\n"):
        
        match = section_re.match(line)

        if match:
            current_key, text = match.groups()
            report_dict[current_key] = text

        elif current_key is not None:
            report_dict[current_key] += " " + line

    # Remove whitespaces
    report_dict = {k: white_re.sub(" ", v).strip() for k, v in report_dict.items()}

    try:
        return report_dict["IMPRESSION"]
    
    except KeyError:
        return None

class dataset_iterator():

    def __init__(self) -> None:
        """Iterate over the dataset and yield the image and caption for each study.

        Yields:
            img_path (Path): Path to the image.
            caption (str): Caption of the report.
        """
        pass

    def __iter__(self) -> Generator[Tuple[Path, Dict[str, Any]], None, None]:

        n = 0
        for studypath in single_jpg_studies:
            if n >= 1000:
                break
            img_path, report_path = get_img_and_report_path(studypath)
            caption = extract_caption(report_path)

            if caption:
                n += 1
                yield img_path, {"caption": caption, "metadata": {}}
            else:
                continue

    def __len__(self) -> int:
        return sum(1 for _ in self)

def test():
    print(no_jpg_studies[:10])

def main():

    convert_dataset(
        data_dir=Path("/home/user/vbernhard/medi-magma/data"),
        mode="cp",
        ds_iterator=dataset_iterator(),
    )
    
    # for studypath in single_jpg_studies:
    #     img_path, report_path = get_img_and_report_path(studypath)
    #     caption = extract_caption(report_path)

test()
