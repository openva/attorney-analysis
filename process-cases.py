import csv
import os.path
import sys
from courtreader import readers
from datetime import datetime

csv_fieldnames = []

def parse_datetime(date):
    return datetime.strptime(date, "%m/%d/%y")

def dt_str(date):
    return '{0.month}/{0.day}/{0:%y}'.format(date)

def load_case_file(file_path):
    cases = []
    with open(file_path, 'r') as case_file:
        case_file_reader = csv.DictReader(case_file)
        global csv_fieldnames
        csv_fieldnames = case_file_reader.fieldnames
        for row in case_file_reader:
            row['FIPS'] = row['FIPS'].zfill(3)
            row['FILE_DATE'] = parse_datetime(row['FILE_DATE'])
            row['FINAL_DISP_DATE'] = parse_datetime(row['FINAL_DISP_DATE'])
            cases.append(row)
    return cases

def find_matching_cases(partial_case, cases):
    matching_cases = []
    for i, case in enumerate(cases):
        if case['status'] == 'Finalized':
            print '\tGetting details for case ' + str(i+1) + \
                  ' of ' + str(len(cases)) + '\r',
            sys.stdout.flush()
            case_details = reader.get_case_details(case)
            if cases_match(partial_case, case_details):
                print '\nMATCH ' + case_details['case_number']
                matching_case = partial_case.copy()
                matching_case['FIPS'] = int(matching_case['FIPS'])
                matching_case['FILE_DATE'] = dt_str(matching_case['FILE_DATE'])
                matching_case['FINAL_DISP_DATE'] = dt_str(matching_case['FINAL_DISP_DATE'])
                matching_case['CASE_NUMBER'] = case_details['case_number']
                matching_case['NAME'] = case_details['name']
                matching_case['MATCH'] = len(matching_cases) + 1
                matching_cases.append(matching_case)
    return matching_cases

def case_has_match(partial_case, matched_cases):
    for case in matched_cases:
        if case['FIPS'] == partial_case['FIPS'] and \
           case['FILE_DATE'] == partial_case['FILE_DATE'] and \
           case['OFFENSE_CLASS_CODE'] == partial_case['OFFENSE_CLASS_CODE'] and \
           case['FINAL_DISP_DATE'] == partial_case['FINAL_DISP_DATE']:
           return True
    return False

def cases_match(partial_case, case_details):
    return case_details['filed_date'] == partial_case['FILE_DATE'] and \
           case_details['case_type'] == 'Felony' and \
           case_details['offense_class'] == partial_case['OFFENSE_CLASS_CODE']

reader = readers.DistrictCourtReader()
reader.connect()

case_year = '2014'
partial_cases_file_path = 'cases/' + case_year + '.csv'
matched_cases_file_path = 'cases/' + case_year + '_matched.csv'

matched_cases = []
if os.path.isfile(matched_cases_file_path):
    matched_cases = load_case_file(matched_cases_file_path)
partial_cases = load_case_file(partial_cases_file_path)
csv_fieldnames.extend(['CASE_NUMBER', 'NAME', 'MATCH'])

with open(matched_cases_file_path, 'wb') as matched_cases_file:
    matched_case_writer = csv.DictWriter(matched_cases_file, \
                                         csv_fieldnames)
    matched_case_writer.writeheader()
    for case in matched_cases:
        case_to_file = case.copy()
        case_to_file['FIPS'] = int(case_to_file['FIPS'])
        case_to_file['FILE_DATE'] = dt_str(case_to_file['FILE_DATE'])
        case_to_file['FINAL_DISP_DATE'] = dt_str(case_to_file['FINAL_DISP_DATE'])
        matched_case_writer.writerow(case_to_file)
    matched_cases_file.flush()
    
    for i, partial_case in enumerate(partial_cases):
        print '\nPartial case ' + str(i+1) + ' of ' + str(len(partial_cases))
        if case_has_match(partial_case, matched_cases):
            print '\tAlready Matched',
            continue
        fips_code = partial_case['FIPS']
        search_date = partial_case['FINAL_DISP_DATE']
        cases = reader.get_cases_by_date(fips_code, search_date)
        matching_cases = find_matching_cases(partial_case, cases)
        if len(matching_cases) > 0:
            matched_case_writer.writerows(matching_cases)
        else:    
            partial_case['FIPS'] = int(partial_case['FIPS'])
            partial_case['FILE_DATE'] = dt_str(partial_case['FILE_DATE'])
            partial_case['FINAL_DISP_DATE'] = dt_str(partial_case['FINAL_DISP_DATE'])
            matched_case_writer.writerow(partial_case)
        matched_cases_file.flush()

