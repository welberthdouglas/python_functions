import pandas as pd

def cat_encoding(df, cat_vars:str, encoding:str = 'label'):
    """Encodes cathegorical variables of a dataframe
    
    inputs
    df - dataframe that have variables to encode
    cat_vars - list of variables to encode
    encoding - encoding method (possible values are 'label' or 'one_hot')
    
    output
    df_out - outputs the modified dataframe (with the original columns replaced by the respective
            encoded ones)"""
    
    if encoding == 'label':
        df_cat = pd.DataFrame({col: df[col].astype('category').cat.codes for col in df[cat_vars]}, index=df.index)
        df_out = df.drop(cat_vars, axis=1).merge(df_cat,left_index = True,right_index=True)
    if encoding == 'one_hot':
        df_out = pd.get_dummies(df,columns = cat_vars)
        
    return df_out