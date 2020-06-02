import pandas as pd
import numpy as np


def decile(score,resp,buckets=10):

        """Takes as input score and binary response and outputs an aggregate dataframe grouped by decile
        with columns for gain, lift and KS

        resp= list or dataframe with binary response for each instance
        score= list or dataframe with score for each instance
        buckets= Use if another bucket division desired default = 10 (decile)
        """

        df0=pd.DataFrame(resp)
        df0['score']=score

        df=df0.copy()
        df[2] = 1-df.iloc[:,0] # creating the negative response column       
        df.columns = ['resp','score','neg_resp']

        df['decile'] = pd.qcut(df.iloc[:,1],buckets,duplicates='drop') # defining deciles
        df = df.groupby('decile', as_index = False) # aggregating data
        
        agg = pd.DataFrame()
        agg['min_' + str(df0.columns[1])] = df.min().score.apply('{0:.3f}'.format)
        agg['max_' + str(df0.columns[1])] = df.max().score.apply('{0:.3f}'.format)
        agg[df0.columns[0]] = df.sum().resp
        agg['n_'+ str(df0.columns[0])] = df.sum().neg_resp
        agg['total'] = (agg[df0.columns[0]] + agg['n_'+ str(df0.columns[0])])
        agg[str(df0.columns[0]) + '_ratio'] = (agg[df0.columns[0]] / agg.total).apply('{0:.1%}'.format)
        agg['mean_score'] = df.mean().score.apply('{0:.3f}'.format)

        agg = (agg.sort_values(by = 'max_' + str(df0.columns[1]), ascending = False)).reset_index(drop = True)
        
        agg['gain'] = (agg[df0.columns[0]].cumsum()/agg[df0.columns[0]].sum()).apply('{0:.1%}'.format)
        #agg['cum % n_resp'] = (agg['n_'+ str(df0.columns[0])].cumsum()/agg['n_'+ str(df0.columns[0])].sum()).apply('{0:.1%}'.format)
        
        agg['lift_cum'] = ((agg[df0.columns[0]].cumsum()/agg[df0.columns[0]].sum())/(agg.total.cumsum()/agg.total.sum())).apply('{0:.2f}'.format)
        agg['lift'] = ((agg[df0.columns[0]]/agg.total)/(agg[df0.columns[0]].sum()/agg.total.sum())).apply('{0:.2f}'.format)
        agg['KS'] = np.round(((agg[df0.columns[0]] / agg[df0.columns[0]].sum()).cumsum() - (agg['n_'+ str(df0.columns[0])] / agg['n_'+ str(df0.columns[0])].sum()).cumsum()), 4) * 100
        
        mark = lambda x: '◄─    ' if x == agg.KS.max() else ''
        agg['max_KS'] = agg.KS.apply(mark)
        agg.index +=1
        
        return agg
