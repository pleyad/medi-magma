from DATA_iuxray_prepare import dataset_iterator as iuxray_dataset_iterator
from DATA_mimic_prepare import dataset_iterator as mimic_dataset_iterator

from magma.datasets.convert_datasets import convert_dataset
import os
# Set visible CUDAs to empty
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from pathlib import Path

MIMIC_ROOT = Path("<path>/physionet.org/files/mimic-cxr-jpg/2.0.0/")
IUXRAY_ROOT = Path("<path>/iu-xray/")

class combined_iterator():

    def __init__(self, mimic_path: Path, iuxray_path: Path, length=None):
        """Iterate over the dataset and yield captions and image paths.

        Yields:
            caption (str): Caption of the image.
            image_path (str): Path to the image.
        """
        self.mimic_path = mimic_path
        self.iuxray_path = iuxray_path
        self.length = length

    def __iter__(self):
            
        # Approx 200k images in mimic
        # Approx 3.6k images in iuxray

        mimic_iterator = mimic_dataset_iterator(self.mimic_path, toy=False).__iter__()
        iuxray_iterator = iuxray_dataset_iterator(self.iuxray_path).__iter__()

        i = 0
        while True:
            try:
                if i % 55 == 0:
                    yield next(iuxray_iterator)
                else:
                    yield next(mimic_iterator)
                i += 1
            except StopIteration:
                break
        
        # Empty the iterators, one of them is already empty
        while True:
            try:
                yield next(mimic_iterator)
            except StopIteration:
                break
        while True:
            try:
                yield next(iuxray_iterator)
            except StopIteration:
                break
        
    def __len__(self):
        if self.length:
            return self.length
        else:
            length = sum(1 for _ in self)
            self.length = length
            return length
        

def create_dataset():
    
        convert_dataset(
            data_dir=Path("<path>"),
            mode="cp",
            ds_iterator=combined_iterator(
                mimic_path=MIMIC_ROOT,
                iuxray_path=IUXRAY_ROOT
            )
        )

if __name__ == "__main__":
    create_dataset()