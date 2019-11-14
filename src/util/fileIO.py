import os
from .constants import *


def build_dirs():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(b1_dir):
        os.makedirs(b1_dir)
    if not os.path.exists(b2_dir):
        os.makedirs(b2_dir)