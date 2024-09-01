
# QRCodeCustomizer

QRCodeCustomizer is a Python-based tool for generating QR codes with customizable features, including embedded logos, rounded corners, and different styles. This tool is ideal for creating visually appealing QR codes for your brand, website, or project.

## Features

- **Custom Colors:** Easily set background and foreground colors using hex codes.
- **Embedded Logo:** Embed a logo in the center of the QR code with optional rounded corners.
- **Rounded Corners:** Apply rounded corners to both the QR code and the embedded logo.
- **Randomized Output:** Generate QR codes with randomized filenames for easy identification.
- **Multiple Styles:** Choose from a variety of module drawer styles for creating unique QR code designs.
- **User Choice:** Print available QR code styles to the console for end-user selection or apply a random style automatically.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/qrcodecustomizer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd qrcodecustomizer
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your logo image in the `images` directory.
2. Update the `main.py` script with the desired URL and logo path.
3. Run the script:
    ```bash
    python main.py
    ```

The generated QR code will be saved in the `qr_codes` directory with a randomized filename.

## Customization

- **Colors:** Modify the `back_color` and `front_color` variables in `make_qrcode.py` to change the QR code colors.
- **Logo Size:** Adjust the `logo_size` in the `prepare_logo` function to resize the embedded logo.
- **Border Radius:** Change the `border_radius` variable in `make_qrcode.py` to modify the corner rounding of both the QR code and the logo.
- **Styles:** The script supports multiple module drawer styles from the `qrcode` library, allowing unique QR code appearances. The available styles are displayed for selection when you run the script.

## Example

You can generate a QR code with an embedded logo and customized styles by calling the `QRCode_embed_image` function in the `main.py` script:

```python
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

    # Choose between a basic or a styled QR code
    # QRCode_basic(url)
    QRCode_embed_image(url, logo_path, logo_size=(90, 90), img_border_radius=50, border_radius=10)

    print("QR code generation process completed.")

if __name__ == "__main__":
    main()
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## Acknowledgments

- [qrcode](https://github.com/lincolnloop/python-qrcode) library for QR code generation.
- [Pillow](https://python-pillow.org/) for image processing.

---

Happy QR coding!