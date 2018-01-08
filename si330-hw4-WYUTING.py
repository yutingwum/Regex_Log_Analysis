# -*- coding: utf-8 -*-
#!/usr/bin/python -tt
import re
import csv
from collections import defaultdict


def write_log_entries(filename, list_of_rows_to_write):
    row_counter = 0
    with open(filename, 'w+', newline = '') as f:
        row_writer = csv.DictWriter(f, delimiter='\t', quotechar='"', extrasaction='ignore',
                                    fieldnames=["IP", "Ignore1", "Ignore2", "Timestamp", "Ignore3", "HTTP_Verb",
                                                "HTTP_Status", "HTTP_Duration", "HTTP_Redirect", "Browser_Type",
                                                "Top_Level_Domain"])
        row_writer.writeheader()
        for row in list_of_rows_to_write:
            row_writer.writerow(row)
            row_counter = row_counter + 1

    print("Wrote {} rows to {}".format(row_counter, filename))

# Function get_top-level_domain:
#    Input:  A string containing a URL
#    Output:  the top-level domain in the URL, or None if no valid top-level domain was found.  The top-level
#             domain, if it exists, should be normalized to always be in lower case.

def get_toplevel_domain(url):
    ### Use re.search here with the appropriate regular expression to look for a match
    ### Hint: define a group to pull out the top-level domain from the match
    #match = re.search(r'((http:\/\/|https:\/\/)[a-zA-Z]+[0-9]*\.[a-zA-Z0-9]+\.(\w*)(\D*)', url)
    #match = re.search(r'(http[s]?://([a-zA-Z]+[a-zA-Z0-9.-]+\.)([a-zA-Z]+))\D*[0-9]*', url)
    #match = re.search(r'(http[s]?://([a-zA-Z]+[a-zA-Z0-9.-]+\.)([a-zA-Z]+))[0-9\/:]*', url)
    match = re.search(r'(http[s]?://([a-zA-Z]+[a-zA-Z0-9.-]+\.)([a-zA-Z]+))[0-9\/:]*', url)
    if match == None:
        return None
    return match.group(3).lower()

# Function read_log_file:
#   Input: the file name of the log file to process
#   Output:  A two-element tuple with element 0 a list of valid rows, and element 1 a list of invalid rows
def read_log_file(filename):
    valid_entries   = []
    invalid_entries = []

    with open(filename, 'r', newline='') as input_file:
        log_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"', skipinitialspace=True,
                                         fieldnames=["IP","Ignore1","Ignore2","Timestamp","Ignore3","HTTP_Verb","HTTP_Status","HTTP_Duration","HTTP_Redirect","Browser_Type"])
        for row in log_data_reader:
            not_a_valid_line = False
            check_https = re.search(r"(^GET|^POST)\s+(http:\/\/|https:\/\/)[a-zA-Z]+[0-9.\w-]*", row['HTTP_Verb'])
            toplevel_domain = get_toplevel_domain(row['HTTP_Verb'])


            if check_https != None and row['HTTP_Status'] == '200' and toplevel_domain != None and toplevel_domain.isalpha():
                row['Top_Level_Domain'] = toplevel_domain
                pass
            else:
                not_a_valid_line = True

            if not_a_valid_line:
                if check_https != None:
                    row['Top_Level_Domain'] = toplevel_domain
                invalid_entries.append(row)
                continue

            # if we get here, it's a valid line
            valid_entries.append(row)


    return (valid_entries, invalid_entries)

def main():
    valid_rows, invalid_rows = read_log_file(r'access_log.txt')
    #valid_rows, invalid_rows = read_log_file(r'access_log_first_1000_lines.txt')

    write_log_entries('valid_access_log_WYUTING.txt', valid_rows)
    write_log_entries('invalid_access_log_WYUTING.txt', invalid_rows)

# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()

