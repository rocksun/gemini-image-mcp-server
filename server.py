from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types
from io import BytesIO
import os
import uuid
from PIL import Image
import sys

# Initialize FastMCP server
mcp = FastMCP("gemini-image-mcp-server")

def get_gemini_client():
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    return client

def generate_image_from_gemini(prompt: str, save_path: str = None) -> str:
    if save_path is None:
        import uuid
        save_path = f'{uuid.uuid4()}.png'
    client = get_gemini_client()
    contents = (prompt)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            # print(part.text)
            sys.stderr.write(part.text + '\n')
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            # Ensure the save directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            image.save(save_path)
            return os.path.abspath(save_path)
    # 如果没有找到有效的图像数据，返回一个默认的错误信息
    return "No valid image data found."
    image.show()

def edit_page_from_gemini(prompt: str, image_path: str, save_path: str) -> str:
    image = Image.open(image_path)
    client = get_gemini_client()
    text_input = (prompt,)

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            sys.stderr.write(part.text + '\n')
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(save_path)
            return os.path.abspath(save_path)
    return "No valid image data found."

    
@mcp.tool()
async def generate_image(prompt: str, save_path: str = None) -> str:
    """
    Generate an image based on the given prompt and save it to the specified path.

    Args:
        prompt (str): The prompt used to generate the image.
        save_path (str, optional): The path to save the generated image. If not provided, a default path will be used.

    Returns:
        str: The absolute path of the saved image, or an error message if no valid image data is found.
    """
    if save_path is None:
        save_path = os.path.join('generated-images', f'{uuid.uuid4()}.png')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
    path = generate_image_from_gemini(prompt, save_path)
    return path

@mcp.tool()
async def edit_image(prompt: str, image_path: str, save_path: str = None) -> str:
    """
    :param prompt: Image editing instruction (supports Chinese)
    :param image_path: Original image path
    :param save_path: Optional save path (default: generated-images/ directory)
    :return: Absolute path of edited image
    """
    if save_path is None:
        save_path = os.path.join('generated-images', f'{uuid.uuid4()}.png')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
    path = edit_page_from_gemini(prompt, image_path, save_path)
    return path

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

# if __name__ == "__main__":
#     import asyncio
#     # path = asyncio.run(generate_image('''Hi, can you create a 3d rendered image of a pig
#     #             with wings and a top hat flying over a happy 
#     #             futuristic scifi city with lots of greenery?'''))

#     path = asyncio.run(edit_image('''Add a watermark in the bottom right corner saying \"Clouds & People\"''', 'generated-images\\71f03828-1ede-4b5c-9bc0-1f2af0a87895.png'))
#     print(path)

    # import asyncio
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(mcp.serve())
    # loop.close()


