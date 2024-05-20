# Import required libraries
import streamlit as st  # For creating the web app
from sentence_transformers import SentenceTransformer  # For embedding generation
from elasticsearch import Elasticsearch  # For querying Elasticsearch
import pandas as pd  # For data manipulation

# Set Streamlit page configuration for better layout
st.set_page_config(layout="wide")

# Define the model loading function (cached for performance)
# This function loads the SentenceTransformer model which is used to generate embeddings
@st.cache(allow_output_mutation=True)
def load_model():
    # Here the model 'all-MiniLM-L6-v2' is a compact and efficient model for generating embeddings
    return SentenceTransformer('all-MiniLM-L6-v2')

# Load the SentenceTransformer model
model = load_model()

# Initialize the Elasticsearch client to communicate with the Elasticsearch server
# 'basic_auth' is used for authentication with username 'elastic' and a password
es = Elasticsearch("http://localhost:9200", basic_auth=('elastic', 'sT94YBrOD+*D0NxK_I8N'))

# Function to perform the search for similar movies
def search_similar_movies(query, top_n=10):
    # Generate embedding for the query
    query_embedding = model.encode([query])[0].tolist()
    # Define the script query for Elasticsearch
    # This script calculates the cosine similarity between the query vector and document embeddings
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_embedding}
            }
        }
    }
    # Execute the search query on Elasticsearch
    response = es.search(
        index="movie_embeddings",  # Name of the Elasticsearch index
        query=script_query,
        size=top_n,  # Number of top results to return
        _source=["movie_id", "Series_Title", "Genre", "Released_Year"]  # Fields to return for each document
    )
    # Process the search results and prepare a DataFrame
    movies_found = [
        {
            "Movie ID": hit['_source'].get('movie_id', 'N/A'),
            "Title": hit['_source'].get('Series_Title', 'Unknown'),
            "Genre": hit['_source'].get('Genre', 'Unknown'),
            "Released Year": hit['_source'].get('Released_Year', 'Unknown')
        }
        for hit in response['hits']['hits']
    ]
    return pd.DataFrame(movies_found)

# Streamlit UI components for the web app
st.title('Movie Search App 🎬')

# Layout for input and slider using columns
col1, col2 = st.columns([3, 1])
with col1:
    user_query = st.text_input('Enter a movie description to search:')  # Input for movie description
with col2:
    number_of_results = st.slider('Select how many movies to display', 1, 50, 10)  # Slider to select the number of results

# Search button to trigger the search
search_button = st.button('Search 🔍')

# Execute search and display results upon button click
if search_button and user_query:
    similar_movies = search_similar_movies(user_query, top_n=number_of_results)
    st.write('Similar movies found:')
    # Display the results as an HTML table without the index
    st.markdown(similar_movies.to_html(index=False), unsafe_allow_html=True)

# Custom CSS for styling the results table displayed on the web app
st.markdown("""
<style>
table {
    white-space: nowrap;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}
thead tr th:first-child {
    position: sticky;
    left: 0;
    z-index: 100;
}
th {
    background-color: #4f8bf9;
    color: white;
    font-size: 16px;
}
td {
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)
