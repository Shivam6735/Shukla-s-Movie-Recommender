import streamlit as st
import pickle
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Netflix Style Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background-image: url("https://imgs.search.brave.com/ejtM1LPRcS4UHQhLAcIztJamhwkI_uyMJUsulT_WP7o/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJhY2Nlc3Mu/Y29tL2Z1bGwvNDE3/ODAzNC5qcGc");
    background-size: cover;
    background-attachment: fixed;
}

/* Dark overlay */
.main {
    background: rgba(0,0,0,0.85);
    border-radius: 20px;
    padding: 20px;
}

/* Title */
h1 {
    color: #E50914;
    text-align: center;
    font-size: 60px !important;
    font-weight: bold;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #d3d3d3;
    font-size: 22px;
    margin-bottom: 30px;
}

/* Movie Cards */
.movie-card {
    background: linear-gradient(145deg, #ff416c, #ff4b2b);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 20px;
    transition: 0.4s;
    box-shadow: 0px 4px 20px rgba(255,75,43,0.5);
}

.movie-card:hover {
    transform: scale(1.08);
    background: linear-gradient(145deg, #7F00FF, #E100FF);
}

/* Buttons */
.stButton>button {
    width: 100%;
    background-color: #E50914;
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 22px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
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

# =========================
# LOAD DATA
# =========================
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(
            movies.iloc[i[0]].title
        )

    return recommended_movies

# =========================
# HEADER
# =========================
st.markdown(
    "<h1>🎬 Netflix Style Movie Recommender</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Discover movies matching your vibe ✨</div>",
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
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
st.sidebar.write("🎬 Netflix Style UI")
st.sidebar.write("💡 Built using Machine Learning")
st.sidebar.write("🚀 Streamlit Web App")

# =========================
# MOOD SUGGESTIONS
# =========================
if mood != "All":

    st.subheader(f"🎭 Popular {mood} Movies")

    mood_movies = movies[
        movies['tags'].apply(
            lambda x: mood.lower() in str(x).lower()
        )
    ]

    mood_titles = mood_movies['title'].head(10).values

    cols = st.columns(5)

    for idx, title in enumerate(mood_titles):

        with cols[idx % 5]:

            emojis = ["🎬", "🍿", "🔥", "✨", "🚀"]

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

# =========================
# MOVIE SELECTOR
# =========================
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🎥 Select Your Favorite Movie",
    movie_list
)

# =========================
# RECOMMEND BUTTON
# =========================
if st.button("🚀 Recommend Movies"):

    recommendations = recommend(selected_movie)

    st.subheader("✨ Recommended For You")

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    emojis = ["🎬", "🍿", "🔥", "✨", "🚀"]

    for idx in range(5):

        with cols[idx]:

            st.markdown(
                f"""
                <div class='movie-card'>
                    {emojis[idx]}
                    <br><br>
                    {recommendations[idx]}
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# FOOTER
# =========================
st.markdown(
    """
    <div class='footer'>
        Made with ❤️ using Python, Machine Learning & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

import requests

API_KEY = "fcf9f73df6496d43694861d5e80258c2"

url = f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}"

data = requests.get(url).json()

print(data['title'])