import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageStat
import cv2
import os
import random


def prepare_logo(logo_path, border_radius, logo_size=(100, 100)):
    """
    Prepares the logo image by resizing it using OpenCV for better quality,
    and adding rounded corners.

    Parameters:
    - logo_path: Path to the logo image.
    - border_radius: Radius for rounded corners.
    - logo_size: Desired size for the logo (width, height).
    """
    # Load the logo using OpenCV
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

    # Resize the logo using OpenCV with high-quality interpolation
    resized_logo = cv2.resize(logo, logo_size, interpolation=cv2.INTER_LANCZOS4)

    # Convert OpenCV image (BGR or BGRA) to PIL format (RGBA)
    logo_pil = Image.fromarray(cv2.cvtColor(resized_logo, cv2.COLOR_BGRA2RGBA))

    # Apply rounded corners
    mask = Image.new("L", logo_pil.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, logo_pil.size[0], logo_pil.size[1]], radius=border_radius, fill=255)

    logo_pil.putalpha(mask)

    # Save the compressed logo to the 'images' folder
    os.makedirs("images", exist_ok=True)
    compressed_logo_path = f"images/compressed_logo.png"
    logo_pil.save(compressed_logo_path, format='PNG')

    return compressed_logo_path


def hex_to_rgb(hex_color):
    """
    Converts a hex color code to an RGB tuple.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_dominant_color(image):
    """
    Gets the dominant color of an image.
    """
    # Resize the image to reduce computation, keeping a small size
    image = image.convert('RGB').resize((50, 50))
    # Use the ImageStat module to find the mean color
    stat = ImageStat.Stat(image)
    return tuple(int(x) for x in stat.mean)


def add_border_radius(image, radius):
    """
    Adds rounded corners to the image.
    """
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)

    image = image.convert("RGBA")
    image.putalpha(mask)

    return image


def QRCode_embed_image(url, img_path, logo_size=(100, 100), img_border_radius=10,border_radius=10, output_format='PNG'):
    """
    Generates a styled QR code with an embedded logo and rounded corners, then saves it to a file.
    Allows customization of logo size, border radius, and output format.
    """
    print("Initializing QR code generation...")

    os.makedirs("qr_codes", exist_ok=True)
    print("Output directory checked/created: 'qr_codes'")

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    print("QR code object created with high error correction.")

    qr.add_data(url)
    qr.make(fit=True)
    print(f"URL '{url}' added to the QR code.")

    # Prepare and compress the logo
    compressed_logo_path = prepare_logo(img_path, img_border_radius, logo_size)
    logo = Image.open(compressed_logo_path)

    # Determine the background color from the image
    back_color = get_dominant_color(logo)
    # If the background color is too light, use white as default
    if sum(back_color) > 700:  # adjust the threshold as needed
        back_color = (255, 255, 255)
    print(f"Background color determined: {back_color}")

    front_color = hex_to_rgb("#000000")

    # Create the QR code image
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=GappedSquareModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=back_color, front_color=front_color)
    )
    print("QR code generated with custom colors.")

    # Embed the logo manually
    qr_img = qr_img.convert("RGBA")  # Ensure QR code image has alpha channel
    logo_size_scaled = (logo_size[0], logo_size[1])
    logo.thumbnail(logo_size_scaled, Image.LANCZOS)  # Use Image.LANCZOS for high-quality resizing

    # Calculate positioning for the logo
    qr_width, qr_height = qr_img.size
    logo_width, logo_height = logo.size
    pos = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    # Overlay the logo on the QR code
    qr_img.paste(logo, pos, mask=logo)
    print("Logo embedded into the QR code.")

    # Apply rounded corners to the entire QR code
    qr_img = add_border_radius(qr_img, border_radius)

    random_number = random.randint(1000, 9999)
    output_filename = f"qr_{random_number}.{output_format.lower()}"

    output_path = f"qr_codes/{output_filename}"
    qr_img.save(output_path, format=output_format)  # Save in chosen format
    print(f"QR code saved to '{output_path}'.")

    print("QR code generation completed successfully.")

def QRCode_basic(url,
                 back_color=hex_to_rgb("#ffffff"),
                 front_color=hex_to_rgb("#000000"),
                 error_correction=qrcode.constants.ERROR_CORRECT_H,
                 output_format='PNG'):
    """
    Generates a basic QR code without an embedded logo, then saves it to a file.
    Allows customization of colors, error correction level, and output format.
    """
    print("Initializing basic QR code generation...")

    os.makedirs("qr_codes", exist_ok=True)
    print("Output directory checked/created: 'qr_codes'")

    qr = qrcode.QRCode(
        error_correction=error_correction  # Custom error correction level
    )
    print("QR code object created with high error correction.")

    qr.add_data(url)
    qr.make(fit=True)
    print(f"URL '{url}' added to the QR code.")

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=GappedSquareModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=back_color, front_color=front_color)
    )
    print("Basic QR code generated with custom colors.")

    random_number = random.randint(1000, 9999)
    output_filename = f"basic_qr_{random_number}.{output_format.lower()}"

    output_path = f"qr_codes/{output_filename}"
    qr_img.save(output_path, format=output_format)  # Save in chosen format
    print(f"Basic QR code saved to '{output_path}'.")

    print("Basic QR code generation completed successfully.")