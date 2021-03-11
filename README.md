# ArchiveDownload
Console tool to search and grab Grateful Dead tracks from archive.org

* python3 -m venv pyenv
* source ./pyenv/bin/activate
* pip install -r requirements.txt

To grab the archive links from etree:

    ./get_etree_links.py

To download all the archive pages:

    ./get_archive_pages.py

This last step will take some time and hard drive space (about 6 hours and 3GB on my machine).
