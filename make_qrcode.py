from PIL import Image

def prepare_logo(logo_path, border_radius):
    """
    Prepares the logo image by resizing it and applying rounded corners.

    Parameters:
    - logo_path (str): The path to the logo image.
    - border_radius (int): The radius of the rounded corners.

    Returns:
    - Image: The prepared logo image with rounded corners.
    """
    logo = Image.open(logo_path)

    # Resize the logo image
    logo_size = (100, 100)  # Adjust the size as needed
    logo = logo.resize(logo_size, Image.LANCZOS)

    # Apply rounded corners to the logo
    mask = Image.new("L", logo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, logo.size[0], logo.size[1]], radius=border_radius, fill=255)

    logo = logo.convert("RGBA")
    logo.putalpha(mask)

    return logo
