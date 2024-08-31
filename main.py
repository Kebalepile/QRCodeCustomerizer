from make_qrcode import QRCode_embed_image

def main():
    """
    Main function to generate a QR code with a specific URL and logo.
    
    Returns:
    - None: The function generates and saves a QR code image.
    """
    print("Starting QR code generation process...")
    
    url = "https://boitekongeats.co.za"
    logo_path = "images/logo_1.png"  # Ensure this path is correct
    QRCode_embed_image(url, logo_path)
    
    print("QR code generation process completed.")

if __name__ == "__main__":
    main()
