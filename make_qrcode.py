import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, 
                                               RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer)
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageStat
import cv2
import os
import random

# List of all available ModuleDrawers
available_drawers = [
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
]

def choose_module_drawer():
    print("\nAvailable QR Code Module Drawers:")
    for i, drawer in enumerate(available_drawers):
        print(f"{i + 1}. {drawer.__name__}")

    choice = input("\nChoose a Module Drawer by number, or press Enter to waive your right to choose (a random drawer will be selected): ")
    if choice.strip():
        try:
            selected_drawer = available_drawers[int(choice) - 1]
        except (IndexError, ValueError):
            print("Invalid choice. Selecting a random drawer.")
            selected_drawer = random.choice(available_drawers)
    else:
        print("You waived your right to choose. Selecting a random drawer.")
        selected_drawer = random.choice(available_drawers)

    print(f"Selected Module Drawer: {selected_drawer.__name__}\n")
    return selected_drawer

def prepare_logo(logo_path, border_radius, logo_size=(100, 100)):
    """
    Prepares the logo image by resizing it using OpenCV for better quality,
    adding rounded corners, and setting the background to white if needed.
    """
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    resized_logo = cv2.resize(logo, logo_size, interpolation=cv2.INTER_LANCZOS4)
    logo_pil = Image.fromarray(cv2.cvtColor(resized_logo, cv2.COLOR_BGRA2RGBA))

    dominant_color = get_dominant_color(logo_pil)
    if sum(dominant_color) > 700 or sum(dominant_color) < 100:
        white_background = Image.new("RGBA", logo_pil.size, (255, 255, 255, 255))
        white_background.paste(logo_pil, (0, 0), logo_pil)
        logo_pil = white_background
        print("Logo background changed to white due to light or dark dominant color.")

    mask = Image.new("L", logo_pil.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, logo_pil.size[0], logo_pil.size[1]], radius=border_radius, fill=255)

    logo_pil.putalpha(mask)
    os.makedirs("images", exist_ok=True)
    compressed_logo_path = f"images/compressed_logo.png"
    logo_pil.save(compressed_logo_path, format='PNG')

    return compressed_logo_path

def hex_to_rgb(hex_color):
    return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def get_dominant_color(image):
    image = image.convert('RGB').resize((50, 50))
    stat = ImageStat.Stat(image)
    return tuple(int(x) for x in stat.mean)

def add_border_radius(image, radius):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)

    image = image.convert("RGBA")
    image.putalpha(mask)

    return image

def QRCode_embed_image(url, img_path, logo_size=(100, 100), img_border_radius=10, border_radius=10, output_format='PNG'):
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

    compressed_logo_path = prepare_logo(img_path, img_border_radius, logo_size)
    logo = Image.open(compressed_logo_path)

    back_color = get_dominant_color(logo)
    if sum(back_color) > 700 or sum(back_color) < 100:
        back_color = hex_to_rgb("#ffffff")
    print(f"Background color determined: {back_color}")

    front_color = hex_to_rgb("#000000")

    # Allow the user to choose or randomly select a ModuleDrawer
    selected_drawer = choose_module_drawer()

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=selected_drawer(),
        color_mask=SolidFillColorMask(
            back_color=back_color, front_color=front_color)
    )
    print("QR code generated with custom colors and selected module drawer.")

    qr_img = qr_img.convert("RGBA")
    logo_size_scaled = (logo_size[0], logo_size[1])
    logo.thumbnail(logo_size_scaled, Image.LANCZOS)

    qr_width, qr_height = qr_img.size
    logo_width, logo_height = logo.size
    pos = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    qr_img.paste(logo, pos, mask=logo)
    print("Logo embedded into the QR code.")

    qr_img = add_border_radius(qr_img, border_radius)

    random_number = random.randint(1000, 9999)
    output_filename = f"qr_{random_number}.{output_format.lower()}"

    output_path = f"qr_codes/{output_filename}"
    qr_img.save(output_path, format=output_format)
    print(f"QR code saved to '{output_path}'.")

    print("QR code generation completed successfully.")

def QRCode_basic(url,
                 back_color=hex_to_rgb("#ffffff"),
                 front_color=hex_to_rgb("#000000"),
                 error_correction=qrcode.constants.ERROR_CORRECT_H,
                 output_format='PNG'):
    print("Initializing basic QR code generation...")

    os.makedirs("qr_codes", exist_ok=True)
    print("Output directory checked/created: 'qr_codes'")

    qr = qrcode.QRCode(
        error_correction=error_correction
    )
    print("QR code object created with high error correction.")

    qr.add_data(url)
    qr.make(fit=True)
    print(f"URL '{url}' added to the QR code.")

    # Allow the user to choose or randomly select a ModuleDrawer
    selected_drawer = choose_module_drawer()

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=selected_drawer(),
        color_mask=SolidFillColorMask(
            back_color=back_color, front_color=front_color)
    )
    print("Basic QR code generated with custom colors and selected module drawer.")

    random_number = random.randint(1000, 9999)
    output_filename = f"basic_qr_{random_number}.{output_format.lower()}"

    output_path = f"qr_codes/{output_filename}"
    qr_img.save(output_path, format=output_format)
    print(f"Basic QR code saved to '{output_path}'.")

    print("Basic QR code generation completed successfully.")
