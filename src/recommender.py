from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons = []

    # Genre match (binary)
    genre_match = 1 if song["genre"] == user_prefs["genre"] else 0
    if genre_match:
        reasons.append("matches your favorite genre")

    # Mood match (binary)
    mood_match = 1 if song["mood"] == user_prefs["mood"] else 0
    if mood_match:
        reasons.append("matches your preferred mood")

    # Energy score (continuous)
    energy_score = 1 - abs(user_prefs["energy"] - song["energy"])
    reasons.append(f"energy is {song['energy']:.2f} (target {user_prefs['energy']:.2f})")

    # Acousticness score (continuous)
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_score = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]

    score = (genre_match  * 0.25 +
             mood_match   * 0.35 +
             energy_score * 0.30 +
             acoustic_score * 0.10)

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return [
        (song, score, ", ".join(reasons))
        for song, score, reasons in ranked[:k]
    ]
