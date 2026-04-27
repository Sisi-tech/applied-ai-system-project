from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import csv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

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

    def score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += 1.0
            reasons.append("Genre matches user favorite")

        if song.mood == user.favorite_mood:
            score += 1.5
            reasons.append("Mood matches user preference")

        energy_difference = abs(song.energy - user.target_energy)
        energy_score = max(0.0, 1.0 - energy_difference)
        energy_bonus = energy_score * 2.0
        score += energy_bonus
        reasons.append(f"Energy is close to target (+{energy_bonus:.2f})")

        acoustic_match = song.acousticness > 0.5
        if acoustic_match == user.likes_acoustic:
            score += 1.0
            reasons.append("Acoustic preference matches")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = [
            (song, *self.score_song(user, song))
            for song in self.songs
        ]
        scored_songs.sort(key=lambda item: item[1], reverse=True)
        return [song for song, score, reasons in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self.score_song(user, song)
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """Load songs from a CSV file for the CLI recommender."""
    songs: List[Dict[str, Any]] = []
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['id'] = int(row['id'])
                row['energy'] = float(row['energy'])
                row['tempo_bpm'] = float(row['tempo_bpm'])
                row['valence'] = float(row['valence'])
                row['danceability'] = float(row['danceability'])
                row['acousticness'] = float(row['acousticness'])
                songs.append(row)
    except FileNotFoundError:
        logger.error("Song data file not found: %s", csv_path)
        raise
    except ValueError as exc:
        logger.error("Bad song data in %s: %s", csv_path, exc)
        raise
    return songs


def score_song(user_prefs: Dict[str, Any], song: Dict[str, Any]) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return score plus reasons."""
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += 1.0
        reasons.append("Genre matches user favorite")

    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += 1.5
        reasons.append("Mood matches user preference")

    energy_difference = abs(song.get("energy", 0.0) - user_prefs.get("target_energy", 0.0))
    energy_score = max(0.0, 1.0 - energy_difference)
    energy_bonus = energy_score * 2.0
    score += energy_bonus
    reasons.append(f"Energy is close to target (+{energy_bonus:.2f})")

    acoustic_match = song.get("acousticness", 0.0) > 0.5
    if acoustic_match == bool(user_prefs.get("likes_acoustic", False)):
        score += 1.0
        reasons.append("Acoustic preference matches")

    return score, reasons


def recommend_songs(user_prefs: Dict[str, Any], songs: List[Dict[str, Any]], k: int = 5) -> List[Tuple[Dict[str, Any], float, str]]:
    """Score all songs and return the top k recommendations."""
    scored_songs = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]


def validate_recommendations(user_prefs: Dict[str, Any], recommendations: List[Tuple[Dict[str, Any], float, str]]) -> Dict[str, Any]:
    """Check whether recommendations meet simple reliability heuristics."""
    if not recommendations:
        logger.warning("No recommendations to validate.")
        return {
            "top_genre_match": False,
            "top_mood_match": False,
            "average_score": 0.0,
            "issues": ["No recommendations computed."],
        }

    top_song, _, _ = recommendations[0]
    top_genre_match = top_song.get("genre") == user_prefs.get("favorite_genre")
    top_mood_match = top_song.get("mood") == user_prefs.get("favorite_mood")
    average_score = sum(score for _, score, _ in recommendations) / len(recommendations)

    issues: List[str] = []
    if not (top_genre_match or top_mood_match):
        issues.append("Top recommendation does not match the user's genre or mood.")
    if average_score < 2.0:
        issues.append("Average recommendation score is low; the model may need tuning.")

    return {
        "top_genre_match": top_genre_match,
        "top_mood_match": top_mood_match,
        "average_score": average_score,
        "issues": issues,
    }
