import pandas as pd
import numpy as np


def createDecile(resp:pd.Series,score:pd.Series,buckets:int=10) -> pd.DataFrame:

    """Takes as input score and binary response and outputs an aggregate dataframe grouped by decile
    with columns for gain, lift and KS   

    Args
    resp : list or dataframe with binary response for each instance
    score : list or dataframe with score for each instance
    buckets : number of divisions desired default = 10 (decile)      
      
    Return
    agg : Dataframe with aggregated data       
    """        
    
    input_df=pd.DataFrame({'resp':resp,'score':score})      
    input_df['neg_resp'] = 1-input_df['resp']               
    input_df['decile'] = pd.qcut(input_df['score'],buckets,duplicates='drop')
    binned_df = input_df.groupby('decile', as_index = False)
    
    aggregated_df = pd.DataFrame()
    aggregated_df['min_score'] = binned_df.min().score.apply('{0:.3f}'.format)
    aggregated_df['max_score'] = binned_df.max().score.apply('{0:.3f}'.format)
    aggregated_df['resp'] = binned_df.sum().resp
    aggregated_df['n_resp'] = binned_df.sum().neg_resp
    aggregated_df['total'] = (aggregated_df['resp'] + aggregated_df['n_resp'])
    aggregated_df['resp_ratio'] = (aggregated_df['resp'] / aggregated_df['total']).apply('{0:.1%}'.format)
    aggregated_df['mean_score'] = binned_df.mean().score.apply('{0:.3f}'.format)        
    
    sorted_df = (aggregated_df.sort_values(by = 'max_score', ascending = False)).reset_index(drop = True)
    sorted_df['gain'] = (sorted_df['resp'].cumsum()/sorted_df['resp'].sum()).apply('{0:.1%}'.format)
    sorted_df['cum_lift'] = ((sorted_df['resp'].cumsum()/sorted_df['resp'].sum())/(sorted_df.total.cumsum()/sorted_df.total.sum())).apply('{0:.2f}'.format)
    sorted_df['lift'] = ((sorted_df['resp']/sorted_df.total)/(sorted_df['resp'].sum()/sorted_df.total.sum())).apply('{0:.2f}'.format)
    sorted_df['KS'] = np.round(((sorted_df['resp'] / sorted_df['resp'].sum()).cumsum() - (sorted_df['n_resp'] / sorted_df['n_resp'].sum()).cumsum()), 4) * 100
    
    mark = lambda x: '◄─    ' if x == sorted_df.KS.max() else ''
    sorted_df['max_KS'] = sorted_df.KS.apply(mark)
    sorted_df.index +=1
    
    return sorted_df