def format_for_pptgen(ai_text: str, max_slides: int = 5):
    """
    Converts AI text into PPTGen slide schema
    Uses slide_index = 0 ONLY (template duplication)
    """

    slides = []
    lines = [l.strip() for l in ai_text.split("\n") if l.strip()]

    for i, line in enumerate(lines[:max_slides]):
        slides.append({
            "type": "slide",
            "slide_index": 0,  # 🔥 IMPORTANT FIX
            "shapes": [
                {
                    "name": "Title 1",
                    "content": f"Slide {i + 1}"
                },
                {
                    "name": "Content Placeholder 2",
                    "content": line
                }
            ]
        })

    return slides
