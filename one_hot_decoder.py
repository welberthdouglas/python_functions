def onehot_declutter(df, col_in:str, sep:str =','):
    """ transforms a column with multiple string values into one hot encoding"""
    
    string_instances = {item.strip() for i in data[col_in] for item in i.split(sep)}
    
    for string in string_instances:
        df[string.replace(' ','_')] = [1 if string in i else 0 for i in df[col_in]]
    return df
