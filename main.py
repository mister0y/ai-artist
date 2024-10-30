from trends import fetch_trending_topics
from create_prompt import generate_prompt
from create_image import generate_image_huggingface
import os
import random

def main():
    # Fetch trending topics

    subreddit = random.choice(["upliftingnews", "worldnews", "technology"])
    trending_topics = fetch_trending_topics(subreddit_name=subreddit, time_filter="day", limit=10)    
    
    # Print trending topics
    print("Trending Topics:")
    for topic in trending_topics:
        print(f"- {topic}")
    
    # Generate prompt using Mistral
    prompt, title = generate_prompt(trending_topics)
    
    # Print generated prompt
    print("\nGenerated Prompt:")
    print(prompt)
    print("\nGenerated Title:")
    print(title)

    # Generate image using openjourney
    image = generate_image_huggingface(prompt, title)
    
    index = 1
    while os.path.exists(f"generated_image_{index}.png"):
        index += 1
    
    image.save(f"generated_image_{index}.png")
    
    print("\nImage generated and saved as 'generated_image.png'")

if __name__ == "__main__":
    main()