"""Creates a toy dataset from the not yet fully loaded MIMIC-CXR dataset."""

import os
import sys
import re
from pathlib import Path

#from tqdm import tqdm
from typing import Generator, Tuple, List, Dict, Any, Optional

import pandas as pd
from magma.datasets.convert_datasets import convert_dataset


DATAROOT = Path("/srv/scratch1/nbodenmann/mimic-cxr/physionet.org/files/mimic-cxr-jpg/2.0.0/")

def report_image_generator(dataroot: Path, duplicate_reports=False):
    """Iterate over all reports and images in the MIMIC-CXR dataset.

    By standard, only one AP is used per study. If duplicate_reports is True, all
    images that are AP or PA are used, while the path to the report is duplicated for
    each image.
    
    Args:
        dataroot (str): Path to the MIMIC-CXR dataset.
        duplicate_reports (bool): If True, duplicate reports for studies with multiple
            images. If False (default), only use the first report for studies with
            multiple images.
            
    Yields:
        report_path (str): Path to the report.
        image_path (str): Path to the image.
    """

    df = pd.read_csv(dataroot / "mimic-cxr-2.0.0-metadata.csv")
    # Iterate over all rows of a patient
    for patient_id, patient_images in df.groupby('subject_id'):
        # Iterate over all studies of a patient
        for study_id, study_images in patient_images.groupby('study_id'):

            dicom_ids = []

            AP_images = study_images[study_images['ViewPosition'] == 'AP']
            dicom_ids.extend(AP_images['dicom_id'].tolist())

            PA_images = study_images[study_images['ViewPosition'] == 'PA']
            dicom_ids.extend(PA_images['dicom_id'].tolist())


            dicom_iterable = dicom_ids if duplicate_reports else dicom_ids[:1]
            
            for dicom_id in dicom_iterable:
                image_path =  dataroot / f"files/p{str(patient_id)[:2]}" / f"p{patient_id}" / f"s{study_id}" / f"{dicom_id}.jpg"
                report_path = dataroot / f"files/p{str(patient_id)[:2]}" / f"p{patient_id}" / f"s{study_id}.txt"

                yield report_path, image_path

section_re = re.compile(r"\s*([A-Z ]+):(.*)")
white_re = re.compile(r"\s+")

def extract_caption(report_path: Path) -> Optional[str]:
    """Extract the caption from a report.

    The FINDINGS section is used as the caption. If no FINDINGS section is found, the
    IMPRESSION section is used. If neither FINDINGS nor IMPRESSION is found, None is
    returned.

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
        return report_dict["FINDINGS"]
    
    except KeyError:
        try:
            return report_dict["IMPRESSION"]
        
        except KeyError:
            return None

class dataset_iterator():

    def __init__(self, toy: bool, dataroot: Path, length=None) -> None:
        """Iterate over the dataset and yield the image and caption for each study.

        Yields:
            img_path (Path): Path to the image.
            caption (str): Caption of the report.
        """
        self.toy = toy
        self.data_root = Path(dataroot)
        self.length = length

    def __iter__(self) -> Generator[Tuple[Path, Dict[str, Any]], None, None]:

        n = 0

        for report_path, img_path in report_image_generator(self.data_root, duplicate_reports=False):
            
            if self.toy and n > 1000:
                break

            caption = extract_caption(report_path)

            if caption:
                n += 1
                yield img_path, {"caption": caption, "metadata": {}}
                print(f"Yielded {n} images.", end="\r")
            else:
                continue

    def __len__(self) -> int:
        """Return the length of the dataset.

        Only calculate the length once and store it in self.length.
        
        Returns:
            length (int): Length of the dataset.
        """
        if self.length:
            return self.length
        else:
            length = sum(1 for _ in self)
            self.length = length
            return length

def create_toy_dataset():

    convert_dataset(
        data_dir=Path("/home/user/vbernhard/medi-magma/data"),
        mode="cp",
        ds_iterator=dataset_iterator(
            toy=True,
            dataroot=DATAROOT,
        ),
    )
    
    # for studypath in single_jpg_studies:
    #     img_path, report_path = get_img_and_report_path(studypath)
    #     caption = extract_caption(report_path)


def create_real_dataset():
    
    convert_dataset(
        data_dir=Path("/srv/scratch1/nbodenmann/prepared_mimic-cxr"),
        mode="cp",
        ds_iterator=dataset_iterator(
            toy=False,
            dataroot=DATAROOT,
        ),
    )

def main():
    # create_toy_dataset()
    create_real_dataset()

if __name__ == "__main__":
    main()