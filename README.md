# Matrix Homeserver Flooder (DDoS)

A simple Python script to flood a Matrix homeserver with fake data using multithreading in order to DDoS the target, through bypassing any caching layer and stressing the database and webserver.

## Features

- Cycles through random, anonymous proxies from the scraped proxy list using the `fp` (free-proxy) library to obfuscate your IP
- Generates fake IP addresses, user agents, and other data using the `faker` library
- Sends spoofed `X-Forwarded-For` header to further obfuscate (Note: this will only work if server WAF/VCL is misconfigured and doesn't drop incoming headers)
- Runs indefinitely with multiple threads concurrently to increase the rate of DDoS attempts

## Requirements

Using `pip install`

- `requests`
- `termcolor`
- `faker`
- `free-proxy`

## Usage

`python3 matrix_flooder.py`

Enter the base URL of the Matrix homeserver when prompted. Then enter number of concurrent threads. Then choose whether to use proxies or not. The script will then continuously flood the Matrix homeserver with fake data using desired concurrent threads. Successful attempts and errors will be reported in the console.

**Note: This script is for educational purposes only and should not be used for malicious activities. The author is not responsible for any damages or consequences that may result from using this script.**
