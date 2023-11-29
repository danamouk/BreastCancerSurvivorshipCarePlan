import requests
from bs4 import BeautifulSoup
from ediblepickle import checkpoint
import os

def get_esearch_example():
    """
    Perform an example PubMed search using the E-utilities API and return the BeautifulSoup object.

    Returns:
    - BeautifulSoup: The BeautifulSoup object containing the search results.
    """
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {'db': 'pubmed',
              'term': 'pmc open access[filter] ' + 'breast cancer',
              'retmax': '5000'}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# This is a BeautifulSoup object - see above
esearch_example = get_esearch_example()

def e_search(query=None, max_results=1000):
    """
    Perform a PubMed search using the E-utilities API and return the Response object.

    Parameters:
    - query (str): The search query.
    - max_results (int): The maximum number of results to retrieve.

    Returns:
    - requests.Response: The Response object containing the search results.
    """
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {'db': 'pubmed',
              'term': 'pmc open access[filter] ' + query,
              'retmax': max_results}
    response = requests.get(url, params=params)
    return response

def e_search_id_list(query=None, max_results=1000):
    """
    Perform a PubMed search using the E-utilities API and return the list of retrieved IDs (total count for that query).

    Parameters:
    - query (str): The search query.
    - max_results (int): The maximum number of results to retrieve.

    Returns:
    - list: The list of retrieved IDs.
    """
    response = e_search(query, max_results)
    soup = BeautifulSoup(response.content, 'html.parser')
    count = soup.find('count').text
    ids = [tag.text for tag in soup.find_all('id')]

    print('Total results: ', count)
    print('Results returned: ', len(ids))

    return ids

## This stuff is for checkpointing the results
if not os.path.exists('papers-json'):
    os.mkdir('papers-json')

def id_key(args, kwargs):
    return args[0] + '.pkl'

def format_bioC_url(paper_id, format_='xml', encoding='unicode'):
    """
    Generate a BioC API URL for a PubMed Central article based on its ID (This formats the URL for the BioC API.)

    Parameters:
    - paper_id (str): The PubMed Central article ID.
    - format_ (str): The desired format for the response (default is 'xml').
    - encoding (str): The desired encoding for the response (default is 'unicode').

    Returns:
    - str: The formatted BioC API URL.
    """
    url = f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_{format_}/{paper_id}/{encoding}'
    return url

@checkpoint(key=id_key, work_dir='papers-json')
def get_paper_bioC(paper_id, format_='json'):
    """
    Fetch a machine-readable paper from PubMed Central given its ID and return the Response object.

    Parameters:
    - paper_id (str): The PubMed Central article ID.
    - format_ (str): The desired format for the response (default is 'json').

    Returns:
    - requests.Response: The Response object containing the paper.
    """
    url = format_bioC_url(paper_id, format_)
    response = requests.get(url)
    return response
