# Reflection: Profile Comparisons

This file documents observations from running VibeMatch 1.0 with different user profiles and comparing the outputs.

---

## Profile 1 vs Profile 2: High-Energy Pop Fan vs Chill Lofi Listener

**High-Energy Pop Fan** (`genre=pop, mood=happy, energy=0.85`) → Top: Sunrise City (4.46), Gym Hero (3.38), Rooftop Lights (2.36)

**Chill Lofi Listener** (`genre=lofi, mood=chill, energy=0.38, likes_acoustic=True`) → Top: Library Rain (4.89), Midnight Coding (4.79), Focus Flow (3.86)

**What changed**: The entire top 5 is different between these two profiles — no song appears in both lists. This makes sense: energy is nearly inverted (0.85 vs 0.38) and both genre and mood are different. The acoustic bonus for Profile 2 further reinforced the separation, pushing high-acousticness lofi tracks to the very top. The pop profile's top scores are slightly lower because the pop catalog has only 3 songs, giving fewer opportunities for a strong genre+mood+energy triple match.

---

## Profile 2 vs Profile 3: Chill Lofi Listener vs Deep Intense Rock Fan

**Chill Lofi Listener** → Top: Library Rain (4.89), Midnight Coding (4.79), Focus Flow (3.86)

**Deep Intense Rock Fan** (`genre=rock, mood=intense, energy=0.92`) → Top: Storm Runner (4.48), Gym Hero (2.48), Iron Sky (2.43)

**What changed**: The chill profile's scores are tightly clustered at the top because lofi is over-represented in the catalog (3 songs, all fitting the chill/low-energy pattern). The rock profile drops off much faster after #1 because there is only 1 rock song in the catalog. After "Storm Runner," the recommender falls back to mood and energy matches from unrelated genres (pop/intense, metal/intense). This illustrates a key limitation: a small, imbalanced dataset forces the system to recommend songs from neighboring genres rather than true matches.

---

## Profile 1 vs Profile 3: High-Energy Pop Fan vs Deep Intense Rock Fan

**High-Energy Pop Fan** → Top: Sunrise City (4.46), Gym Hero (3.38), Rooftop Lights (2.36)

**Deep Intense Rock Fan** → Top: Storm Runner (4.48), Gym Hero (2.48), Iron Sky (2.43)

**What changed**: "Gym Hero" (pop/intense, energy 0.93) appears in the top 5 for BOTH profiles. For the pop fan it ranks #2 because of the genre match; for the rock fan it also ranks #2 because of the mood match (intense). This is an interesting overlap — Gym Hero is a "crossover" song in this catalog. It also shows that a very high energy + matching mood can make a song cross genre boundaries in the rankings. The pop fan sees it as a slightly-off pop song; the rock fan sees it as an acceptable energetic alternative when no more rock songs exist.

---

## Edge Case: Conflicting Preferences (energy=0.9, mood=sad)

**Adversarial Profile** (`genre=pop, mood=melancholy, energy=0.9`) → Expected: confusion

Results: "Gym Hero" (pop/intense, 0.93 energy) scored 3.48 — genre match + strong energy closeness. "Delta Blues" (blues/melancholy, 0.44 energy) scored only 1.56 — mood matched but energy was very far off. The system chose a pop/intense song over a truly melancholy song because genre + energy outweigh mood. A user who wants high-energy but sad music would likely be disappointed — the system cannot distinguish between "intense-sad" and "intense-happy" within the same genre. This is a genuine limitation of having only one mood field.

---

## Key Takeaway

Comparing profiles shows that the recommender works best when the user's preferences align with the genre distribution of the catalog, and when all three main signals (genre, mood, energy) point in the same direction. When preferences conflict or a genre is under-represented, the system degrades gracefully by finding the best available partial match rather than refusing to recommend — but those partial matches may not feel satisfying to the user.
