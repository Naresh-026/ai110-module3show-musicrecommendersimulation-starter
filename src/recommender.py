import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
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
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by score for the given user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "acousticness": song.acousticness,
                "danceability": song.danceability,
                "tempo_bpm": song.tempo_bpm,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "acousticness": song.acousticness,
            "danceability": song.danceability,
            "tempo_bpm": song.tempo_bpm,
        }
        _, reasons = score_song(user_prefs, song_dict)
        if reasons:
            return "; ".join(reasons)
        return "Matched based on overall profile similarity."


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of song dictionaries with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns (total_score, list_of_reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 points — strongest signal for taste alignment
    if user_prefs.get("genre") and song.get("genre", "").lower() == user_prefs["genre"].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0 point — emotional vibe alignment
    if user_prefs.get("mood") and song.get("mood", "").lower() == user_prefs["mood"].lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy closeness: up to +1.5 points — rewards songs with similar intensity
    if user_prefs.get("energy") is not None and "energy" in song:
        energy_gap = abs(float(song["energy"]) - float(user_prefs["energy"]))
        energy_score = round(1.5 * (1.0 - energy_gap), 2)
        score += energy_score
        reasons.append(f"energy closeness (+{energy_score:.2f})")

    # Acoustic bonus: up to +0.5 points if user prefers acoustic music
    if user_prefs.get("likes_acoustic") and "acousticness" in song:
        acoustic_score = round(float(song["acousticness"]) * 0.5, 2)
        score += acoustic_score
        reasons.append(f"acoustic quality (+{acoustic_score:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top k as (song_dict, score, explanation) tuples sorted highest first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
