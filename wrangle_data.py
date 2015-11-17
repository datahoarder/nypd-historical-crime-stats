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

makedirs(WRANGLED_DATA_DIR, exist_ok = True)


OUTPUT_FIELDNAMES = ['precinct', 'year', 'category', 'incident_count']

# All 4 of these spreadsheets have Row 3, i.e. row 2 in a 0-based index:
HEADERS_ROW_NUMBER = 2
PRECINCT_COL_NUMBER = 0
CATEGORIES_COL_NUMBER = 1


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
    precinct = False
    category = False
    for row_num in range(HEADERS_ROW_NUMBER + 1, sheet.nrows):
        row_vals = [str(val).strip() for val in sheet.row_values(row_num)]
        # first, determine if the precinct column contains a valid precinct
        precinct_val = row_vals[PRECINCT_COL_NUMBER]
        # if it is a number or 'DOC, then it is a valid precinct number
        if re.search(pattern = r'^\d+\.0$|DOC', string = precinct_val):
            # though it has to be converted from a float if it is a number
            precinct = 'DOC' if precinct_val == 'DOC' else int(float(precinct_val))
            print("\tPrecinct", precinct)
        elif precinct_val == '':   # if the column is blank
            if precinct is False:  # if the current precinct variable is set to false too
                # then we're done here
                break
            else:
                pass # move on to the category iteration
        else: # Any other situation is unexpected
            errmsg = "Unexpected precinct value; %s ; in row: %s" % (precinct_val, row_num)
            raise ValueError(errmsg)

        # At this point in the loop, the precinct has been set...now we check to see if
        # we're on a valid category (i.e not a "TOTAL" type category)
        category_val = row_vals[CATEGORIES_COL_NUMBER]
        if re.search(pattern = r'^TOTAL', string = category_val):
            precinct = False
            continue # moving on

        # OK, we're on a valid precinct and a valid category (ostensibly)
        # note that this regex gets the entire string except for the parenthetical notes:
        category = re.search(pattern = r'^[^(]+', string = category_val).group().strip()
        # now we iterate horizontally to get the year data
        print("\t\t", category)
        for col_idx in range(CATEGORIES_COL_NUMBER + 1, sheet.ncols):
            year = int(headers[col_idx])
            # for some situations, an incident does not exist, i.e. it is None, rather
            # than 0, e.g. Precinct 121, post-2012
            incident_count = int(float(row_vals[col_idx])) if row_vals[col_idx] else None
            print("\t\t\t", year, ":", incident_count)
            ##################################
            # FINALLY, we can write to the CSV
            d = {'precinct': precinct,
                'year': year,
                'category': category,
                'incident_count': incident_count}
            output_csv.writerow(d)



