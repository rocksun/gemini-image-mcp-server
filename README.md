

## Installation

# Gemini Image MCP Server

Google Gemini-based image generation and editing service providing AI image processing capabilities through MCP protocol.

## Features

- Text-to-Image Generation (generate_image)
- Image Editing & Modification (edit_image)
- PNG Format Support
- Automatic File Path Management

## 安装运行

```bash
# 安装依赖
uv pip install -r requirements.txt

# 设置环境变量（Linux/macOS）
export GEMINI_API_KEY=your_api_key_here

# Windows 设置：
setx GEMINI_API_KEY "your_api_key_here"
```

## API Documentation

### generate_image
```python
@mcp.tool()
async def generate_image(prompt: str, save_path: str = None) -> str:
    """
    :param prompt: Image generation prompt (works better in English)
    :param save_path: Optional save path (default: generated-images/ directory)
    :return: Absolute path of generated image
    """
```

### edit_image
```python
@mcp.tool()
async def edit_image(prompt: str, image_path: str, save_path: str = None) -> str:
    """
    :param prompt: 图像编辑指令（支持中文）
    :param image_path: 原始图片路径
    :param save_path: 可选保存路径，默认生成在 generated-images/ 目录
    :return: 编辑后图片的绝对路径
    """
```

## MCP Configuration
Add to mcp.json:
```json
{
    "mcpServers": {
        "gemini-image-mcp-server": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/",
                "run",
                "server.py"
            ]
        }
    }
}
```

## Important Notes
1. Ensure replacement of absolute paths in configuration
2. API key must be set through environment variables
3. Recommended to run sample code first for initial usage
4. Generated images default to generated-images directory