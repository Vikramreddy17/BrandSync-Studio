# agents/designer.py (FIXED - No More Duplicate Images)
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import urllib.parse
import time
import random

class AgentState: pass 

def designer(state: AgentState) -> AgentState:
    """Generates professional AI visuals with unique prompts every time."""
    copy = state["copy"]
    strategy = state["strategy"]
    brief = state.get("brief", "")
    rev_count = state.get('revision_count', 0)
    
    # Extract key concepts from the brief
    brief_lower = brief.lower()
    
    # MUCH MORE SPECIFIC subject detection
    if "product" in brief_lower or "launch" in brief_lower:
        if "speaker" in brief_lower or "audio" in brief_lower:
            main_subject = "sleek smart speaker device on podium, sound waves visualization, product photography"
        elif "phone" in brief_lower or "mobile" in brief_lower:
            main_subject = "modern smartphone with glowing screen, app interface visible, product shot"
        else:
            main_subject = "innovative tech product on display pedestal, product launch event atmosphere"
    
    elif "event" in brief_lower or "webinar" in brief_lower or "conference" in brief_lower or "summit" in brief_lower:
        main_subject = "crowded auditorium with large presentation screen, conference attendees, event photography, stage lighting"
    
    elif "announcement" in brief_lower or "news" in brief_lower or "breakthrough" in brief_lower:
        main_subject = "dramatic spotlight on announcement podium, press conference setup, journalists with cameras"
    
    elif "brand" in brief_lower or "story" in brief_lower or "mission" in brief_lower or "empower" in brief_lower:
        main_subject = "diverse team of professionals collaborating in modern office, inspiring workspace, corporate lifestyle"
    
    elif "research" in brief_lower or "innovation" in brief_lower or "neural" in brief_lower:
        main_subject = "scientists in advanced laboratory, high-tech equipment, research facility, data visualization screens"
    
    elif "creative" in brief_lower or "design" in brief_lower or "artists" in brief_lower:
        main_subject = "artist working on digital tablet in creative studio, colorful design workspace, creative process"
    
    elif "agency" in brief_lower or "autonomous" in brief_lower:
        main_subject = "futuristic AI control room with robotic arms, holographic displays showing BrandSync Studio, cyberpunk aesthetic"
    
    else:
        # Randomize default to avoid caching
        subjects = [
            "modern tech office with glass walls and city view",
            "sleek corporate presentation room with large displays",
            "innovative startup workspace with collaborative areas",
            "high-tech control center with multiple monitors"
        ]
        main_subject = random.choice(subjects)
    
    # More varied style options
    if "playful" in strategy.lower():
        style = f"vibrant rainbow colors, {random.choice(['fun confetti effects', 'playful bubble elements', 'cheerful atmosphere'])}, bright daylight"
    elif "energetic" in strategy.lower():
        style = f"high energy scene, {random.choice(['motion trails', 'speed lines', 'dynamic angles'])}, intense dramatic lighting"
    elif "corporate" in strategy.lower() or "professional" in strategy.lower():
        style = f"ultra professional, {random.choice(['clean minimalist', 'elegant sophisticated', 'polished premium'])}, soft natural lighting"
    else:
        style = "photorealistic, cinematic composition, professional photography"
    
    # Add random seed to prevent caching
    random_seed = random.randint(1000, 9999)
    timestamp = int(time.time())
    
    # Build HIGHLY customized prompt with cache-busting
    image_prompt = (
        f"{main_subject}, "
        f"theme: {brief[:60]}, "
        f"'BrandSync Studio' subtle branding, "
        f"{style}, "
        f"professional commercial photography, 8k ultra detailed, "
        f"seed:{random_seed}"  # This prevents caching!
    )
    
    path = f"output_content/image_rev_{rev_count}.png"
    os.makedirs("output_content", exist_ok=True)
    
    # Try Pollinations with cache-busting
    try:
        print(f"🎨 Generating unique image...")
        print(f"📝 Prompt: {image_prompt[:120]}...")
        
        if generate_pollinations_unique(image_prompt, path, timestamp):
            print(f"✅ Successfully generated unique image")
            state["image_prompt"] = image_prompt
            state["image_path"] = path
            return state
    except Exception as e:
        print(f"⚠️ Generation failed: {e}")
    
    print("📦 Creating premium styled image...")
    create_premium_fallback(path, brief, strategy, rev_count, main_subject)
    
    state["image_prompt"] = image_prompt
    state["image_path"] = path
    return state


def generate_pollinations_unique(prompt, path, timestamp):
    """Pollinations.ai with cache-busting parameters."""
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Add multiple cache-busting parameters
    image_url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width=1200&height=630"
        f"&nologo=true"
        f"&enhance=true"
        f"&model=flux"
        f"&seed={random.randint(1, 999999)}"  # Random seed
        f"&timestamp={timestamp}"  # Current timestamp
    )
    
    response = requests.get(image_url, timeout=60)
    if response.status_code == 200 and len(response.content) > 5000:
        img = Image.open(BytesIO(response.content))
        img.save(path, format='PNG', quality=95)
        return True
    return False


