import requests
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

# ── 1. GET CONTENT ──────────────────────────────────────────────
def get_content(article_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": article_name,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "formatversion": "2",
        "format": "json"
    }
    headers = {
        "User-Agent": "EncyclEarthpedia/1.0 (student project; leila@example.com)"
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

data = get_content("Ozone_layer")
print("✅ Step 1 done: got data from Wikipedia")

# ── 2. MERGE CONTENTS ────────────────────────────────────────────
def merge_contents(data):
    pages = data.get("query", {}).get("pages", [])
    raw_text = ""
    for page in pages:
        for rev in page.get("revisions", []):
            raw_text += rev.get("slots", {}).get("main", {}).get("content", "")
    for _ in range(5):
        raw_text = re.sub(r'\{\{[^{}]*\}\}', ' ', raw_text)
    raw_text = re.sub(r'\[\[(?:File|Image):[^\]]*\]\]', ' ', raw_text, flags=re.IGNORECASE)
    raw_text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', raw_text)
    raw_text = re.sub(r'<ref[^>]*>.*?</ref>', ' ', raw_text, flags=re.DOTALL)
    raw_text = re.sub(r'<ref[^/]*/>', ' ', raw_text)
    raw_text = re.sub(r'<[^>]+>', ' ', raw_text)
    raw_text = re.sub(r'https?://\S+', ' ', raw_text)
    raw_text = re.sub(r'&\w+;', ' ', raw_text)
    raw_text = re.sub(r'=+[^=]+=+', ' ', raw_text)
    raw_text = re.sub(r"[^a-zA-Z0-9\s\-']", ' ', raw_text)
    raw_text = re.sub(r'\s+', ' ', raw_text).strip()
    return [raw_text]

merge_content = merge_contents(data)
print("✅ Step 2 done:", merge_content[0][:100])

# ── 3. TOKENIZE ──────────────────────────────────────────────────
splitters = [" ", "\n", "\t", "-", "_", "/"]

def tokenize(content):
    pattern = "|".join(re.escape(s) for s in splitters)
    tokens = []
    for text in content:
        parts = re.split(pattern, text)
        tokens.extend([p for p in parts if p])
    return tokens

collection = tokenize(merge_content)
print(f"✅ Step 3 done: {len(collection)} tokens")

# ── 4. LOWERCASE ─────────────────────────────────────────────────
def lower_collection(collection):
    collection[:] = [w.lower() for w in collection]
    return collection

lower_collection(collection)
print("✅ Step 4 done: all lowercase")

# ── 5. COUNT FREQUENCY ───────────────────────────────────────────
def count_frequency(collection):
    clean = [w for w in collection if w and not w.isdigit()]
    return Counter(clean)

def print_most_frequent(frequencies, n):
    print(f"\n{'Word':<25} {'Count':>6}")
    print("-" * 33)
    for word, count in frequencies.most_common(n):
        print(f"{word:<25} {count:>6}")

frequencies = count_frequency(collection)
print("✅ Step 5 done: frequency model built")
print_most_frequent(frequencies, 10)

# ── 6. PLOT TOP 20 unfiltered ────────────────────────────────────
def plot_most_frequent(frequencies, n, title, filename):
    words, counts = zip(*frequencies.most_common(n))
    plt.figure(figsize=(14, 5))
    plt.bar(words, counts, color="steelblue", edgecolor="white")
    plt.title(title)
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"✅ Plot saved → {filename}")

plot_most_frequent(frequencies, 20, "Top 20 Most Frequent Words (unfiltered)", "plot_unfiltered.png")

# ── 7. STOP WORDS ────────────────────────────────────────────────
stop_words = [
    "the", "a", "an", "of", "to", "in", "and", "is", "it", "its",
    "was", "are", "be", "by", "as", "at", "or", "for", "on", "from",
    "that", "this", "with", "which", "not", "has", "have", "been",
    "but", "also", "can", "more", "than", "into", "their", "they",
    "about", "were", "had", "he", "she", "we", "you", "i", "s",
    "such", "some", "other", "no", "most", "will", "may", "up",
    "so", "while", "between", "through", "during", "under", "over",
    "however", "if", "when", "after", "before", "although", "since",
    "all", "any", "both", "each", "few", "many", "new", "these",
    "those", "then", "there", "where", "what", "how", "do", "did",
    "does", "use", "used", "using", "would", "could", "should",
    "being", "due", "only", "very", "much", "well", "make", "made",
    "one", "two", "three", "first", "second", "per", "km", "nm", "cm"
]

def remove_stop_words(words, stop_words):
    stop_set = set(stop_words)
    return [w for w in words if w not in stop_set and len(w) > 1]

filtered_collection = remove_stop_words(collection, stop_words)
print(f"\n✅ Step 7 done: {len(filtered_collection)} tokens after filtering")

# ── 8. PLOT TOP 25 filtered ──────────────────────────────────────
filtered_frequencies = count_frequency(filtered_collection)
print_most_frequent(filtered_frequencies, 10)
plot_most_frequent(filtered_frequencies, 25, "Top 25 Most Frequent Words (filtered)", "plot_filtered.png")

print("\n🎉 ALL DONE!")
