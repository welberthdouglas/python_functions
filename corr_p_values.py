import pandas as pd

def calculate_pvalues(df:pd.DataFrame,method:str) -> pd.DataFrame:
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            if method == 'pearson':
                pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
            if method == 'spearman':
                pvalues[r][c] = round(spearmanr(df[r], df[c])[1], 4)
            
    return pvalues