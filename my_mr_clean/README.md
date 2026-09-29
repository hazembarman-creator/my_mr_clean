# Welcome to My Mr Clean
***

## Task
Build a simple search engine pipeline for EncyclEarthpedia.
The challenge is to retrieve, clean, and analyze Wikipedia article data
to find the most relevant words that describe an article — without using
the forbidden `wikipedia` Python package.

## Description
We solved the problem in 6 steps:
1. **Get the data** — Call Wikipedia's raw API using `requests` with a proper User-Agent header
2. **Clean the data** — Strip all wikitext markup, templates, URLs, HTML tags using `re`
3. **Tokenize** — Split the clean text into individual words using custom splitter characters
4. **Lowercase** — Normalize all tokens to lowercase
5. **Frequency model** — Count word occurrences using `Counter`
6. **Filter stop words** — Remove common words (the, a, of...) to keep only meaningful tokens
7. **Visualize** — Plot histograms of the most frequent words before and after filtering

## Installation
```bash
pip install requests matplotlib jupytext
```

## Usage
Open and run the notebook from top to bottom:
```bash
jupyter notebook my_mr_clean.ipynb
```

Or run the Python script directly:
```bash
python3 my_mr_clean.py
```

The notebook will:
- Fetch the Ozone Layer article from Wikipedia
- Clean and tokenize the text
- Display the top 20 most frequent words (unfiltered)
- Display the top 25 most frequent words (after stop word removal)

### The Core Team
Hazem Barman & Leila Cheikhe

<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>
