import xlrd
import csv

FILE_NAME = 'Local-Authority-Raw-Data.xlsx'

def xls2csv():
    data = get_all_data()
    dicts_to_csv(data, 'local_authorities.csv')

def get_all_data():
    xls = xlrd.open_workbook(FILE_NAME, on_demand=True)
    sheet_names = xls.sheet_names()

    all_data = []

    for sheet in sheet_names:
        county_vals = parse_sheet(xls, sheet)
        all_data.append(county_vals)

    return all_data

def dicts_to_csv(dicts, filename):
    """ Write a list of dicts to a csv file. """
    f = open(filename, 'wb')
    keys = dicts[0].keys()
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writer.writerow(keys)
    dict_writer.writerows(dicts)

def parse_sheet(xls, sheet_name):
    sheet = xls.sheet_by_name(sheet_name)
    nrows = sheet.nrows

    values = {}

    for i in range(nrows):
        row = sheet.row_values(i)
        key = row[0]

        if key:
            key = key.replace(':', '')
            values[key] = row[1]

    return values


def sort_headings(xls, sheet_name):
    sheet = xls.sheet_by_name(sheet_name)
    headings = sheet.col_values(0)

    expenditure_start = headings.index('Total Expenditure')
    income_start = headings.index('Total Income')

    expenditure_headings = headings[expenditure_start + 1:income_start]
    income_headings = headings[income_start + 1:]

    groups = {'Income': group_headings(income_headings),
              'Expenditure': group_headings(expenditure_headings)}

    return groups


def group_headings(headings):

    groups = []
    group = []

    for head in headings:
        if head:
            group.append(head)
        else:
            if group:
                groups.append(group)
                group = []

    if group:
        groups.append(group)

    return groups


def group_values(values, headings):
    for head in headings:
        title = head[0]
        out[title] = {}
        out[title]['Total'] = values[title]

        if len(head) > 1:
            out[title]['Details'] = {}
            for deet in head[1:]:
                out[title]['Details'][deet] = values[deet]

    return out
