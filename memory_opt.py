import pandas as pd
import numpy as np 

def memory_opt(df:pd.DataFrame, datetime_features:list = [], threshold:float = 0.1, obj2cat = True):
    """ reduces memory usage of a pandas dataframe"""
    
    m_b = df.memory_usage(deep = True).sum() / 1024**2
    
    # downcasting floats
    for i in df.select_dtypes(include='float').columns:
        df[i] = pd.to_numeric(df[i],downcast = 'float')
        
        if (df[i]%1 == 0).any():
            df[i] = pd.to_numeric(df[i],downcast = 'integer')
    
    # downcasting ints
    for i in df.select_dtypes(include=['int8','int64','int32']).columns:
        
        df[i] = pd.to_numeric(df[i],downcast = 'integer')
        
    # downcasting objects
    for col in df.select_dtypes(include=['object']).columns:
        if col not in datetime_features:
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if obj2cat:
                if float(num_unique_values) / num_total_values  < threshold:
                    df[col] = df[col].astype('category')
        else:
            df[col] = pd.to_datetime(df[col])
        
    m_a = df.memory_usage(deep = True).sum() / 1024**2
    
    
    print(f'dataframe memory usage before optimization : {m_b} Mb')
    print(f'dataframe memory usage : {m_a} Mb')