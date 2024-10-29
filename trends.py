import praw
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT", "my_news_scraper/0.1")

# Initialize Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

def fetch_trending_topics(subreddit_name, time_filter, limit=10):
    """
    Fetch trending topics from a specific subreddit for the past month.
    
    Args:
        subreddit_name (str): The subreddit to scrape from (e.g., 'worldnews' or 'popular').
        time_filter (str): The time period for top posts (e.g., 'day', 'week', 'month').
        limit (int): Number of posts to fetch.
        
    Returns:
        List of tuples: Each tuple contains (title, score, url, created_utc).
    """
    subreddit = reddit.subreddit(subreddit_name)
    trending_posts = []
    
    # Fetch top posts from the past month
    for post in subreddit.top(time_filter=time_filter, limit=limit):
        title = post.title
        
        trending_posts.append((title))
    
    return trending_posts

def fetch_trending_topics_without_api(subreddit_name, time_filter='day', limit=10):
    """
    Fetch trending topics from a specific subreddit without using the Reddit API.
    
    Args:
        subreddit_name (str): The subreddit to scrape from (e.g., 'worldnews' or 'popular').
        time_filter (str): The time period for top posts (e.g., 'day', 'week', 'month').
        limit (int): Number of posts to fetch.
        
    Returns:
        List of str: Each string contains the title of a trending post.
    """
    url = f"https://www.reddit.com/r/{subreddit_name}/top/?t={time_filter}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    trending_posts = []
    posts = soup.find_all('div', class_='top-matter')
    
    for post in posts[:limit]:
        title_element = post.find('a', class_='title')
        if title_element:
            title = title_element.text.strip()
            trending_posts.append(title)
    
    if not trending_posts:
        print("No trending topics found. The page structure might have changed.")
        trending_posts = ["Unable to fetch trending topics"]
    
    return trending_posts

