"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import shutil
import textwrap

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs

_BAR_WIDTH   = 10   # max score-bar characters
_SCORE_WIDTH = 5    # "0.92" fixed width
# Fixed overhead per data row: "  " rank(3) " " title " " artist "  " score(5) "  " bar(10)
_ROW_FIXED   = 2 + 3 + 1 + 1 + 2 + _SCORE_WIDTH + 2 + _BAR_WIDTH   # = 26


def _table_width() -> int:
    """Detect terminal width and clamp to a safe range."""
    cols = shutil.get_terminal_size(fallback=(80, 24)).columns
    return max(56, min(72, cols - 2))


def _hline(w: int, char: str = "-") -> str:
    return "+" + char * (w - 2) + "+"


def _cell(text: str, w: int) -> str:
    """Left-justify text inside a single bordered row of width w."""
    inner = w - 4
    return "| " + str(text)[:inner].ljust(inner) + " |"


def print_results(label: str, description: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    w     = _table_width()
    inner = w - 4

    # Scale title/artist columns to whatever space is left after fixed overhead
    flexible = inner - _ROW_FIXED
    title_w  = max(12, flexible * 22 // 38)   # ~58 % of flexible space
    artist_w = max(10, flexible - title_w)     # remainder

    pref_str = "  ".join(f"{k}={repr(v)}" for k, v in user_prefs.items())

    # ── header block ──────────────────────────────────────────────
    print()
    print(_hline(w, "="))
    print(_cell(f"  {label}", w))
    print(_cell(f"  Prefs  : {pref_str}", w))
    print(_cell(f"  Note   : {description}", w))
    print(_hline(w, "="))

    # Indent shared by every data row: "  " + rank(3) + " " = 6 chars
    indent = " " * 6

    # ── column headers (two rows: names + sub-labels) ─────────────
    print(_cell(
        f"  {'#':<3} {'Title':<{title_w}} {'Artist':<{artist_w}}  {'Score':>5}  Bar", w
    ))
    print(_cell(
        f"{indent}{'(Genre)':<{title_w}} {'(Mood)':<{artist_w}}", w
    ))
    print(_hline(w))

    # ── one block per recommendation ──────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar    = "#" * max(0, int(score * _BAR_WIDTH))
        title  = song["title"][:title_w]
        artist = song["artist"][:artist_w]
        genre  = song["genre"][:title_w]
        mood   = song["mood"][:artist_w]

        # Row 1: rank  title  artist  score  bar
        print(_cell(
            f"  {rank:<3} {title:<{title_w}} {artist:<{artist_w}}  {score:>5.2f}  {bar:<{_BAR_WIDTH}}", w
        ))
        # Row 2: genre aligned under title, mood aligned under artist
        print(_cell(f"{indent}{genre:<{title_w}} {mood:<{artist_w}}", w))

        # Row 3+: reasons, wrapped to fit inside the box
        reasons_prefix = f"{indent}Reasons: "
        wrap_width = inner - len(reasons_prefix)
        wrapped = textwrap.wrap(explanation, width=max(20, wrap_width))
        for i, chunk in enumerate(wrapped):
            prefix = reasons_prefix if i == 0 else " " * len(reasons_prefix)
            print(_cell(f"{prefix}{chunk}", w))

        print(_hline(w))

    print()


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
