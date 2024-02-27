from openai import OpenAI
from model import InteriorPlan

client = OpenAI()

instruction = """You, as an interior consultant, will propose a room layout. Based on the following interior planning information (in JSON format), please generate a photo of a beautifully laid out room. Be sure to output a photo-style image. Avoid illustration.
"""

def generate_room_image(plan: InteriorPlan):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"{instruction}{plan.json()}",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url
