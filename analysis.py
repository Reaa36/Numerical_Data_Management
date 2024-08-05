import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def get_statistics(df):
    numeric_df = df.select_dtypes(include=['number'])
    stats = {
        'mean': df.mean(),
        'median': df.median(),
        'std': df.std()
    }
    return stats

def save_statistics(stats, file_path):
    with open(file_path, 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}:\n{value}\n\n")

def add_row(df, new_row):
    df = df.append(new_row, ignore_index=True)
    return df

def update_row(df, index, updated_row):
    df.loc[index] = updated_row
    return df

def delete_row(df, index):
    df = df.drop(index).reset_index(drop=True)
    return df