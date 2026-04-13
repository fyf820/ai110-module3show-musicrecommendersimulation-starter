# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MusicRcm 1.0
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender is designed to suggest songs that match a user's current taste preferences, including their favourite genre, preferred mood, target energy level, and whether they like acoustic-sounding music. It scores every song in the catalog against those preferences and returns the top five closest matches, along with a short explanation of why each song was picked. It is built for a single user at a time to find the best available matches from a fixed library of 18 songs.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

  After the user input the features, recommender will compute each song's score using this weighted rule:  score = (genre_match × 0.25) + (mood_match × 0.35) + (1 − |target_energy − song.energy|) × 0.30 + (1 − song.acousticness) × 0.10. Once every song has a score, the list is sorted from highest to lowest. The top K songs from that sorted list are returned as the final recommendations.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  


Including 18 songs. Each song has a title, artist, genre, mood, energy level, tempo, valence, danceability, and acousticness stored in a CSV file. The dataset covers 15 genres, including pop, lofi, rock, jazz, hip-hop, classical, metal, folk, electronic, and reggae; 14 distinct moods ranging from happy and chill to sad, angry, and melancholic. I didn't remove song but add 8 songs. Many genres and moods are not included, like k-pop in the test. Most genres and moods appear only once.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The scoring captures energy proximity well in a relative sense. When two songs share the same genre and mood, the one closer in energy to what the user asked for correctly floats to the top. The explanation system also works as intended for the straightforward cases. If a song matches genre, mood, and energy, the "why" line summarises all three and makes the recommendation feel justified rather than arbitrary.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The filter has a bubble ceiling, that is any same-genre+mood song scoring >= 0.76 permanently locks out every other genre, no matter how musically close those songs are. For example, for a profile which likes lofi and chill song, the same 3 songs appear at #1–#2 o matter what energy or acoustic adjustments the user makes. This is a filter bubble and the system reinforces what the user already likes and makes cross-genre discovery structurally impossible.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested all three profiles: a user who wants sad music but with very high energy (0.95), a user whose favourite genre doesn't exist in the dataset (k-pop), and a user who likes electronic music but also prefers acoustic-sounding songs. For each one I was looking at whether the top result actually made sense for that person. The most surprising result came when I ran the weight experiment. I halved the importance of genre and doubled the importance of energy, the Ghost Genre profile (k-pop) was completely unchanged. I think it is because k-pop doesn't exist in the dataset, the genre score was already zero for every single song. It didn't matter whether that zero was multiplied by any weight.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I want to add some features or preferences that invloves tempo_bpm,valence,and danceability. Those data was collected in the dataset but not used. I want to add them into the score system, so the rank might change a lot based on user's profile.


---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I have learned how collaborative filtering and content-based filtering works toghther. I think if the recommender could be extended into a streaming platform, it can add collaborative filetering and redesign the score system to make the recommendation more accurate.
The AI tools fasted my work but I need to double check it every time it wants to make any change on the original file in case there are any bugs.
I used to think the recommendation score system should be really complex. But AI helps me made the one that not really bias at once. The output of the formula is as my expected in such a small dataset. If the dataset is larger the formula might need to be update, but in this project it works well.
I think I need to add some features or preferences that invloves tempo_bpm,valence,and danceability.