#!/usr/bin/env python3
"""
- Original data set can be downloaded from: http://data.ct.gov/coronavirus
                                            https://data.ct.gov/Health-and-Human-Services/COVID-19-Tests-Cases-and-Deaths-By-Town-/28fr-iqnx
- Massage the COVID-19 data so it can be parsed easily by other programs without using external libraries. Headers have hidden UTF-8 chars, etc
- Author: Jose Vicente Nunez
"""
import csv
import sys
from datetime import datetime

if __name__ == "__main__":
    SRC = "COVID-19_case_rate_per_100_000_population_and_percent_test_positivity_in_the_last_14_days_by_town.csv"
    DST = "COVID-19-massaged.csv"
    d_format = "%m/%d/%Y"
    with open(DST, 'w', newline='') as clean_csv:
        writer = csv.writer(clean_csv, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
        with open(SRC, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
               tNumber = int(row['\ufeffTown number'].strip())
               town = row['Town'].strip()
               tPop = int(row['Town population'].replace(",", "").strip())
               tCW1 = row['Cases in Week 1'].strip()
               tCW2 = row['Cases in Week 2'].strip()
               tC2W = int(row['Total cases over 2-week period'].replace(",", "").strip())
               cC2W = row['COVID-19 cases per 100k population over 2-week period'].strip()
               rc = row['Rate category'].replace(",", "_").strip()
               tt = int(row['Total tests'].replace(",", "").strip())
               pcp = row['Percent test positivity'].strip()
               rpsd = datetime.strptime(row['Report period start date'].strip(), d_format).date()
               rped = datetime.strptime(row['Report period end date'].strip(), d_format).date()
               ud = datetime.strptime(row['Update date'].strip(), d_format).date()
               try:
                   row = [tNumber, town, tPop, tCW1, tCW2, tC2W, cC2W, rc, tt, pcp, rpsd, rped, ud]
                   writer.writerow(row)
               except csv.Error:
                   print("Could not write {}".format(row), file=sys.stderr)
                   raise

