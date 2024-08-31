# QRCodeCustomizer

QRCodeCustomizer is a Python-based tool for generating QR codes with customizable features, including embedded logos and rounded corners. This tool is ideal for creating visually appealing QR codes for your brand, website, or project.

## Features

- **Custom Colors:** Easily set background and foreground colors using hex codes.
- **Embedded Logo:** Embed a logo in the center of the QR code.
- **Rounded Corners:** Add border-radius to both the QR code and the embedded logo.
- **Randomized Output:** Generate QR codes with randomized filenames for easy identification.

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## Acknowledgments

- [qrcode](https://github.com/lincolnloop/python-qrcode) library for QR code generation.
- [Pillow](https://python-pillow.org/) for image processing.

---

Happy QR coding!
