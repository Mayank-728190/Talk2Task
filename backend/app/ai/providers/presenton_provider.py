import os
import requests
from typing import Tuple, Literal, Optional, List

# Correct endpoint - using v1, not v3
PRESENTON_API_URL = "https://api.presenton.ai/api/v1/ppt/presentation/generate"
PRESENTON_API_KEY = os.getenv("PRESENTON_API_KEY")

if not PRESENTON_API_KEY:
    raise RuntimeError("PRESENTON_API_KEY not set in environment")


def generate_presentation_with_presenton(
    content: str,
    n_slides: int = 10,
    language: str = "English",
    template: str = "general",
    export_as: Literal["pdf", "pptx"] = "pptx",
    tone: str = "default",
    verbosity: str = "standard",
    theme: Optional[str] = None,
    file_ids: Optional[List[str]] = None,
) -> Tuple[bytes, str]:
    """
    Calls Presenton API v1 and returns (file_bytes, content_type)
    
    Args:
        content: The presentation topic/content (REQUIRED)
        n_slides: Number of slides to generate (default: 10)
        language: Language for the presentation (default: "English")
        template: Template to use - options: "general", "business", "education", etc.
        export_as: Export format - 'pdf' or 'pptx'
        tone: Presentation tone - options: "default", "casual", "professional", 
              "funny", "educational", "sales_pitch"
        verbosity: Content verbosity - options: "concise", "standard", "text-heavy"
        theme: Optional theme - options: "light", "dark", "cream", "royal_blue", 
               "faint_yellow", "light_red", "dark_pink"
        file_ids: Optional list of uploaded file IDs to include
    
    Returns:
        Tuple of (file_bytes, content_type)
    
    Raises:
        RuntimeError: If API request fails
        ValueError: If invalid parameters provided
    """
    
    if export_as not in ["pdf", "pptx"]:
        raise ValueError(f"export_as must be 'pdf' or 'pptx', got '{export_as}'")
    
    if not content or not content.strip():
        raise ValueError("content cannot be empty")
    
    if n_slides < 1:
        raise ValueError("n_slides must be at least 1")

    # Correct payload structure for Presenton API v1
    # Note: Use "content" parameter (not "prompt")
    payload = {
        "content": content,  # The API expects "content"
        "n_slides": n_slides,
        "language": language,
        "template": template,
        "export_as": export_as,
        "tone": tone,
        "verbosity": verbosity,
    }
    
    # Add optional parameters only if provided
    if theme:
        payload["theme"] = theme
    if file_ids:
        payload["file_ids"] = file_ids

    headers = {
        "Authorization": f"Bearer {PRESENTON_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            PRESENTON_API_URL,
            json=payload,
            headers=headers,
            timeout=300,
        )
        
        # Log the response for debugging
        print(f"Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response Body: {response.text}")
        
        response.raise_for_status()
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Presenton API request timed out after 300 seconds")
    except requests.exceptions.HTTPError:
        error_detail = response.text
        raise RuntimeError(
            f"Presenton API error {response.status_code}: {error_detail}"
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Presenton API request failed: {str(e)}")

    # For v1 API, the response is JSON with presentation details
    # You need to download the file from the path
    try:
        response_data = response.json()
        presentation_path = response_data.get("path")
        
        if not presentation_path:
            raise RuntimeError("No path in API response")
        
        # The path is already a full URL (starts with https://)
        # Don't prepend anything to it
        if presentation_path.startswith("http://") or presentation_path.startswith("https://"):
            file_url = presentation_path
        else:
            # If it's a relative path, construct the full URL
            file_url = f"https://api.presenton.ai{presentation_path}"
        
        print(f"Downloading presentation from: {file_url}")
        
        # Download the actual file
        file_response = requests.get(file_url, timeout=60)
        file_response.raise_for_status()
        
        # Determine content type based on export format
        content_type = (
            "application/pdf"
            if export_as == "pdf"
            else "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        
        return file_response.content, content_type
        
    except Exception as e:
        raise RuntimeError(f"Failed to process API response: {str(e)}")


# Example usage:
if __name__ == "__main__":
    try:
        file_bytes, content_type = generate_presentation_with_presenton(
            content="Introduction to Machine Learning",
            n_slides=8,
            language="English",
            template="general",
            export_as="pptx",
            tone="professional",
            verbosity="standard"
        )
        
        # Save to file
        filename = "presentation.pptx"
        with open(filename, "wb") as f:
            f.write(file_bytes)
        print(f"✅ Presentation generated successfully! Saved as {filename}")
        print(f"Content-Type: {content_type}")
        print(f"File size: {len(file_bytes)} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")