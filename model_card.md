# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch 1.0 is designed to suggest songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference. It is intended for classroom exploration and learning — not for deployment to real users. The system assumes the user can describe their taste in simple terms (a genre name, a mood word, and a 0–1 energy number). It is not designed to handle ambiguous or evolving preferences, large catalogs, or real-time user behavior.

---

## 3. How the Model Works

VibeMatch is a **content-based recommender**. It does not know anything about other listeners — it only compares what a user says they want against the properties of each song.

For every song in the catalog, the system computes a score using four rules:

1. **Genre match** — If the song's genre is the same as the user's favorite genre, it earns the most points (2 out of a maximum of 5). Genre is weighted highest because it is the strongest predictor of whether someone will enjoy a song.

2. **Mood match** — If the song's mood matches the user's preferred mood (e.g., both are "happy" or both are "chill"), the song earns 1 additional point. This captures the emotional tone the user is looking for.

3. **Energy closeness** — The system measures the gap between the song's energy (0 = very calm, 1 = very intense) and the user's target energy. A song with zero gap earns 1.5 points; a song at the opposite extreme earns 0. This rewards intensity alignment even when genre and mood do not match.

4. **Acoustic bonus** — If the user says they prefer acoustic music, songs with higher acoustic character earn a small bonus (up to 0.5 points). This only applies when the user has indicated this preference.

After scoring every song, the system sorts them from highest to lowest and returns the top results along with plain-language reasons for each recommendation.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. The 10 original songs came with the starter project; 8 more were added to improve diversity.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, classical, hip-hop, r&b, country, metal, blues, reggae.

Moods represented: happy, chill, intense, relaxed, focused, moody, energetic, calm, confident, romantic, nostalgic, melancholy.

Each song has numerical features — energy, valence, danceability, acousticness, tempo — all on a consistent scale, making math-based comparisons straightforward.

**Limitations of the dataset:**
- Pop and lofi are over-represented (3 songs each) compared to genres like jazz, blues, or reggae (1 song each).
- All songs were synthetically generated for classroom use, so they may not accurately reflect real musical diversity.
- There are no songs that span multiple genres (e.g., jazz-pop crossovers), which is common in real catalogs.

---

## 5. Strengths

- **Transparent explanations**: every recommendation includes a reason ("genre match (+2.0); energy closeness (+1.46)") so users understand exactly why a song was chosen.
- **Works well for clear profiles**: users with a strong genre preference and a specific energy target (e.g., "high-energy pop" or "chill lofi") get highly relevant top results.
- **Fast and simple**: the algorithm runs in microseconds on an 18-song catalog and requires no training data or external libraries.
- **Acoustic preference modeling**: the optional acoustic bonus meaningfully differentiates otherwise similar songs.

---

## 6. Limitations and Bias

- **Genre dominance**: the genre weight (2.0) is double the mood weight (1.0). A pop song with a mismatched mood will almost always beat a perfectly mood-matched song in a different genre. This creates a filter bubble for genre.

- **Exact string matching**: "indie pop" does not match "pop" even though the genres are related. Users who like pop might miss good indie pop songs because the genre field does not capture sub-genres or relationships between genres.

- **Over-representation of pop**: pop has 3 songs, giving a pop-preferring user more options at the top of the list. A blues or reggae fan has only 1 song in their genre, meaning the recommender will quickly fall back to energy-based matches in unrelated genres.

- **No user history**: the system cannot learn from skips, replays, or ratings. A user who hates "Gym Hero" but loves "Sunrise City" will keep seeing Gym Hero in the top 5 for intense-pop profiles.

- **Static taste assumption**: the user profile never changes. Real listeners' moods and preferences shift throughout the day, week, and over time.

---

## 7. Evaluation

Three distinct user profiles were tested:

**Profile 1 — High-Energy Pop Fan** (`genre=pop, mood=happy, energy=0.85`):
Results matched expectation. "Sunrise City" ranked #1 with a near-perfect score (4.46/5.0). The top 2 were both pop songs. The system correctly pushed lower-energy or different-genre songs to positions 3–5.

**Profile 2 — Chill Lofi Listener** (`genre=lofi, mood=chill, energy=0.38, likes_acoustic=True`):
Results matched expectation. The two lofi/chill songs dominated with scores above 4.8. Notably, "Spacewalk Thoughts" (ambient, not lofi) still appeared at #4 because it matched mood, energy, and acoustic preference — showing the system can surface relevant songs from neighboring genres.

**Profile 3 — Deep Intense Rock Fan** (`genre=rock, mood=intense, energy=0.92`):
"Storm Runner" ranked #1 as expected. "Gym Hero" (pop/intense) ranked #2 before "Iron Sky" (metal/intense). This was a mild surprise — the metal song with a closer energy to the user's target was outranked by a pop song because mood match added a full point to "Gym Hero."

**Experiment — Weight Shift**: doubling the energy weight and halving the genre weight caused "Iron Sky" to overtake "Gym Hero" for the rock profile but also caused a high-energy electronic song ("Bass Drop") to appear in the top 5 for users with low energy targets, which felt wrong. The original weights performed better overall.

**Tests**: both unit tests in `tests/test_recommender.py` pass — sorting order is correct, and explanations are non-empty strings.

---

## 8. Future Work

1. **Fuzzy genre matching**: treat "indie pop" as related to "pop" and award partial credit for sub-genre overlap, rather than requiring an exact string match.

2. **Diversity penalty**: if two songs from the same genre already appear in the top results, apply a small score penalty to the third song from that genre to force more variety.

3. **User history support**: allow the user to mark songs as liked or skipped. Use that signal to dynamically adjust weights — for example, if the user skips high-energy songs, lower the target energy automatically.

4. **Valence and danceability scoring**: the current model does not use `valence` (positivity) or `danceability` even though these are in the dataset. Adding them could improve accuracy for users who care about feel-good or dance-floor vibes separately from general energy.

---

## 9. Personal Reflection

The most surprising thing about building VibeMatch was how quickly a small difference in weights changed which songs appeared at the top. Doubling the energy weight from 1.5 to 3.0 moved a metal song above a pop song for a pop-preferring user — a clearly wrong result — just because their energy values happened to be close. This made me realize that the "weights" in a scoring algorithm are not neutral math: they encode assumptions about what users care about, and getting them wrong produces confidently wrong recommendations.

Building this also changed how I think about Spotify's recommendation engine. It is easy to assume that a large platform's suggestions are deeply intelligent. But at the core, the algorithm is doing something similar: computing a distance between "you" and "each song" and returning the nearest neighbors. The magic comes from having thousands of features (listening history, skip patterns, time-of-day behavior, friends' playlists) instead of four hand-crafted rules. Human judgment still matters in deciding which features to include, how to weight them, and — most importantly — whether the recommendations are fair to users whose taste does not fit the majority patterns in the training data.
