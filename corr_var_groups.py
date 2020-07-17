import numpy as np

def corrGroups(df:pd.DataFrame,corr_tresh:float=0.9) -> list:
    """creates a list of lists with groups of variables that have a pearson correlation 
    bigger than corr_tresh among each other"""
    
    corrMatrix = df.corr().abs()
    corrMatrix.loc[:,:] =  np.tril(corrMatrix, k=-1)
    corrMatrix = corrMatrix[corrMatrix > corr_tresh].dropna(how='all').dropna(axis=1,how='all')
    corrMatrix['corr_groups'] = corrMatrix.apply(lambda x:sum([[x.name],x.index[x.notna()].tolist()],[]), axis=1)
    corrMatrix['max'] = corrMatrix.max(axis=1)
    
    corrVars = [i for i in corrMatrix.sort_values('max',ascending=False).corr_groups]
    
    remove=[]
    for i in corrVars:
        for j in range(0,len(corrVars)):
            if set(i).issubset(corrVars[j]) and i!=corrVars[j] and i not in remove:
                remove.append(i)
                
    for rm in remove:
        corrVars.remove(rm)
        
    return corrVars