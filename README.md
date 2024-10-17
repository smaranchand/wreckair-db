# WreckAir-DB

## Description

**WreckAir-DB** is a Python tool designed to perform a stress test on the WordPress database repair endpoint 
(`/wp-admin/maint/repair.php`). It targets the potential vulnerability of this endpoint being publicly 
accessible when the `WP_ALLOW_REPAIR` setting is enabled. The tool repeatedly sends requests to the repair 
endpoint, making the server busy, which can lead to a Denial of Service (DoS) condition.

> **Disclaimer:** This tool is for educational and testing purposes only. Use it responsibly and only on 
systems you own or have explicit permission to test. Misuse of this tool can result in significant damage to 
the target system and may lead to legal consequences.

## Features
- Validates if a target WordPress website has the database repair endpoint enabled and accessible.
- Continuously sends requests to the repair endpoint to test its response to repeated stress attempts.
- Logs results in real-time to show if the target is unresponsive.

## Requirements
- Python 3.x
- `requests` library

You can install the required dependencies using:
```sh
pip install -r requirements.txt
```
## Disclaimer
This tool is intended for **authorized testing and educational purposes only**. Using it on servers without permission is illegal. The author is not responsible for any misuse or damage caused by this tool.

## Author
- **Smaran Chand**  
  [Website](https://smaranchand.com.np) | [GitHub](https://github.com/smaranchand)

## Contribution
Feel free to open issues or contribute to the project through pull requests. Make sure your code follows the existing style and includes relevant documentation where appropriate.
