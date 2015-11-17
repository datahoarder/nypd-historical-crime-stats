from os import makedirs
from os.path import join
WRANGLED_DATA_DIR = './data/wrangled'
COMPILED_DATA_DIR = './data/compiled'
COMPILED_DATA_PATH = join(COMPILED_DATA_DIR, 'nypd-precinct-historical-crime-data.csv')
BASE_FILENAMES = ['seven_major_felony_offenses_by_precinct_2000_2014.xls',
    'non_seven_major_felony_offenses_by_precinct_2000_2014.xls',
    'misdemeanor_offenses_by_precinct_2000_2014.xls',
    'violation_offenses_by_precinct_2000_2014.xls']
OUTPUT_FIELDNAMES = ['precinct', 'year', 'category', 'incident_count']

makedirs(COMPILED_DATA_DIR, exist_ok = True)

with open(COMPILED_DATA_PATH, 'w') as compiled_file:
    # write the headers as just a line of text
    compiled_file.write(','.join(OUTPUT_FIELDNAMES))
    compiled_file.write("\n")
    for fname in BASE_FILENAMES:
        # remember that we appended '.csv' to every original filename
        source_path = join(WRANGLED_DATA_DIR, fname + '.csv')
        print("Adding", source_path, "to", COMPILED_DATA_PATH)
        with open(source_path) as csv_file:
            csv_file.readline() # skip first line
            compiled_file.write(csv_file.read()) # read everything else as a big ol' chunk


