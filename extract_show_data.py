#!/usr/bin/env python3

import os
from tqdm import tqdm

from get_archive_pages import ARCHIVE_FOLDER
from gd_data import Show, Track

# load the archive files and extract the data

def getAllFiles(directory):
	return [x for x in os.listdir() if os.path.isfile(x)]


if __name__ == '__main__':
	print getAllFiles(ARCHIVE_FOLDER)
