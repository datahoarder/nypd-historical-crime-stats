from os import makedirs
from os.path import join
from urllib.parse import urljoin
import requests
FETCHED_DATA_DIR = './data/fetched'
BASE_URL = 'http://www.nyc.gov/html/nypd/downloads/excel/analysis_and_planning/'
BASE_FILENAMES = ['seven_major_felony_offenses_by_precinct_2000_2014.xls',
    'non_seven_major_felony_offenses_by_precinct_2000_2014.xls',
    'misdemeanor_offenses_by_precinct_2000_2014.xls',
    'violation_offenses_by_precinct_2000_2014.xls']


makedirs(FETCHED_DATA_DIR, exist_ok = True)

for fname in BASE_FILENAMES:
    source_url = urljoin(BASE_URL, fname)
    dest_path = join(FETCHED_DATA_DIR, fname)

    print("Downloading", source_url, "into", dest_path)
    resp = requests.get(source_url)
    with open(dest_path, 'wb') as o:
        o.write(resp.content)
