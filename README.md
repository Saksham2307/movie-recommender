# 🎬 CineMatch — Movie Recommendation System

A content-based movie recommendation web app built with Python and Streamlit. Pick any movie and instantly get 8 visually rich recommendations with posters fetched live from TMDB.

---

## 🚀 Live Demo

> > [🚀 Open Live App](https://movie-recommender-v8svfvggmofu43fqirz927.streamlit.app)

---

## 📸 Screenshot

> *(Add a screenshot of the app here)*

---

## 🧠 How It Works

1. The TMDB 5000 Movies dataset is preprocessed — genres, keywords, cast, crew, and overview are combined into a single "tags" string for each movie.
2. **CountVectorizer** converts these tags into feature vectors.
3. **Cosine Similarity** is computed between all movie vectors and stored as a matrix.
4. When a user selects a movie, the app finds the most similar movies using this matrix.
5. Posters are fetched in parallel from the **TMDB API** using `ThreadPoolExecutor`.

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3 |
| ML | scikit-learn (CountVectorizer, Cosine Similarity) |
| Frontend | Streamlit |
| Poster API | TMDB API |
| Dataset | TMDB 5000 Movies (Kaggle) |

---

## 📁 Project Structure

```
movie-recommender/
├── app.py                  # Streamlit frontend
├── exploration.ipynb       # Data preprocessing & model building
├── movies.pkl              # Preprocessed movie data (generated locally)
├── similarity.pkl          # Cosine similarity matrix (generated locally)
└── README.md
```

> **Note:** `movies.pkl`, `similarity.pkl`, and the CSV dataset files are not included in this repo due to size. Run `exploration.ipynb` to generate them locally.

---

## ⚙️ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Saksham2307/movie-recommender.git
cd movie-recommender
```

**2. Install dependencies**
```bash
pip install streamlit scikit-learn pandas requests
```

**3. Download the dataset**

Download [TMDB 5000 Movies](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle and place both CSV files in the project folder.

**4. Generate the pickle files**

Run `exploration.ipynb` top to bottom. This will create `movies.pkl` and `similarity.pkl`.

**5. Add your TMDB API key**

Get a free API key from [themoviedb.org](https://www.themoviedb.org/settings/api) and replace the key in `app.py`.

**6. Run the app**
```bash
streamlit run app.py
```

---

## 👤 Author

**Saksham Miglani**  
MCA Student | Aspiring SDE / ML Engineer  
[GitHub](https://github.com/Saksham2307) • [LinkedIn](https://www.linkedin.com/in/saksham-miglani-1936b7393/)
