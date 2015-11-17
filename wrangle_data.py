from csv import DictWriter
from os import makedirs
from os.path import join
from xlrd import open_workbook
import re
FETCHED_DATA_DIR = './data/fetched'
WRANGLED_DATA_DIR = './data/wrangled'
BASE_FILENAMES = ['seven_major_felony_offenses_by_precinct_2000_2014.xls',
    'non_seven_major_felony_offenses_by_precinct_2000_2014.xls',
    'misdemeanor_offenses_by_precinct_2000_2014.xls',
    'violation_offenses_by_precinct_2000_2014.xls']

# All 4 of these spreadsheets have Row 3, i.e. row 2 in a 0-based index:
HEADERS_ROW_NUMBER = 2
CATEGORIES_COL_NUMBER = 1
OUTPUT_FIELDNAMES = ['precinct', 'year', 'category', 'incident_count']

makedirs(WRANGLED_DATA_DIR, exist_ok = True)


for fname in BASE_FILENAMES:
    source_path = join(FETCHED_DATA_DIR, fname)
    dest_path = join(WRANGLED_DATA_DIR, fname + '.csv')
    print("Wrangling", source_path, "into", dest_path)
    book = open_workbook(source_path)
    sheet = book.sheets()[0]
    headers = sheet.row_values(HEADERS_ROW_NUMBER)

    output_file = open(dest_path, 'w')
    output_csv = DictWriter(output_file, fieldnames = OUTPUT_FIELDNAMES)
    output_csv.writeheader()
    for row_num in range(HEADERS_ROW_NUMBER + 1, sheet.nrows):
        row_vals = [str(val) for val in sheet.row_values(row_num)]
        if re.search(pattern = r'^\d+\.0$', string = row_vals[0]):
            # whatever...
            precinct_num = int(float(row_vals[0]))
            print("precinct:", precinct_num)
            category = re.search(pattern = r'^[^(]+',
                        string = row_vals[CATEGORIES_COL_NUMBER]).group()
            if not re.search(pattern = r'^TOTAL', string = category):
                print("category:", category)
                for col_idx in range(CATEGORIES_COL_NUMBER + 1, sheet.ncols):
                    year = int(headers[col_idx])
                    # for some situations, an incident does not exist, i.e. it is None, rather
                    # than 0, e.g. Precinct 121, post-2012
                    incident_count = int(float(row_vals[col_idx])) if row_vals[col_idx] else None
                    print(year, ":", incident_count)
                    # FINALLY, we can write to the CSV
                    d = {'precinct': precinct_num,
                        'year': year,
                        'category': category,
                        'incident_count': incident_count                    }
                    output_csv.writerow(d)



