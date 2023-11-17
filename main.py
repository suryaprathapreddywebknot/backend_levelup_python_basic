import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def import_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

df=import_dataset('./dataset/movies_initial.csv')

# Function to filer data based on language
def filter_by_language(df, language):
    filtered_df = df[df['language'].str.contains(language, case=False, na=False)]
    return filtered_df

# Function to filer data based on country
def filter_by_country(df, country):
    filtered_df = df[df['country'].str.contains(country, case=False, na=False)]
    return filtered_df

# Function to filer data based on IMDB rating
def filter_high_ratings(df):
    filtered_df = df[(df['imdbRating'] > 7) & (df['imdbVotes'] > 1000)]
    return filtered_df



def _draw_as_table(df, pagesize, fontsize=12):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                        rowLabels=df.index,
                        colLabels=df.columns,
                        rowColours=['lightblue']*len(df),
                        colColours=['lightblue']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center', fontsize=fontsize)
    return fig
  
def dataframe_to_pdf(df, filename, numpages=(1, 1), pagesize=(11, 8.5), exclude_columns=[], fontsize=12):
    with PdfPages(filename) as pdf:
        nh, nv = numpages
        rows_per_page = len(df) // nh
        cols_per_page = len(df.columns) // nv
        for i in range(0, nh):
            for j in range(0, nv):
                page = df.iloc[(i * rows_per_page):min((i + 1) * rows_per_page, len(df)),
                               (j * cols_per_page):min((j + 1) * cols_per_page, len(df.columns))]
                
                page = page.drop(columns=exclude_columns, errors='ignore')
                
                fig = _draw_as_table(page, pagesize, fontsize)
                
                if nh > 1 or nv > 1:
                    fig.text(0.5, 0.5/pagesize[0],
                             "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                             ha='center', fontsize=8)
                
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()



dataframe_to_pdf(filter_by_language(df,'Telugu'),'telugu_movies.pdf',exclude_columns=['poster','plot','fullplot'])

dataframe_to_pdf(filter_by_country(df,'India'),'Indian_Movies.pdf',exclude_columns=['poster','plot','fullplot'])

dataframe_to_pdf(filter_high_ratings(df),'top_rated_movies.pdf',exclude_columns=['poster','plot','fullplot'])