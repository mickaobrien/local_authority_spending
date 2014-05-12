import pandas as pd
import xlrd
from jinja2 import Environment,FileSystemLoader 


def create_html_page():
    """
    Create index.html showing tables of Income and Expenditure outliers.
    """

    exp_outliers = get_outliers('Expenditure')
    inc_outliers = get_outliers('Income')

    # Sort by multiple of median
    sorter = lambda x: x['multiple']
    exp_outliers.sort(key=sorter, reverse=True)
    inc_outliers.sort(key=sorter, reverse=True)

    # Load html template
    env = Environment(loader = FileSystemLoader('./templates/'))
    template = env.get_template('base.html')

    # Render html
    html = template.render(income = inc_outliers, expenditure = exp_outliers)

    # Write to index.html
    with open('index.html', 'w') as f:
        f.write(html)

def get_outliers(inc_or_exp='Expenditure', median_multiple=5):
    """
    Finds income or expenditure that is greater than median_multiple times the median percentage income or expenditure.
    
    Returns a list of dicts containing local authority name, percentage, field name, median and multiple of median.
    """
    xls_file = 'data/Local-Authority-Raw-Data.xlsx'

    council_data = pd.read_csv('data/local_authorities.csv')

    #column_names = council_data.columns.tolist()
    column_names = get_headings(xls_file)

    #best = {}
    outliers = []

    for col in column_names[inc_or_exp]:
        percent_col = '%s Perc' % col
        council_data[percent_col] = council_data[col]/council_data['Total %s' % inc_or_exp]

        col_median = council_data[percent_col].median()
        filter_big = (council_data[percent_col] > median_multiple*col_median) & (council_data[percent_col] > 0.01)

        fields = ['County', percent_col]
        big_values = council_data[filter_big][fields].values.tolist()

        to_dict = lambda x: {
                             'county': x[0],
                             'value': x[1],
                             'name': col,
                             'median': col_median,
                             'multiple': x[1]/col_median if col_median !=0 else 0
                             }

        county_dicts = map(to_dict, big_values)

        outliers += county_dicts
    
    return outliers

        

        #best_county, value = council_data.sort(percent_col, ascending=False)[['County', percent_col]].head(1).values.tolist()[0]
        #median_value = council_data[percent_col].median()

        #best_data = {
                     #'county': best_county,
                     #'name': col,
                     #'value': value,
                     #'median': median_value,
                     #'multiple': value/median_value if median_value != 0 else 0
                    #}

        #if best_county not in best:
            #best[best_county] = best_data
        #else: 
            #county_data = council_data[council_data.County == best_county]
            #old_val = best[best_county]['value']
            #new_val = best_data['value']

            #if old_val < new_val:
                #best[best_county] = best_data

     #convert to list of dicts
    #counties_list = [best[county] for county in best.keys()]
    #return counties_list


def get_headings(filename):
    """
    Get headings from Local Authority spreadsheet. Reads the columns headings in the first sheet.
    
    Returns a dict containing headings grouped in either Income or Expenditure.
    """
    xls = xlrd.open_workbook(filename)
    sheet = xls.sheet_by_index(0)
    headings = sheet.col_values(0)

    expenditure_start = headings.index('Total Expenditure')
    income_start = headings.index('Total Income')

    expenditure_headings = [h for h in headings[expenditure_start + 1:income_start] if h]
    income_headings = [h for h in headings[income_start + 1:] if h]

    #groups = {'Income': group_headings(income_headings),
              #'Expenditure': group_headings(expenditure_headings)}
    groups = {'Income': income_headings,
              'Expenditure': expenditure_headings}

    return groups
