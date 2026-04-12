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


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 45)
    print("   TOP MUSIC RECOMMENDATIONS")
    print("=" * 45)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar = "#" * int(score * 20)
        print(f"\n#{rank}  {song['title']}  -  {song['artist']}")
        print(f"    Genre: {song['genre']:<12} Mood: {song['mood']}")
        print(f"    Score: {score:.2f}  {bar}")
        print(f"    Why:   {explanation}")

    print("\n" + "=" * 45)


if __name__ == "__main__":
    main()
