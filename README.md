# 🎵 Music Recommender Simulation

## Project Overview

**Project name:** Music Recommender Simulation

This repo is a small music recommendation system that takes song metadata and a user preference profile, scores each song based on how well it matches the user, and returns a ranked playlist with explanations.

The original goal was to demonstrate an explainable recommendation pipeline, evaluate its behavior, and add a reliability check so the system is more than just a simple scorer.

## What the Project Does and Why It Matters

The system reads a catalog of songs from `data/songs.csv`, computes a recommendation score for each song using genre, mood, energy, and acousticness, and then prints the top suggestions. It also validates the output to catch weak recommendations by checking whether the top song matches the user’s genre or mood preferences.

This matters because real-world AI products need not only to make predictions, but also to justify them and verify they are reasonable.

## Architecture Overview

The project is organized into these main components:

- **Runner:** `src/main.py`
  - loads song data
  - defines user taste profiles
  - requests recommendations and prints results
- **Recommender:** `src/recommender.py`
  - `load_songs()`: loads data from `data/songs.csv`
  - `score_song()`: computes a score and explanation for each song
  - `recommend_songs()`: ranks and selects the top-K songs
  - `validate_recommendations()`: evaluates whether the output is reliable
- **Tests:** `tests/test_recommender.py`
  - verifies ranking logic and validation behavior

### Data flow

1. User preferences and the song catalog are loaded.
2. Each song is scored against the user profile.
3. Top recommendations are selected.
4. The validator checks whether the top result matches user expectations.
5. Results are printed with explanations and validation feedback.

## Setup Instructions

From the repository root:

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python3 -m src.main
```

4. Run tests:

```bash
python3 -m pytest -q
```

## Sample Interactions

### Example 1 — High-Energy Pop

Input:
- `favorite_genre`: `pop`
- `favorite_mood`: `happy`
- `target_energy`: `0.9`
- `likes_acoustic`: `False`

Output:
- Top recommendation: `Sunrise City` by `Neon Echo`
- Score: `5.34`
- Reasons: `Genre matches user favorite; Mood matches user preference; Energy is close to target (+1.84); Acoustic preference matches`
- Validation: no issues detected

### Example 2 — Chill Lofi

Input:
- `favorite_genre`: `lofi`
- `favorite_mood`: `calm`
- `target_energy`: `0.3`
- `likes_acoustic`: `True`

Output:
- Top recommendation: `Symphony of Dreams` by `Orchestra Nova`
- Score: `4.40`
- Reasons: `Mood matches user preference; Energy is close to target (+1.90); Acoustic preference matches`
- Validation: no issues detected

### Example 3 — Adversarial Edge Case

Input:
- `favorite_genre`: `pop`
- `favorite_mood`: `sad`
- `target_energy`: `0.95`
- `likes_acoustic`: `True`

Output:
- Top recommendation: `Bluesy Nights` by `Delta Blues`
- Score: `3.50`
- Reasons: `Mood matches user preference; Energy is close to target (+1.00); Acoustic preference matches`
- Validation: no issues detected

## Design Decisions

I chose a content-based scoring approach because it is transparent, easy to explain, and appropriate for a small dataset. The system evaluates genre, mood, target energy, and acoustic preference using explicit weights so every recommendation can be traced back to a score.

I also added a simple evaluation layer inside the main workflow. This reliability check is not a full production monitor, but it helps the system identify recommendations that may be weak or inconsistent with user preferences.

Trade-offs:

- Pros: easy to understand, explainable, and testable.
- Cons: limited to a small catalog, not personalized across multiple users, and not adaptive over time.

## Testing Summary

What worked:

- The project runs successfully from the repository root.
- The recommender returns consistent ranked results.
- The validator reports whether the top recommendation aligns with user preferences.
- `pytest` passes for the core functionality.

What I learned:

- Explicit rule-based scoring can be a strong baseline for recommendations.
- Integration of a validator improves trust in the output.
- Writing tests for both ranking and evaluation helps catch logic errors early.

Reliability summary:

- Automated tests: `3 passed` using `pytest`.
- Validation checks are integrated into the main app to report top genre/mood matches and average score.
- The system reports a simple confidence-like signal by flagging cases where the top recommendation does not match user preferences.
- Human review is used to inspect sample outputs and confirm the explanation text matches the recommendation logic.

## Reflection

This project taught me how to structure a small AI system so that it is both functional and explainable. I learned that the value of a recommender is not just in its output, but in how clearly it can communicate why those outputs were chosen and whether they are reliable.

For a future employer, this repo shows that I can build end-to-end AI functionality, document the design clearly, and support it with testing and evaluation.
"""