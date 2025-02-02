## Inspiration
We were inspired by the urgent need to connect disaster victims with those who can help in light of recent world events. Throughout the past years, we have been witnessing a rise in natural and man-made disasters around the world. To relieve the communities struggling to secure shelter, food, and medical assistance, we developed an AI-powered platform that could instantly and optimally match victims with donors, ensuring timely and personalized relief during crises.

## What it does
CrisisConnect leverages advanced natural language processing and machine learning to analyze free-text descriptions from disaster victims and match them with donors who offer specific types of relief that best suites their needs. The platform uses a fine tuned language model to identify key needs as intents, such as shelter, food, medical assistance, transportation, financial support, and essential supplies. It then uses semantic matching to rank donor offers based on location, relevance, capacity, and textual descriptions. This ensures that help is delivered quickly and efficiently to those in need.

## How we built it
We built CrisisConnect using Python for the backend and Streamlit for the front end, integrating AI components with a matching engine. For the matching, we engineered several features. 
1. **Intent Classification**: 
Fine-tuned a BERT-based classification model to understand and categorize victim requests. The model was trained on a generative AI (ChatGPT 4) sampled dataset of disaster assistance requests across six critical categories: shelter, food, medical assistance, transportation, financial aid, and supplies. Using transfer learning, we leveraged BERT's pre-trained language understanding capabilities and fine-tuned it on our domain-specific data, achieving accurate classification of aid requests (100% accuracy) - overfitting!
2. **Semantic Matching and Scoring Algorithm**

*Intent Prediction*: Pass victims text to our fine-tuned intent classifier to get victim intent

*Embedding Computation*: Generate embedding from victim text using a pre-trained model with Sentence Transformers, we compute the donor embeddings as we perform the search

*Compute cosine similarity score*: Measure similarity between victim text description and donor text description using cosine similarity

*Geographic Distance*: Calculate geographic distance as another score using long/lat, adding a penalty to donors who are far based on our threshold. 

*Rule Based Boosts*: Add bonus points for matching the predicted intent with the donor intent, as well as a RegEx keyword match.

*Estimated Capacity Check*: Verify if donor capacity is compatible with victims needs 

*Sort and Normalize*: Sort in descending order for final score and normalize between 0 and 1. 

*Output*: We leverage Llama3-8B-Instruct LLM to summarize donor offers for the victims
 
We also developed the News and Updates page, which automatically summarizes latest news feeds related to a victims disaster. 
1. Disaster Context Extraction: We parse a user’s description for disaster keywords (like “fire,” “flood”) and location (recognized by spaCy).
2. Article Retrieval: We call a news API to fetch up to 10 English articles, sorted by their publish date, that match the extracted disaster type and location.
3. Relevancy Ranking: We compute embeddings for each article’s description (using Sentence Transformers) and compare them to the user’s embedding (the victim’s text) via cosine similarity.
4. Top 5 Summaries: The articles are sorted by similarity, and the top 5 are combined into a single text block. We then run a BART-based summarization pipeline to generate a concise, AI-driven summary of those top articles.

Finally we used streamline to host our app.  We present the summarized news in a collapsible section alongside clickable links to each relevant article, providing quick access to real-time disaster updates tailored to the user’s situation. There is also a Victim page, where victims can enter their description and get matched with donors, and a donor page where donors can enter their information to be contacted. The streamlit app is also able to automatically detect a users location, which is used throughout our pipeline. 

## Challenges we ran into
Overfitting of the intent classification model! This is likely becuase we were not able to find data to train our model, as this is difficult data to come across (victim messages), so to do this we wrote 5 examples for each category and provided it to ChatGPT to generate variations of possible messages, in a real world application this might not generalize well, which is why we have overfitting in this model.

Integration with React front end and python backend -> defaulted to streamlit instead

Creating and integrating the donor map that was made in react to streamlit, and then was not able to create a streamlit equivalent.
 
## Accomplishments that we're proud of
Proud of submitting a project and of each other! Also proud for fine-tuning a language model

## What we learned
Learned a lot of front end development (React) and learning how to integrate it with python AI functions.

## What's next for CrisisConnect
Continuously improve our methods and help people!
