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
    
    input_df=pd.DataFrame({'target_1':resp,'score':score})      
    input_df['target_0'] = 1-input_df['target_1']               
    input_df['decile'] = pd.qcut(input_df['score'],buckets,duplicates='drop')
    binned_df = input_df.groupby('decile', as_index = False)
    
    aggregated_df = pd.DataFrame()
    aggregated_df['min_score'] = binned_df.min().score.apply('{0:.3f}'.format)
    aggregated_df['max_score'] = binned_df.max().score.apply('{0:.3f}'.format)
    aggregated_df['target_1'] = binned_df.sum().target_1
    aggregated_df['target_0'] = binned_df.sum().target_0
    aggregated_df['total'] = (aggregated_df['target_1'] + aggregated_df['target_0'])
    aggregated_df['target_1_ratio'] = (aggregated_df['target_1'] / aggregated_df['total']).apply('{0:.1%}'.format)
    aggregated_df['mean_score'] = binned_df.mean().score.apply('{0:.3f}'.format)        
    
    sorted_df = (aggregated_df.sort_values(by = 'max_score', ascending = False)).reset_index(drop = True)
    sorted_df['gain'] = (sorted_df['target_1'].cumsum()/sorted_df['target_1'].sum()).apply('{0:.1%}'.format)
    sorted_df['lift'] = ((sorted_df['target_1']/sorted_df.total)/(sorted_df['target_1'].sum()/sorted_df.total.sum())).apply('{0:.2f}'.format)
    sorted_df['KS'] = np.round(((sorted_df['target_1'] / sorted_df['target_1'].sum()).cumsum() - (sorted_df['target_0'] / sorted_df['target_0'].sum()).cumsum()), 4) * 100
    
    mark = lambda x: '◄─    ' if x == sorted_df.KS.max() else ''
    sorted_df['max_KS'] = sorted_df.KS.apply(mark)
    sorted_df.index +=1
    
    return sorted_df