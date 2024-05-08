# Also partly imported from zoom tutorial and a youtube video
# Youtube link: https://www.youtube.com/watch?v=UYJDKSah-Ww
import pandas as pd
from random import choice, sample, shuffle, randint

# Load Marvel data
df = pd.read_csv('movies.csv', dtype={'Title': str})
# print(df['Title'].head())
df['Production Budget'] = df['Production \nBudget'].replace('[\$,]', '', regex=True).astype(int)
df['Worldwide Box Office'] = df['Worldwide \nBox Office'].replace('[\$,]', '', regex=True)
df['Worldwide Box Office'] = pd.to_numeric(df['Worldwide Box Office'], errors='coerce').fillna(0).astype('int64')
df['Release Date'] = pd.to_datetime(df['Release \nDate'], errors='coerce')

# Chronological order of Marvel movies
chronological_titles = [
    "Captain America: The First Avenger", "Captain Marvel", "Iron Man", "Iron Man 2",
    "The Incredible Hulk", "Thor", "The Avengers", "Thor: The Dark World",
    "Iron Man 3", "Captain America: The Winter Soldier", "Guardians of the Galaxy",
    "Guardians of the Galaxy Vol. 2", "Avengers: Age of Ultron", "Ant-Man",
    "Captain America: Civil War", "Black Widow", "Spider-Man: Homecoming", "Black Panther",
    "Doctor Strange", "Thor: Ragnarok", "Ant-Man and the Wasp", "Avengers: Infinity War",
    "Avengers: Endgame", "Spider-Man: Far From Home", "Shang-Chi and the Legend of the Ten Rings",
    "Eternals", "Spider-Man: No Way Home", "Doctor Strange in the Multiverse of Madness",
    "Thor: Love and Thunder", "Black Panther: Wakanda Forever", "Ant-Man and the Wasp: Quantumania",
    "Guardians of the Galaxy Vol. 3", "The Marvels"
]


def get_movie_comparison():
    movies = sample(df.index.tolist(), 2)
    movie1, movie2 = df.iloc[movies[0]], df.iloc[movies[1]]
    prompt = f"Which made more money globally? (A) {movie1['Title']} or (B) {movie2['Title']}?"
    # Store both the choice and the full movie name in the answer tuple
    correct_answer = ('A', movie1['Title']) if movie1['Worldwide Box Office'] > movie2['Worldwide Box Office'] else ('B', movie2['Title'])
    return prompt, correct_answer


def get_chronological_order_challenge():
    selected_movies = sample(chronological_titles, 5)
    shuffled_movies = selected_movies[:]
    shuffle(shuffled_movies)
    prompt = f"Order these movies chronologically by events: {' '.join(['A', 'B', 'C', 'D', 'E'])}\n" + \
             "\n".join(f"{chr(65 + i)}: {movie}" for i, movie in enumerate(shuffled_movies))
    correct_order = "\n".join(selected_movies)  # Correct order for feedback
    return prompt, ('order', correct_order)  # Return as tuple with 'order' tag


def higher_or_lower():
    movie = df.sample(1).iloc[0]
    variation = randint(-50000000, 50000000)
    while variation == 0:  # Ensure the variation is not zero
        variation = randint(-50000000, 50000000)
    budget_guess = movie['Production Budget'] + variation
    formatted_budget = f"{budget_guess:,}"  # Format with commas
    prompt = f"Is the production budget of {movie['Title']} higher or lower than ${formatted_budget}? (Answer 'higher' or 'lower')"
    comparison = 'higher' if movie['Production Budget'] > budget_guess else 'lower'
    return prompt, (comparison, f"${movie['Production Budget']:,}")  # Return as tuple with comparison and formatted actual budget


def get_response(user_input: str, user_response=None):
    if user_input == '!compare':
        prompt, correct_answer = get_movie_comparison()
        return prompt, correct_answer
    elif user_input == '!order':
        prompt, correct_order = get_chronological_order_challenge()
        return prompt, correct_order
    elif user_input.startswith('!higherlower'):
        prompt, comparison = higher_or_lower()
        return prompt, comparison
    elif user_input == '!help':
        return " Welcome to MarvelQuiz! A game to compare budget, revenue, and the order of Marvel Movies! \n \
        There are three commands to choose from currently: \n \
        !compare - Guess which movie made more money (Worldwide box office)\n \
        !order - Order movies by events chronologically (NOT in order of release date) \n \
        !higherlower - Guess if the given budget is higher or lower to the true value \n \
        DISCLAIMER: Currently we are partway through Phase Five so only movies are included (Next movie is July 2024)", None
    elif user_input[0] == '!':
        return "Unknown command. Try !help for a list of commands.", None
    return
