from typing import Any
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

def generate_image_from_gemini(prompt: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
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
            # 创建 generated-images 目录（如果不存在）
            if not os.path.exists('generated-images'):
                os.makedirs('generated-images')
            # 生成唯一文件名
            unique_filename = f"generated-images/{uuid.uuid4()}.png"
            image.save(unique_filename)
            return os.path.abspath(unique_filename)
    # 如果没有找到有效的图像数据，返回一个默认的错误信息
    return "No valid image data found."
    image.show()


@mcp.tool()
async def generate_image(prompt: str) -> str:
    """Get the image path from prompt.

    Args:
        prompt: Text used to generate the image
    """
    path = generate_image_from_gemini(prompt)
    return path

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

# if __name__ == "__main__":
#     path = generate_image_from_gemini('''Hi, can you create a 3d rendered image of a pig
#                 with wings and a top hat flying over a happy 
#                 futuristic scifi city with lots of greenery?''')
#     print(path)

    # import asyncio
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(mcp.serve())
    # loop.close()


