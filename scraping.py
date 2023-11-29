#!/usr/bin/env python
# coding: utf-8

from lib.utilities import get_esearch_example, e_search, e_search_id_list, id_key, format_bioC_url, get_paper_bioC
import requests
from bs4 import BeautifulSoup
import json

# get_esearch example
esearch_example = get_esearch_example()

# Get count
print('Total Results:', esearch_example.find('count'))

# Get IDs
ids = [x.text for x in esearch_example.find_all('id')]

# Note that 5000 IDS are returned because that was what we specified 
# for retmax in the example function above.
print('Number of IDs returned: {}'.format(len(ids)))
print('First 5 IDS', ids[:5])

# e-search, e-search-id-list
query = ('((((("survivorship care"[Title/Abstract]) OR '
         '("follow up plans"[Title/Abstract])) OR '
         '("patient care planning"[MeSH Terms])) OR '
         '("survivorship"[MeSH Terms])) OR '
         '("cancer survivors"[MeSH Terms])) AND '
         '(("breast cancer"[Title/Abstract]) OR '
         '(breast neoplasms[MeSH Terms]))')

# Get IDs
id_list = e_search_id_list(query)
# First 5 IDs
short_list = id_list[:10]

# id_key, format_bioC_url, get_paper_bioC
parsed_papers = [json.loads(get_paper_bioC(x).text) for x in id_list]

# Continued, dump the json file
all_papers = [paper['documents'][0] for paper in parsed_papers]

with open('all-papers.json', 'w') as f:
    json.dump(all_papers, f)
