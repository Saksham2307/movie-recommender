import streamlit as st
import pickle
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# ── Load data ─────────────────────────────────────────────────
# ── Load data ─────────────────────────────────────────────────
import gdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pickle.load(open(os.path.join(BASE_DIR, 'movies.pkl'), 'rb'))

similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')
if not os.path.exists(similarity_path):
    gdown.download(
        "https://drive.google.com/uc?id=1NtIxeZ85uoWP34PZoS0lJwY6wA46pA8d",
        similarity_path,
        quiet=False
    )
similarity = pickle.load(open(similarity_path, 'rb'))

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# ── Global CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');

.stApp {
    background: #0a0a0f;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2rem 4rem 4rem 4rem !important;
    max-width: 1300px !important;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.hero-subtitle {
    font-size: 1rem;
    color: #6b7280;
    font-weight: 400;
    margin-bottom: 2.5rem;
    letter-spacing: 0.3px;
}

.hero-accent {
    color: #c084fc;
}

.stSelectbox > div > div {
    background: #13131a !important;
    border: 1px solid #2d2d3d !important;
    border-radius: 12px !important;
    color: #e5e7eb !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.2rem 0.5rem !important;
    transition: border-color 0.2s ease;
}
.stSelectbox > div > div:hover {
    border-color: #7c3aed !important;
}
.stSelectbox label {
    color: #9ca3af !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.55rem 1.2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    width: 100% !important;
    white-space: nowrap !important;
    margin-top: 0.3rem !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7280;
    margin: 2.5rem 0 1.2rem 0;
}

.movie-card {
    background: #13131a;
    border: 1px solid #1f1f2e;
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    cursor: default;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-6px) scale(1.03);
    border-color: #7c3aed;
    box-shadow: 0 12px 40px rgba(124, 58, 237, 0.3);
}
.movie-card img {
    width: 100%;
    height: 300px;
    display: block;
    object-fit: cover;
    object-position: center top;
    transition: transform 0.25s ease;
}
.movie-card:hover img {
    transform: scale(1.05);
}

.no-poster {
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #13131a;
    border: 1px solid #1f1f2e;
    border-radius: 14px;
}
.no-poster-inner {
    text-align: center;
    padding: 1rem;
}
.no-poster-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
    opacity: 0.4;
}
.no-poster-title {
    font-size: 0.85rem;
    font-weight: 500;
    color: #6b7280;
    line-height: 1.4;
}

.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2d2d3d 30%, #2d2d3d 70%, transparent);
    margin: 2rem 0;
}

.stSpinner > div {
    border-top-color: #a855f7 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ─────────────────────────────────────────────
st.markdown('<div style="padding-top: 2rem;"></div>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">Cine<span class="hero-accent">Match</span></p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Discover movies tailored to your taste</p>', unsafe_allow_html=True)
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Functions ─────────────────────────────────────────────────
def fetch_poster(movie_title):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['results'] and data['results'][0].get('poster_path'):
            return "https://image.tmdb.org/t/p/w500" + data['results'][0]['poster_path']
    except:
        pass
    return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:17]
    titles = [movies.iloc[i[0]].title for i in movies_list]

    with ThreadPoolExecutor(max_workers=16) as executor:
        posters = list(executor.map(fetch_poster, titles))

    filtered = [(t, p) for t, p in zip(titles, posters) if p is not None][:8]
    
    # pad to 8 if still not enough results
    while len(filtered) < 8:
        filtered.append(("No Result", None))

    titles_out, posters_out = zip(*filtered)
    return list(titles_out), list(posters_out)

# ── Controls ─────────────────────────────────────────────────
st.markdown('<div class="section-label">Choose a movie</div>', unsafe_allow_html=True)

col_select, col_btn = st.columns([5, 1])
with col_select:
    selected_movie = st.selectbox('', movies['title'].values, label_visibility='collapsed')
with col_btn:
    recommend_btn = st.button('✦ Recommend')

# ── Results ───────────────────────────────────────────────────
def render_card(name, poster):
    if poster:
        return f"""
        <div class="movie-card">
            <img src="{poster}" alt="{name}"/>
            <div class="movie-card-title">{name}</div>
        </div>
        """
    else:
        return f"""
        <div class="no-poster">
            <div class="no-poster-inner">
                <div class="no-poster-icon">🎬</div>
                <div class="no-poster-title">{name}</div>
            </div>
        </div>
        """

if recommend_btn:
    with st.spinner('Finding your next obsession...'):
        names, posters = recommend(selected_movie)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Recommended for you</div>', unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")
    for i in range(4):
        with cols[i]:
            st.markdown(render_card(names[i], posters[i]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols2 = st.columns(4, gap="medium")
    for i in range(4):
        with cols2[i]:
            st.markdown(render_card(names[i+4], posters[i+4]), unsafe_allow_html=True)