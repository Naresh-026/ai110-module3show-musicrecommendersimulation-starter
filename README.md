# Music Recommender Simulation

## Project Summary

This project is a content-based music recommender built in Python. It reads a catalog of 18 songs from a CSV file, scores each song against a user's taste profile, and returns a ranked list of the top recommendations along with explanations for every result.

Real-world platforms like Spotify combine two strategies: **collaborative filtering** (learning from what millions of other listeners do) and **content-based filtering** (matching song attributes directly to a user's stated preferences). This simulation focuses on content-based filtering because it does not require any data about other users — only the features of each song and the features of one user profile. Each song is scored using a weighted formula that rewards a matching genre, a matching mood, and a close energy level. The system is transparent: every recommendation comes with a plain-language reason so the user can see exactly why a song was chosen.

---

## How The System Works

### Song Features Used

Each `Song` object stores these attributes loaded from `data/songs.csv`:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | e.g. pop, rock, lofi, jazz |
| `mood` | string | e.g. happy, chill, intense, relaxed |
| `energy` | float 0–1 | Overall intensity of the track |
| `tempo_bpm` | float | Beats per minute |
| `valence` | float 0–1 | Musical positivity |
| `danceability` | float 0–1 | How suitable for dancing |
| `acousticness` | float 0–1 | Acoustic vs. electronic character |

### User Profile Fields

A `UserProfile` stores:
- `favorite_genre` — the genre the user most wants to hear
- `favorite_mood` — the emotional vibe they are in
- `target_energy` — a 0–1 number representing preferred intensity
- `likes_acoustic` — whether acoustic quality matters to them

### Algorithm Recipe (Scoring Rule)

For every song in the catalog, `score_song()` computes a numeric score:

1. **Genre match → +2.0 pts** (strongest signal — users care most about genre)
2. **Mood match → +1.0 pt** (emotional alignment matters, but less than genre)
3. **Energy closeness → up to +1.5 pts** — formula: `1.5 × (1 − |user_energy − song_energy|)`. A perfect energy match scores 1.5; a completely opposite energy scores 0.
4. **Acoustic quality bonus → up to +0.5 pts** — only applied when `likes_acoustic=True`. Formula: `0.5 × song_acousticness`.

Maximum possible score is **5.0** (genre + mood + perfect energy + full acoustic).

### Ranking Rule

`recommend_songs()` calls `score_song()` for every song, then uses Python's `sorted()` to order results from highest to lowest score, and slices the top `k` entries.

**Data flow:**

```
User Preferences
       │
       ▼
score_song() called for each song in catalog
       │
       ▼
List of (song, score, reasons) sorted descending
       │
       ▼
Top K recommendations printed with explanations
```

### Potential Bias in This Design

Genre carries 2.0 points — twice the weight of mood. A user who prefers "happy pop" will always see pop songs ranked above a better-matching "happy" song in a different genre. This means the system may under-recommend emotionally fitting songs from minority genres in the dataset.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python3 -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

### Experiment 1 — Default "Happy Pop" Profile

User prefs: `genre=pop, mood=happy, energy=0.85`

- "Sunrise City" ranked #1 (score 4.46): it matched genre, mood, AND energy closely.
- "Gym Hero" ranked #2 (3.38): genre matched but mood didn't (intense vs happy) — energy was still very close.
- "Rooftop Lights" ranked #3 (2.36): indie pop shares the "happy" mood but not the exact genre, so it placed lower than a less-happy pure-pop track.

**Observation**: The genre weight strongly determines the top half of the list. Two pop songs dominate before any other genre appears.

### Experiment 2 — Chill Lofi Listener with Acoustic Preference

User prefs: `genre=lofi, mood=chill, energy=0.38, likes_acoustic=True`

- "Library Rain" ranked #1 (4.89): lofi + chill + near-perfect energy + high acousticness (0.86 → +0.43).
- "Midnight Coding" ranked #2 (4.79): same genre/mood combo, slightly less acoustic.
- Non-lofi chill songs ("Spacewalk Thoughts", "Island Breeze") still appeared in top 5 because they matched mood + energy + had some acoustic character.

**Observation**: The acoustic bonus meaningfully separates candidates within the same genre/mood bucket and lets it reward an ambient song over a lofi song with lower acousticness.

### Experiment 3 — Weight Shift: Energy doubled, Genre halved

Temporarily changed scoring to: genre = 1.0, mood = 1.0, energy gap penalty = 3.0.

- "Storm Runner" still topped the rock profile, but the gap between #1 and #2 shrank.
- "Iron Sky" (metal, intense, 0.97 energy) jumped from #3 to a tie with "Gym Hero" for #2 because energy was now the dominant signal.
- Conclusion: when energy dominates, the system can accidentally recommend a metal song to a pop fan if they both have `energy ≈ 0.9`.

### Experiment 4 — Mood Removed (commented out)

Removing the mood match check for the rock profile changed rankings slightly: "Iron Sky" outranked "Gym Hero" because iron sky's energy was a closer match, and without the mood bonus there was nothing to reward "Gym Hero" for sharing the "intense" mood.

---

## Limitations and Risks

- **Tiny catalog**: 18 songs is too small for a real recommender; results are heavily influenced by which genres happen to be represented.
- **Single-dimension genre**: "indie pop" does not match "pop" even though they are related — the system treats genres as exact string matches.
- **No history**: the system cannot learn from what the user has already heard or skipped.
- **Static weights**: weights are hand-tuned; different users may want genre to matter less and energy to matter more.
- **No diversity control**: the top 5 can be dominated by one genre if that genre is well-represented in the catalog.

---

## Reflection

See [model_card.md](model_card.md) for the full model card.

Building this recommender made it clear how much of a "recommendation" is really just arithmetic. Platforms like Spotify are doing fundamentally the same thing — computing a similarity score between a user vector and a song vector — but with thousands of features learned from billions of listening events instead of four hand-crafted rules. The most surprising moment was seeing how the genre weight alone could drown out an otherwise excellent match: a chill jazz track with the perfect energy for a "happy pop" user will never beat a mediocre pop song, simply because the genre label doesn't match. That is a real and well-documented bias in content-based systems, and it is one reason real platforms blend collaborative signals (what do people who listen to similar things also like?) with content signals.
