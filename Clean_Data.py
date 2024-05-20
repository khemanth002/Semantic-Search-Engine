# Import necessary libraries
import pandas as pd
import re
from nltk.stem.porter import PorterStemmer

# Load movie data from a CSV file into a DataFrame
hk_movies = pd.read_csv("imdb_top_1000.csv")
print(hk_movies.info())  # Display the DataFrame's information including data types and non-null counts
print(hk_movies.head())  # Print the first 5 rows of the DataFrame to get an overview of the data

# Remove rows where the movie overview is missing, as the overview is essential for semantic analysis
hk_movies.dropna(subset=['Overview'], inplace=True)

# Fill missing values in 'Genre' and 'Director' columns with the string 'Unknown'
hk_movies['Genre'] = hk_movies['Genre'].fillna('Unknown')
hk_movies['Director'] = hk_movies['Director'].fillna('Unknown')

# Define a function to clean text data
def hk_clean_text(hk_text):
    # Replace multiple spaces with a single space
    hk_text = re.sub(r'\s+', ' ', hk_text)
    # Remove all non-alphanumeric characters
    hk_text = re.sub(r"[^a-zA-Z0-9]", " ", hk_text)
    # Convert all characters to lowercase
    hk_text = hk_text.lower()
    # Apply stemming to reduce words to their root form
    hk_stemmer = PorterStemmer()
    hk_text = ' '.join([hk_stemmer.stem(hk_word) for hk_word in hk_text.split()])
    return hk_text

# Clean the 'Overview' column text using the defined function
hk_movies['hk_clean_overview'] = hk_movies['Overview'].apply(hk_clean_text)

# Remove duplicate movie entries based on the 'Series_Title' column
hk_movies.drop_duplicates(subset=['Series_Title'], inplace=True)

# Clean 'Released_Year' and 'Genre' columns using the text cleaning function
hk_movies['Released_Year'] = hk_movies['Released_Year'].apply(hk_clean_text)
hk_movies['Genre'] = hk_movies['Genre'].apply(hk_clean_text)

# Combine cleaned text columns into a single column for further text embedding or analysis
hk_movies['hk_embedded_text'] = (hk_movies['hk_clean_overview'] + ' ' +
                                 hk_movies['Director'] + ' ' +
                                 hk_movies['Genre'] + ' ' +
                                 hk_movies['Released_Year'])

# Save the cleaned and processed DataFrame to a new CSV file
hk_movies.to_csv('hk_cleaned_imdb_top_1000.csv', index=False)

# Print the first 10 rows of the cleaned 'Series_Title' and 'Overview' to verify the cleaning process
print(hk_movies[["Series_Title", "Overview"]].head(10))
