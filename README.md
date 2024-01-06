# Web Monitoring to Telegram

This Python project leverages Selenium to automate tasks on an Azerbaijan university's portal. It actively monitors application updates and delivers notifications via a Telegram bot. The project is deployed using a free web hosting service, with modifications in the deployment script to directly execute `portal.py` through the command `python portal.py`, rather than relying on a conventional build script.

## Overview

The primary goal is to automate the monitoring of application updates on an Azerbaijan university's portal. The project employs Selenium for web automation, facilitating login, tracking application changes, and utilizing a Telegram bot for notifications. Upon deployment, the execution of `portal.py` is streamlined using the command `python portal.py`.

## Features

- Active monitoring of application updates on an Azerbaijan university's portal.
- Utilization of Selenium for web-based automation and interaction.
- Integration with a Telegram bot for seamless update notifications.
- Deployment on a free web hosting service with customized execution via `python portal.py`.
- Encryption of credentials (email, password, bot chat ID) using `encrypter.py`, stored in a JSON database, and decrypted during runtime for user visibility.
- Headless mode configuration for the WebDriver to ensure memory consumption remains below 50MB, enabling operation on any free online server.

## Usage Instructions

1. Clone this repository: `git clone https://github.com/BaselAshraf81/WebMonitoringToTelegram.git`
2. Install required packages: `pip install -r requirements.txt`
3. Configure your Telegram bot and acquire the API token.
4. Run `encrypter.py` to encrypt and store your credentials in the JSON database.
5. Configure the portal settings within `portal.py` and access encrypted credentials.
6. Test the script locally: `python portal.py`
7. Deploy the application on your preferred web hosting service, ensuring execution is set to `python portal.py`.

## Usage

- Run `portal.py` locally or after deployment to monitor updates on the university's portal.
- Receive notifications about application updates via your configured Telegram bot.

## Contribution

Contributions are welcome! Submit issues or pull requests for improvements or bug fixes.

## Disclaimer

Ensure responsible usage in compliance with the terms of use of the Azerbaijan university's portal. The project creators are not liable for any misuse or violations.

For further inquiries, please contact [Basel Ashraf](linkedin.com/in/basel-askar-920248156).
