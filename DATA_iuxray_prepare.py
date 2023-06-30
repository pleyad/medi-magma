"""Creates a MAGMA dataset for the IU X-ray dataset."""

import os
import sys
import csv
from pathlib import Path

import pandas as pd
from tqdm import tqdm
import numpy as np
from typing import Generator, Tuple, List, Dict, Any, Optional
from magma.datasets.convert_datasets import convert_dataset

DATAROOT = Path("<path>/iu-xray/")

def caption_image_generator(projections_path: Path, reports_path: Path) -> Generator[Tuple[str, str], None, None]:
    """Iterate over all reports and images in the IU X-ray dataset.

    Args:
        projections_path (Path): Path to the projections.csv file.
        reports_path (Path): Path to the reports.csv file.
        
    Yields:
        report_path (str): Path to the report.
        image_path (str): Path to the image.
    """

    projections_df = pd.read_csv(projections_path)
    reports_df = pd.read_csv(reports_path)

    # Per study, only use a single frontal image. If there are multiple frontal images,
    # use the first one. If there are no frontal images, skip the study.
    only_frontal_df = projections_df[projections_df["projection"] == "Frontal"]
    only_frontal_df = only_frontal_df.groupby("uid").first().reset_index()

    df = pd.merge(only_frontal_df, reports_df, on="uid", how="inner")

    for _, row in df.iterrows():
        image_path = DATAROOT / "images" / "images_normalized" / row["filename"]
        

        caption = row["findings"]
        if type(caption) != str:

            caption = row["impression"]

            if type(caption) != str:
                continue

        yield caption, image_path


class dataset_iterator():

    def __init__(self, dataroot: Path, length=None):
        """Iterate over the dataset and yield captions and image paths.

        Yields:
            caption (str): Caption of the image.
            image_path (str): Path to the image.
        """
        self.dataroot = dataroot
        self.length = length

    def __iter__(self):
        
        proj_path = self.dataroot / "indiana_projections.csv"
        reports_path = self.dataroot / "indiana_reports.csv"
        
        for caption, img_path in caption_image_generator(proj_path, reports_path):
            yield img_path, {"caption": caption, "metadata": {}}

    def __len__(self):
        if self.length:
            return self.length
        else:
            length = sum(1 for _ in self)
            self.length = length
            return length

def test():
    # Test 3 iterations
    iterator = dataset_iterator(DATAROOT)
    for i, (caption, image_path) in enumerate(iterator):
        print(caption)
        print(image_path)
        if i == 2:
            break

def create_dataset():
    # Create the dataset
    convert_dataset(
        data_dir=Path("<path>/prepared_iu-xray/"),
        mode="cp",
        ds_iterator=dataset_iterator(DATAROOT)
    )

def main():
    create_dataset()

if __name__ == "__main__":
    main()