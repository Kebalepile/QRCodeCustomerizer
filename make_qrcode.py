import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw
import os
import random

def hex_to_rgb(hex_color):
    """
    Converts a hex color code to an RGB tuple.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def add_border_radius(image, radius):
    """
    Adds rounded corners to the image.
    """
    # Create a rounded mask
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)

    # Apply the rounded mask to the image
    image = image.convert("RGBA")
    image.putalpha(mask)
    
    return image


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


def basic_QRCode(url, img_path):
    """
    Generates a styled QR code with an embedded logo and rounded corners, then saves it to a file.
    The QR code has a custom background and foreground color.
    """
    
    print("Initializing QR code generation...")
    
    # Ensure the output directory exists
    os.makedirs("qr_codes", exist_ok=True)
    print("Output directory checked/created: 'qr_codes'")

    # Initialize the QR code with high error correction
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    print("QR code object created with high error correction.")

    # Add the URL to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    print(f"URL '{url}' added to the QR code.")

    # Convert hex colors to RGB
    back_color = hex_to_rgb("#f3f5cc")
    front_color = hex_to_rgb("#000000")

    # Prepare the logo with a border radius
    logo = prepare_logo(img_path, border_radius=10)

    # Generate the QR code with a styled image, custom colors, and embedded logo
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=GappedSquareModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=back_color, front_color=front_color),
        embeded_image=logo  # Embed the logo with rounded corners
    )
    print("QR code generated with custom colors and embedded logo.")

    # Apply a rounded border-radius to the QR code
    border_radius = 5  # Adjust this value to change the radius
    qr_img = add_border_radius(qr_img, border_radius)

    # Generate a random 4-digit number for the filename
    random_number = random.randint(1000, 9999)
    output_filename = f"qr_{random_number}.png"

    # Save the QR code image
    output_path = f"qr_codes/{output_filename}"
    qr_img.save(output_path)
    print(f"QR code saved to '{output_path}'.")

    print("QR code generation completed successfully.")

