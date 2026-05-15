import streamlit as st
import pickle
import pandas as pd
import requests
import random

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Shukla's Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-image: url("https://imgs.search.brave.com/ejtM1LPRcS4UHQhLAcIztJamhwkI_uyMJUsulT_WP7o/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJhY2Nlc3Mu/Y29tL2Z1bGwvNDE3/ODAzNC5qcGc");
    background-size: cover;
    background-position: top center;
    background-attachment: fixed;
}

/* Dark Overlay */
.main {
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(6px);
    border-radius: 20px;
    padding: 20px;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #E50914;
    letter-spacing: 2px;
    margin-top: -10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #e0e0e0;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Cards */
.movie-card {
    background: linear-gradient(145deg, #ff416c, #ff4b2b);
    padding: 15px;
    border-radius: 20px;
    text-align: center;
    color: white;
    transition: 0.4s;
    box-shadow: 0px 5px 25px rgba(255,75,43,0.5);
    margin-bottom: 20px;
}

.movie-card:hover {
    transform: scale(1.05);
    background: linear-gradient(145deg, #7F00FF, #E100FF);
}

/* Buttons */
.stButton > button {
    width: 100%;
    background-color: #E50914;
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 22px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #ff1f1f;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111111;
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
    font-size: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# =========================================================
# TMDB API
# =========================================================
API_KEY = "fcf9f73df6496d43694861d5e80258c2"

# =========================================================
# FETCH POSTER
# =========================================================
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url)

    data = data.json()

    poster_path = data.get('poster_path')

    if poster_path:

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path

    else:

        return "https://via.placeholder.com/500x750?text=No+Poster"

# =========================================================
# FETCH MOVIE DETAILS
# =========================================================
def fetch_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url)

    data = data.json()

    title = data.get('title', 'Unknown')

    rating = data.get('vote_average', 'N/A')

    overview = data.get('overview', 'No overview available.')

    release_date = data.get('release_date', 'Unknown')

    return title, rating, overview, release_date

# =========================================================
# RECOMMEND FUNCTION
# =========================================================
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_overviews = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

        title, rating, overview, release_date = fetch_details(movie_id)

        recommended_ratings.append(rating)

        recommended_overviews.append(overview)

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_overviews
    )

# =========================================================
# HEADER
# =========================================================
st.markdown(
    "<div class='main-title'>🎬 Shukla's Movie Recommender</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Discover movies matching your vibe ✨</div>",
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙️ Explore")

mood = st.sidebar.selectbox(
    "🎭 Choose Your Mood",
    [
        "All",
        "Action",
        "Comedy",
        "Sci-Fi",
        "Romance",
        "Thriller",
        "Adventure",
        "Fantasy",
        "Drama"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write("🔥 AI Powered Recommendation Engine")
st.sidebar.write("🎬 Netflix Inspired UI")
st.sidebar.write("🚀 Machine Learning + Streamlit")
st.sidebar.write("✨ TMDB API Integrated")

# =========================================================
# MOOD BASED MOVIES
# =========================================================
if mood != "All":

    st.subheader(f"🎭 Popular {mood} Movies")

    mood_movies = movies[
        movies['tags'].apply(
            lambda x: mood.lower() in str(x).lower()
        )
    ]

    mood_titles = mood_movies['title'].head(10).values

    cols = st.columns(5)

    emojis = ["🎬", "🍿", "🔥", "✨", "🚀"]

    for idx, title in enumerate(mood_titles):

        with cols[idx % 5]:

            st.markdown(
                f"""
                <div class='movie-card'>
                    {emojis[idx % 5]}
                    <br><br>
                    {title}
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# MOVIE SELECTOR
# =========================================================
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🎥 Select Your Favorite Movie",
    movie_list
)

# =========================================================
# RANDOM QUOTE
# =========================================================
quotes = [
    "Cinema is a mirror painted with dreams ✨",
    "Every movie is a journey through emotions 🎭",
    "Stories become immortal on screen 🎬",
    "AI meets cinema in this universe 🚀"
]

st.info(random.choice(quotes))

# =========================================================
# RECOMMEND BUTTON
# =========================================================
if st.button("🚀 Recommend Movies"):

    names, posters, ratings, overviews = recommend(selected_movie)

    st.subheader("✨ Recommended For You")

    cols = st.columns(5)

    for idx in range(5):

        with cols[idx]:

            st.image(posters[idx])

            st.markdown(
                f"""
                <div class='movie-card'>
                    <h3>{names[idx]}</h3>
                    ⭐ Rating: {ratings[idx]}
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("📖 Overview"):

                st.write(overviews[idx])

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class='footer'>
        Made with ❤️ using Python, Machine Learning, TMDB API & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)