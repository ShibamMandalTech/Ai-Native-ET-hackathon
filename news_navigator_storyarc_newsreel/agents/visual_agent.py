import re
import random
from PIL import Image, ImageDraw, ImageFont
from config import VIDEO_WIDTH, VIDEO_HEIGHT

def draw_news_background(width, height, seed=None):
    if seed is not None:
        random.seed(seed)
    
    # Create RGBA image to support transparent overlays
    img = Image.new('RGBA', (width, height), color=(10, 15, 25, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle Grid
    grid_color = (30, 40, 60, 255)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=2)
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=grid_color, width=2)
        
    # 2. Tech / News Graph Line
    points = []
    num_points = 6
    x_step = width / (num_points - 1)
    
    current_y = height * 0.6
    for i in range(num_points):
        x = int(i * x_step)
        # Add random movement to the graph
        current_y += random.uniform(-300, 200)
        current_y = max(300, min(height - 400, current_y)) 
        points.append((x, int(current_y)))
        
    # Draw graph line layers (glow effect)
    for w, color in [(15, (20, 80, 200, 100)), (8, (50, 120, 255, 255)), (3, (200, 220, 255, 255))]:
        draw.line(points, fill=color, width=w, joint="curve")
        
    for p_x, p_y in points:
        r = 12
        draw.ellipse([p_x-r, p_y-r, p_x+r, p_y+r], fill=(255, 255, 255, 255), outline=(50, 120, 255, 255), width=4)

    return img

def create_slide(text, filename):
    # Dynamically draw a graph background based on the slide's filename hash
    img = draw_news_background(VIDEO_WIDTH, VIDEO_HEIGHT, seed=filename)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40) # Made font smaller as requested
    except:
        font = None

    # Text Wrapping
    words = text.split()
    lines = []
    line = ""

    for word in words:
        if len(line + word) < 38: # Adjusted wrapping for smaller font
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    # Determine text block height and anchor it towards the bottom of the screen
    # e.g. at 75% down the screen, so it doesn't overlap centered visuals
    y_start = int(VIDEO_HEIGHT * 0.75) - (len(lines) * 60)
    y_end = y_start + (len(lines) * 60)
    
    # Draw translucent black box behind text so it's readable over the graph
    draw.rectangle([40, y_start - 30, VIDEO_WIDTH - 40, y_end + 10], fill=(0, 0, 0, 180))

    y = y_start
    for l in lines:
        draw.text((60, y), l, fill=(255, 255, 255, 255), font=font)
        y += 60

    path = f"output/images/{filename}.png"
    # Convert RGBA back to RGB for video pipeline
    img.convert('RGB').save(path)
    return path

def generate_visuals(script, news_id):
    # Split by double newline (paragraphs) to break into slides
    scenes = re.split(r'\n\s*\n', script.strip())
    
    # If it's still just one big block, try falling back to single newlines
    if len(scenes) == 1:
        scenes = script.strip().split('\n')
        
    images = []
    for i, scene in enumerate(scenes):
        scene = scene.strip()
        if scene:
            img = create_slide(scene, f"{news_id}_{i}")
            images.append(img)

    return images