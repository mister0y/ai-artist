import subprocess
import time
def run_ollama(prompt, max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['ollama', 'run', 'mistral', prompt],
                capture_output=True,
                text=True,
                check=True  # This will raise CalledProcessError if the command fails
            )
            return result.stdout
        except FileNotFoundError:
            print(f"Attempt {attempt + 1}/{max_retries}: Ollama not found, waiting {retry_delay} seconds...")
            time.sleep(retry_delay)
        except subprocess.CalledProcessError as e:
            print(f"Error running ollama: {e}")
            print(f"stderr: {e.stderr}")
            return None
    
    print("Failed to run ollama after multiple attempts")
    return None

def generate_prompt(topics):
    prompt_template = """You are an AI artist. Your job is to create a short prompt for a text-to-image model that will make a piece of art
    in the form of a painting or drawing based on the most trending topics in the world today. Here are today's trending topics in the world:

    {topics}

    Please select a topic from this list to base the prompt on. The topic should not be about a company or sports club. The prompt should be short and concise. 
    The prompt should create a piece of art that is visually striking and attention-grabbing. The style should be a little abstract and futuristic. 
    The prompt should mention that the piece of art should be a painting or a drawing. 
    Also provide a title for the piece of art.
    Format your response as follows:
    Prompt: [Your generated prompt]
    Title: [Your generated title]"""

    formatted_prompt = prompt_template.format(topics=topics)
    response = run_ollama(formatted_prompt)
    
    if response:
        prompt_line = next((line for line in response.strip().split('\n') if line.startswith('Prompt: ')), '')
        title_line = next((line for line in response.strip().split('\n') if line.startswith('Title: ')), '')
        
        prompt = prompt_line[len('Prompt: '):].strip() if prompt_line else ""
        title = title_line[len('Title: '):].strip() if title_line else ""
        
        return prompt, title
    else:
        return "A colorful abstract representation of current events", "The Pulse of Now"