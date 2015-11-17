# Compiling NYPD stats

Just discovered that the NYPD [publishes historical precinct-level annual crime data as spreadsheets](http://www.nyc.gov/html/nypd/html/analysis_and_planning/historical_nyc_crime_data.shtml).

The 2000 to 2014 Excel spreadsheets can be found at these direct links:

- [Citywide Seven Major Felony Offenses by Precinct 2000 - 2014](http://www.nyc.gov/html/nypd/downloads/excel/analysis_and_planning/seven_major_felony_offenses_by_precinct_2000_2014.xls)
- [Non Seven Major Felony Offenses by Precinct 2000 - 2014](http://www.nyc.gov/html/nypd/downloads/excel/analysis_and_planning/non_seven_major_felony_offenses_by_precinct_2000_2014.xls)
- [Misdemeanor Offenses by Precinct 2000 - 2014](http://www.nyc.gov/html/nypd/downloads/excel/analysis_and_planning/misdemeanor_offenses_by_precinct_2000_2014.xls)
- [Violation Offenses by Precinct 2000 - 2014](http://www.nyc.gov/html/nypd/downloads/excel/analysis_and_planning/violation_offenses_by_precinct_2000_2014.xls)

# Contents

- [`fetch_data.py`](fetch_data.py) - Simply fetches the 4 spreadsheets on the [NYPD site](http://www.nyc.gov/html/nypd/html/analysis_and_planning/historical_nyc_crime_data.shtml).
- [`wrangle_data.py`](wrangle_data.py) - Opens each Excel file and does an awkward loop-de-loop parsing thingy to pluck out the relevant rows and turn the "wide", year-columnar data into [Hadley Wickham's "tidy" data](http://vita.had.co.nz/papers/tidy-data.pdf). Each spreadsheet is saved as a separate CSV file.
- [`compile_data.py`](compile_data.py) - Simply concats the files in the [`data/wrangled/` folder](data/wrangled/) into a single file, [`data/compiled/nypd-precinct-historical-crime-data.csv`](data/compiled/nypd-precinct-historical-crime-data.csv)


(Yeah there could be other kinds of historical NYPD crime data, but I didn't bother to namespace things. Whatever)


## How the data is tidied

In each spreadsheet, the data looks like this:

| PCT |    CRIME     | 2001 | 2002 | 2003 |
|-----|--------------|------|------|------|
| 555 | ROBBERY      |    4 |    6 |    3 |
| 555 | MURDER       |    0 |    1 |    0 |
| 555 | TOTAL CRIMES |    4 |    7 |    3 |
| 999 | ROBBERY      |      |   20 |   40 |
| 999 | MURDER       |      |    5 |   15 |
| 999 | TOTAL CRIMES |      |   25 |   55 |


The [`wrangle_data.py`](wrangle_data.py) script tidies the data, as per [Hadley Wickham's term](http://vita.had.co.nz/papers/tidy-data.pdf), to make it suitable for insertion into a database, e.g. change it to a vertical orientation and remove the redundant aggregation rows (i.e. `TOTAL CRIMES`):

| precinct | category | year | incident_count |
|----------|----------|------|----------------|
|      555 | ROBBERY  | 2001 |              4 |
|      555 | ROBBERY  | 2002 |              6 |
|      555 | ROBBERY  | 2003 |              3 |
|      555 | MURDER   | 2001 |              0 |
|      555 | MURDER   | 2002 |              1 |
|      555 | MURDER   | 2003 |              0 |
|      999 | ROBBERY  | 2001 |                |
|      999 | ROBBERY  | 2002 |             20 |
|      999 | ROBBERY  | 2003 |             40 |
|      999 | MURDER   | 2001 |                |
|      999 | MURDER   | 2002 |              5 |
|      999 | MURDER   | 2003 |             15 |


## How to run the scripts

Works on Python 3.x and uses the [requests](http://docs.python-requests.org/en/latest/) and [xlrd](https://pypi.python.org/pypi/xlrd) libraries.

~~~sh
python3 ./fetch_data.py
python3 ./wrangle_data.py
python3 ./compile_data.py
~~~



# About the NYPD crime stats

## Hooray for Excel files

In the past, the NYPD has published PDF reports, which are substantially more difficult to parse. No matter how ugly you think my use of the [xlrd library is](wrangle_data.py), it could be a lot worse. Also, before 2014, most [reports were only at the citywide level](https://web.archive.org/web/20130724044422/http://www.nyc.gov/html/nypd/html/analysis_and_planning/historical_nyc_crime_data.shtml), which made precinct-level comparisons impossible even if you got to parsing the PDFs.

## Caveats about the data

Open the spreadsheets for yourself to see the notes at the bottom. The most important caveats relate to precinct boundary changes, which would invalidate year-over-year comparisons for the affected precincts.

Here are the caveats verbatim:

- On Sept. 28, 2012, there was a re-alignment of the boundaries of the 077, 078, and 088 precincts.  Therefore statistics for the 077, 078, and 088 precincts following 2011 are not comparable to earlier years.
- The 121 pct was created on 7-1-2013 from parts of the 120 and 122 precinct.  Therefore statistics for 120 and 122 precincts following 2012 are not comparable to earlier years.

Here's a table listing the changes by precinct:

| Precinct | 2012 | 2013 |
|----------|------|------|
|       77 | X    |      |
|       78 | X    |      |
|       88 | X    |      |
|      120 |      | X    |
|      121 |      | X    |
|      122 |      | X    |