def create_premium_fallback(path, brief, strategy, rev_count, main_subject):
    """Creates highly customized fallback image based on brief."""
    width, height = 1200, 630
    
    # Highly varied color schemes based on content
    if "product" in brief.lower():
        bg_colors = [(20, 20, 40), (60, 60, 100)]
        accent = (100, 200, 255)
        theme_text = "PRODUCT LAUNCH"
    elif "event" in brief.lower() or "conference" in brief.lower():
        bg_colors = [(80, 20, 80), (150, 50, 150)]
        accent = (255, 200, 100)
        theme_text = "LIVE EVENT"
    elif "creative" in brief.lower():
        bg_colors = [(180, 50, 100), (220, 100, 150)]
        accent = (255, 220, 100)
        theme_text = "CREATIVE STUDIO"
    elif "research" in brief.lower() or "innovation" in brief.lower():
        bg_colors = [(10, 50, 80), (30, 100, 140)]
        accent = (0, 255, 200)
        theme_text = "INNOVATION LAB"
    else:
        bg_colors = [(10, 25, 47), (29, 53, 87)]
        accent = (69, 178, 157)
        theme_text = "AI POWERED"
    
    # Create base with gradient
    img = Image.new('RGB', (width, height), color=bg_colors[0])
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient
    for i in range(height):
        ratio = i / height
        r = int(bg_colors[0][0] + (bg_colors[1][0] - bg_colors[0][0]) * ratio)
        g = int(bg_colors[0][1] + (bg_colors[1][1] - bg_colors[0][1]) * ratio)
        b = int(bg_colors[0][2] + (bg_colors[1][2] - bg_colors[0][2]) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    
    # Varied geometric patterns based on content
    glow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    if "event" in brief.lower():
        # Stage-like composition
        glow_draw.rectangle([100, 400, 1100, 600], fill=accent + (40,))
        glow_draw.ellipse([400, 100, 800, 400], fill=accent + (30,))
    elif "product" in brief.lower():
        # Pedestal composition
        glow_draw.ellipse([450, 200, 750, 500], fill=accent + (50,))
        glow_draw.rectangle([500, 400, 700, 550], fill=accent + (40,))
    else:
        # Default tech composition
        glow_draw.ellipse([50, 50, 350, 350], fill=accent + (30,))
        glow_draw.rectangle([850, 250, 1100, 550], fill=accent + (40,))
    
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=25))
    img.paste(glow_layer, (0, 0), glow_layer)
    
    # Sharp outlines
    if "event" in brief.lower():
        draw.rectangle([100, 400, 1100, 600], outline=accent, width=4)
    else:
        draw.ellipse([50, 50, 350, 350], outline=accent, width=3)
        draw.rectangle([850, 250, 1100, 550], outline=accent, width=3)
    
    # Fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 70)
        font_theme = ImageFont.truetype("arial.ttf", 28)
        font_subtitle = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 22)
    except:
        try:
            font_title = ImageFont.truetype("Arial.ttf", 70)
            font_theme = ImageFont.truetype("Arial.ttf", 28)
            font_subtitle = ImageFont.truetype("Arial.ttf", 32)
            font_small = ImageFont.truetype("Arial.ttf", 22)
        except:
            font_title = ImageFont.load_default()
            font_theme = font_title
            font_subtitle = font_title
            font_small = font_title
    
    # Theme label at top
    draw.text((width//2, 80), theme_text, fill=accent, font=font_theme, anchor="mm")
    
    # Brand name
    shadow_offset = 4
    draw.text((width//2 + shadow_offset, 220 + shadow_offset), "BrandSync Studio", 
             fill=(0, 0, 0, 120), font=font_title, anchor="mm")
    draw.text((width//2, 220), "BrandSync Studio", 
             fill=(255, 255, 255), font=font_title, anchor="mm")
    
    # Brief excerpt
    brief_words = " ".join(brief.split()[:8]) + "..."
    draw.text((width//2, 320), brief_words, 
             fill=(220, 220, 220), font=font_small, anchor="mm")
    
    # Dynamic tagline based on content
    if "launch" in brief.lower():
        tagline = "Revolutionary Launch Experience"
    elif "event" in brief.lower():
        tagline = "Transforming Virtual Events"
    elif "creative" in brief.lower():
        tagline = "Empowering Creative Innovation"
    elif "research" in brief.lower():
        tagline = "Advancing AI Research"
    else:
        tagline = "AI-Powered Brand Consistency"
    
    draw.text((width//2, 400), tagline, fill=accent, font=font_subtitle, anchor="mm")
    
    # Revision badge
    if rev_count > 0:
        draw.rounded_rectangle([width//2 - 140, 520, width//2 + 140, 570],
                              radius=25, fill=accent + (220,), outline=(255, 255, 255), width=2)
        draw.text((width//2, 545), f"✓ Revision {rev_count}", 
                 fill=(255, 255, 255), font=font_small, anchor="mm")
    
    # Scanlines
    for i in range(0, height, 3):
        draw.line([(0, i), (width, i)], fill=(255, 255, 255, 3), width=1)
    
    # Enhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    
    img.save(path, format='PNG', quality=95)
    print(f"✅ Unique styled image created")