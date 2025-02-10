from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with a white background
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple circle
    draw.ellipse([40, 40, 160, 160], fill='#2e4057')
    
    # Draw text
    draw.text((85, 85), "PDF", fill='white', font=ImageFont.load_default())
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Save the image
    img.save('assets/logo.png')

if __name__ == "__main__":
    create_logo() 