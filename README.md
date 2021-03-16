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

 Now we can extract the data from the archive pages and write out a large json file of the data:

     ./extract_show_data.py


Cleaning Data
-------------

The next step is to clean the data.

We have a large number of recordings for every show. We comapre all recording to check the song orders.

If a show has only 1 recording, we take that and assume it is correct.

If a show has > 2 recordings, we see if any are the same, and select those with the most "sameness".

If a show only has 2 recordings and they disagree, we must check manually.

This part is currently incomplete.

    ./split_json.py