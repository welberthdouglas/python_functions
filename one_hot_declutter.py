import pandas as pd

def onehot_declutter(df:pd.DataFrame, col_in:str, sep:str =',', replace = True) -> pd.DataFrame:
    """ transforms a column with multiple string values into one hot encoding"""
    
    string_instances = {item.strip() for i in data[col_in] for item in i.split(sep)}
    
    for string in string_instances:
        df[string.replace(' ','_')] = [1 if string in i else 0 for i in df[col_in]]
    if replace:
        df.drop(columns = col_in, inplace = True)
    return df
