# Import necessary libraries
import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

# Load the cleaned dataset from a CSV file into a DataFrame
hk_movies = pd.read_csv('hk_cleaned_imdb_top_1000.csv')

# Initialize a sentence transformer model for generating text embeddings
hk_model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for the consolidated movie information in the DataFrame
# This converts the text information into a numerical format that machines can work with
hk_movie_embeddings = hk_model.encode(hk_movies['hk_embedded_text'].tolist(), show_progress_bar=True)

# Initialize an Elasticsearch client to communicate with an Elasticsearch cluster
# The basic_auth parameter is used for authentication with the cluster
hk_es = Elasticsearch("http://localhost:9200", basic_auth=('elastic', 'sT94YBrOD+*D0NxK_I8N'))

# Define a function to store movie embeddings and additional details in Elasticsearch
def hk_store_embeddings(hk_index, hk_movie_id, hk_movie_name, hk_genre, hk_released_year, hk_embedding):
    # Prepare the document to be stored, converting the numpy array of the embedding to a list
    hk_document = {
        "movie_id": hk_movie_id,
        "Series_Title": hk_movie_name,
        "Genre": hk_genre,
        "Released_Year": hk_released_year,
        "embedding": hk_embedding.tolist()
    }
    # Use the Elasticsearch index API to store the document in a specified index
    hk_es.index(index=hk_index, id=hk_movie_id, document=hk_document)

# Loop over each row in the DataFrame and store the corresponding movie embedding
# along with the movie name, genre, and year of release in Elasticsearch
for hk_row in hk_movies.itertuples():
    hk_store_embeddings("movie_embeddings", hk_row.Index, hk_row.Series_Title, hk_row.Genre, hk_row.Released_Year, hk_movie_embeddings[hk_row.Index])

# Print a message to indicate successful storage of embeddings and movie information in Elasticsearch
print("Embeddings along with genre and year of release created and stored in Elasticsearch successfully.")
