"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Prints formatted top-k recommendations for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'='*55}")
    print(f"  Profile: {label}")
    print(f"  Preferences: {user_prefs}")
    print(f"{'='*55}")
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score: {score:.2f}  |  {song['genre']} / {song['mood']}")
        print(f"     Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Profile 1: High-Energy Pop Fan ---
    print_recommendations(
        "High-Energy Pop Fan",
        {"genre": "pop", "mood": "happy", "energy": 0.85},
        songs,
    )

    # --- Profile 2: Chill Lofi Listener ---
    print_recommendations(
        "Chill Lofi Listener",
        {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True},
        songs,
    )

    # --- Profile 3: Deep Intense Rock Fan ---
    print_recommendations(
        "Deep Intense Rock Fan",
        {"genre": "rock", "mood": "intense", "energy": 0.92},
        songs,
    )


if __name__ == "__main__":
    main()
