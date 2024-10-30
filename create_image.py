import torch
from diffusers import StableDiffusion3Pipeline, StableDiffusionPipeline
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
import io
import base64

def generate_image_huggingface(prompt, title):
    """
    Generate an image using the OpenJourney model via HuggingFace Inference API,
    and add a title and date to it.
    
    Args:
    prompt (str): The text prompt to generate the image from.
    title (str): The title to add to the image.
    
    Returns:
    PIL.Image.Image: The generated image with title and date.
    """
    load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    client = InferenceClient(token=api_key)
    
    # Generate image using OpenJourney model
    image_bytes = client.post(
        model="prompthero/openjourney",
        data={
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "photorealistic"
            }
        }
    )
    
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Add title and date to the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    # Add title
    draw.text((10, 10), title, font=font, fill=(255, 255, 255))
    
    # Add date
    current_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((10, image.height - 30), current_date, font=font, fill=(255, 255, 255))
    
    return image

def generate_image_openjourney(prompt, title):
    """
    Generate an image using the OpenJourney model via Stable Diffusion pipeline,
    and add a title and date to it.
    
    Args:
    prompt (str): The text prompt to generate the image from.
    title (str): The title to add to the image.
    
    Returns:
    PIL.Image.Image: The generated image with title and date.
    """
    model_id = "prompthero/openjourney"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
    pipe = pipe.to(device)

    negative_prompt = "photorealistic"
    image = pipe(prompt, negative_prompt=negative_prompt).images[0]
    
    # Add title and date to the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    # Add title
    draw.text((10, 10), title, font=font, fill=(255, 255, 255))
    
    # Add date
    current_date = datetime.now().strftime("%Y-%m-%d")
    draw.text((10, image.height - 30), current_date, font=font, fill=(255, 255, 255))
    
    return image


def generate_image_SD3(prompt):
    """
    Initialize the Stable Diffusion pipeline and generate an image.
    
    Args:
    prompt (str): The text prompt to generate the image from.
    
    Returns:
    PIL.Image.Image: The generated image.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch_dtype
    ).to(device)

    if device != "cuda":
        pipe.enable_attention_slicing()

    image = pipe(
        prompt,
        negative_prompt="photorealistic",
        num_inference_steps=28,
        guidance_scale=7.0,
        height=512,
        width=512,
    ).images[0]
    
    return image

def generate_image_stability_api(prompt, title):
    """
    Generate an image using the Stability AI platform with Stable Diffusion 3 Medium 
    and add a title and date to it.
    
    Args:
    prompt (str): The text prompt to generate the image from.
    title (str): The title to add to the image.
    
    Returns:
    PIL.Image.Image: The generated image with title and date.
    """
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("STABILITY_API_KEY")
    
    if not api_key:
        raise ValueError("STABILITY_API_KEY not found in .env file")

    api_host = 'https://api.stability.ai'
    engine_id = 'stable-diffusion-xl-1024-v1-0'  # This is the current engine for SD 3

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 28,
        },
    )

    if response.status_code != 200:
        raise Exception(f"Non-200 response: {response.text}")

    # Decode the image
    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    image = Image.open(io.BytesIO(image_data))
    
    # Draw the title and date
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Replace with a specific TTF font if needed
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Position and draw title and date
    text_position = (10, 10)
    date_position = (10, 40)
    draw.text(text_position, title, fill="white", font=font)
    draw.text(date_position, date_str, fill="white", font=font)

    return image