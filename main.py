from make_qrcode import QRCode_embed_image, QRCode_basic


def main():
    """
    Main function to generate a QR code with a specific URL and logo.

    Returns:
    - None: The function generates and saves a QR code image.
    """
    print("Starting QR code generation process...")

    url = "https://boitekongeats.co.za"
    logo_path = "images/logo_1.png"

    # QRCode_basic(url)
    QRCode_embed_image(url, logo_path, logo_size=(90, 90),
                       img_border_radius=50, border_radius=10)

    print("QR code generation process completed.")


if __name__ == "__main__":
    main()
