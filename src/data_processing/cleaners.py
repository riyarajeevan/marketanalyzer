import pandas as pd
import numpy as np

class DataCleaner:
    @staticmethod
    def remove_missing_values(df, method='forward_fill', threshold=None):
        df = df.copy()
        
        if threshold is not None:
            missing_pct = df.isnull().sum() / len(df)
            cols_to_drop = missing_pct[missing_pct > threshold].index
            df = df.drop(columns=cols_to_drop)
        
        if method == 'forward_fill':
            df = df.fillna(method='ffill')
        elif method == 'backward_fill':
            df = df.fillna(method='bfill')
        elif method == 'interpolate':
            df = df.interpolate(method='linear')
        elif method == 'drop':
            df = df.dropna()
        
        return df
    
    @staticmethod
    def remove_outliers(df, method='iqr', threshold=3.0, columns=None):
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        mask = pd.Series([True] * len(df))
        
        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR
                col_mask = (df[col] >= lower) & (df[col] <= upper)
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                col_mask = z_scores < threshold
            else:
                col_mask = pd.Series([True] * len(df))
            
            mask = mask & col_mask
        
        return df[mask]
    
    @staticmethod
    def align_dataframes(dfs, method='inner'):
        if len(dfs) < 2:
            return dfs
        
        indices = [df.index for df in dfs]
        
        if method == 'inner':
            common_index = indices[0]
            for idx in indices[1:]:
                common_index = common_index.intersection(idx)
        elif method == 'outer':
            common_index = indices[0]
            for idx in indices[1:]:
                common_index = common_index.union(idx)
        else:
            common_index = indices[0]
        
        aligned = [df.reindex(common_index) for df in dfs]
        return aligned
    
    @staticmethod
    def resample_data(df, freq, method='last'):
        if method == 'last':
            return df.resample(freq).last()
        elif method == 'first':
            return df.resample(freq).first()
        elif method == 'mean':
            return df.resample(freq).mean()
        elif method == 'sum':
            return df.resample(freq).sum()
        else:
            return df
