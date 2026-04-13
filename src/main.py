"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


def print_results(label: str, description: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 55)
    print(f"  {label}")
    print(f"  Prefs: {user_prefs}")
    print(f"  Why adversarial: {description}")
    print("=" * 55)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar = "#" * max(0, int(score * 20))
        print(f"\n#{rank}  {song['title']}  -  {song['artist']}")
        print(f"    Genre: {song['genre']:<12} Mood: {song['mood']}")
        print(f"    Score: {score:.2f}  {bar}")
        print(f"    Why:   {explanation}")

    print("\n" + "=" * 55)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Starter example profile ---
    print_results(
        label="STARTER PROFILE",
        description="Baseline happy pop fan",
        user_prefs={"genre": "pop", "mood": "happy", "energy": 0.8},
        songs=songs,
    )

    # --- Adversarial Profile 1: The Contradiction ---
    # mood: "sad" but energy: 0.95 (no sad song has high energy).
    # The only sad song is "3AM Thoughts" (energy 0.38), so it scores poorly
    # on energy. High-energy songs like metal may outscore it despite wrong mood.
    print_results(
        label="ADVERSARIAL #1 — The Contradiction",
        description="sad mood + very high energy: no song satisfies both, watch which weight wins",
        user_prefs={"genre": "r&b", "mood": "sad", "energy": 0.95},
        songs=songs,
    )

    # --- Adversarial Profile 2: The Ghost Genre ---
    # genre: "k-pop" does not exist in the dataset.
    # genre_match is always 0; the recommender never warns the user.
    # Results are driven entirely by mood + energy, regardless of genre.
    print_results(
        label="ADVERSARIAL #2 — The Ghost Genre",
        description="genre 'k-pop' doesn't exist in data: genre_match silently stays 0 for every song",
        user_prefs={"genre": "k-pop", "mood": "happy", "energy": 0.7},
        songs=songs,
    )

    # --- Adversarial Profile 3: The Acoustic-Electronic Paradox ---
    # genre: "electronic" + likes_acoustic: True conflict directly.
    # The only electronic song (Pulse Wave) has acousticness 0.03, so it scores
    # near-zero on the acoustic component. Highly acoustic classical/folk songs
    # may rank above it despite being a completely different genre.
    print_results(
        label="ADVERSARIAL #3 — The Acoustic-Electronic Paradox",
        description="electronic genre + likes_acoustic=True: the only electronic song is nearly non-acoustic",
        user_prefs={"genre": "electronic", "mood": "uplifting", "energy": 0.88, "likes_acoustic": True},
        songs=songs,
    )


if __name__ == "__main__":
    main()
