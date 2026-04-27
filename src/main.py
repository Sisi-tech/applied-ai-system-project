"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs

Use this prompt for inline Copilot analysis on the top-ranked song:

    I want to understand why `Sunrise City` ranked first for the
    `High-Energy Pop` profile. In `src/recommender.py`, the scoring logic gives:
    - +2.0 for genre match,
    - +1.5 for mood match,
    - an energy closeness bonus up to 1.0,
    - +1.0 if acoustic preference matches.

    Given the user profile:
    {
      "favorite_genre": "pop",
      "favorite_mood": "happy",
      "target_energy": 0.9,
      "likes_acoustic": False
    }

    explain why `Sunrise City` becomes the top song and how its score is computed
    from the current weights.
"""

from .recommender import load_songs, recommend_songs, validate_recommendations


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    print(f"\n=== {profile_name} ===")
    print(f"Preferences: {user_prefs}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)
    validation = validate_recommendations(user_prefs, recommendations)

    for rec in recommendations:
        song, score, explanation = rec
        print(f"Title: {song['title']}")
        print(f"Artist: {song['artist']}")
        print(f"Score: {score:.2f}")
        print(f"Reasons: {explanation}")
        print("-" * 40)

    print("Recommendation validation:")
    print(f"  Top genre match: {validation['top_genre_match']}")
    print(f"  Top mood match: {validation['top_mood_match']}")
    print(f"  Average score: {validation['average_score']:.2f}")
    if validation['issues']:
        print("  Issues:")
        for issue in validation['issues']:
            print(f"    - {issue}")
    else:
        print("  No issues detected. The recommender passed basic reliability checks.")


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        (
            "High-Energy Pop",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.9,
                "likes_acoustic": False,
            },
        ),
        (
            "Chill Lofi",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "calm",
                "target_energy": 0.3,
                "likes_acoustic": True,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.8,
                "likes_acoustic": False,
            },
        ),
        (
            "Adversarial Edge Case",
            {
                "favorite_genre": "pop",
                "favorite_mood": "sad",
                "target_energy": 0.95,
                "likes_acoustic": True,
            },
        ),
    ]

    for profile_name, user_prefs in profiles:
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
