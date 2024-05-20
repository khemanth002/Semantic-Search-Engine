
MOVIE SEARCH APPLICATION README

OVERVIEW:
This project allows users to search for similar movies based on descriptions. It involves preparing a dataset from IMDb, embedding the textual data for semantic search, storing the data in Elasticsearch, and using a Streamlit application for the user interface.

PREREQUISITES:
- Python 3.8+
- Elasticsearch 7.x+
- Streamlit
- Pandas
- NLTK
- Sentence Transformers
- Kaggle API

SETUP INSTRUCTIONS:

1. Install Required Python Packages:
   Use pip to install the necessary Python packages.
   ```
   pip install streamlit pandas nltk sentence_transformers elasticsearch kaggle
   ```

2. Kaggle API Setup:
   - Ensure you have a Kaggle account. Visit https://www.kaggle.com/ to create one if necessary.
   - Go to the Account section of your Kaggle profile, scroll to the API section, and click "Create New API Token". This will download a kaggle.json file.
   - Place the kaggle.json file in your home directory under ~/.kaggle/kaggle.json (Windows: C:\Users\<Username>\.kaggle\kaggle.json).

3. Elasticsearch Setup:
   Ensure Elasticsearch is installed and running on your system. Refer to the official Elasticsearch documentation for installation instructions.

EXECUTION INSTRUCTIONS:

1. Prepare the Data:
   - Navigate to the directory containing the project files.
   - Run the Create_Dataset.py script to download and extract the IMDb dataset.
     ```
     python Create_Dataset.py
     ```

2. Clean the Data:
   - Run the Clean_Data.py script to process and clean the dataset.
     ```
     python Clean_Data.py
     ```

3. Embed and Store Data:
   - Run the embed_and_store_data.py script to generate embeddings for the movies and store them in Elasticsearch.
     ```
     python embed_and_store_data.py
     ```

4. Run the Streamlit Application:
   - Start the Streamlit web application using the search_app.py script.
     ```
     streamlit run search_app.py
     ```
   - Visit the local URL provided by Streamlit in your web browser to interact with the application.

TROUBLESHOOTING:
- Ensure all Python dependencies are correctly installed.
- Verify that Elasticsearch is running and accessible.
- Check that the kaggle.json file is correctly placed for Kaggle API access.

