import pandas as pd
import os.path as path
# try:
#     from urllib.parse import urlparse
#     from urllib.request import request
# except ImportError:
#     try:
#         from urlparse import urlparse
#         from urlrequest import request
#     except ImportError:
#         print('Sorry ran out of options')

import urllib.parse as urlparse
import urllib.request as request

def import_func(file_or_url):
    # Locate the text at the last period '.'
    _, extn = path.splitext(file_or_url)
    extn_fns = {  '.csv':pd.read_csv
                , '.xls':pd.read_excel
                , '.xlsx':pd.read_excel
                , '.json':pd.read_json
                , '.html':pd.read_html
            }
    return extn_fns[extn]
def is_valid_url(url):
    rslt = urlparse.urlparse(url)
    is_url = all([rslt.scheme, rslt.netloc, rslt.path])
    
    is_url_valid = False
    
    if is_url:
        try:
            with request.urlopen(url) as resp:
                is_url_valid = (resp.status == 200)
        except Exception as exn:
            is_url_valid = False
            print(f'There was an error {exn}')
        else:
            is_url_valid = True
            
    return is_url_valid
def apply_index(df, idx=None):
    right_type = type(idx) == list or type(idx) == str
    idx_in_df = set(idx).issubset(set(df))

    if right_type and idx_in_df:
        df.set_index(keys=idx,inplace=True)
    else:
        # TODO: Fix this later, check if the index already exists
        #print(f"Index not applied {idx} [Type {right_type}] [Subset {idx_in_df}]")
        pass

    return df

def CreateDataFrame(file_name, idx=None, remove_nulls=True):
    file_name = file_name.strip()
    state = []

    apply_func = import_func(file_name)
    if is_valid_url(file_name):
        state.append('Valid url')
    else:
        if not path.exists(file_name):
            print(f'Had problems locating the data [{file_name}]')
            return pd.DataFrame()

    # Import File based on file extension
    df = apply_func(file_name, index_col=idx, parse_dates=True, infer_datetime_format=True)
    state.append('imported')

    # TODO: Index already applied
    #if idx is not None:
    #    df = apply_index(df, idx=idx)

    if remove_nulls:
        df.dropna(inplace=True)

    print(state)

    return df

if __name__ == "__main__":
    # execute only if run as a script
    if is_valid_url('https://www.youtube.com/watch?v=ucY6NwQTI3M&list=RDMMnQWFzMvCfLE&index=9'):
        print(urlparse.urlparse('https://www.youtube.com/watch?v=ucY6NwQTI3M&list=RDMMnQWFzMvCfLE&index=9'))
    #main()
