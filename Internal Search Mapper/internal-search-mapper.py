""" Internal Search Report Mapper V1 by Lee Foot 07/01/2021 @LeeFootSEO
Takes the Google Analytics Search Terms Report and merges with a Screaming Frog crawl file to find opportunities to Map
internal searches to.

1) Search Terms Report must be Exported as an Excel file
2) Screaming Frog Crawl should only contain category pages (unless you really want to map internal searches to products!
3) Paths are hardcoded,please enter your own!
"""

from glob import glob  # Used to parse wildcard for csv import

import pandas as pd

# imports using GA data using a wildcard match
for f in glob('/python_scripts/Internal Search Mapper/Analytics*.xlsx'):  # ENTER YOUR PATH TO THE SEARCH TERM REPORT
    df_ga = pd.read_excel((f), sheet_name='Dataset1')

df_sf = pd.read_csv('/python_scripts/Internal Search Mapper/internal_html.csv', encoding='utf8')[['H1-1', 'Address',
                                                                                                  'Indexability']]

try:  # drop non-indexable pages
    df_sf = df_sf[~df_sf['Indexability'].isin(['Non-Indexable'])]  # Drop Non-indexable Pages
except Exception:
    pass

del df_sf['Indexability']  # delete the helper column

# merge the dataframe
final_df = pd.merge(df_sf, df_ga, left_on="H1-1", right_on="Search Term", how="inner")

# sort by Total Unique Searches column
final_df = final_df.sort_values(by='Total Unique Searches', ascending=False)

# export the final csv
final_df.to_csv('/python_scripts/Internal Search Mapper/output.csv')  # ENTER YOUR PATH HERE!