# Intro

Authentication is a fundamental security mechanism in APIs that verifies __who__ a user or system is before granting access. It ensures that only legitimate users can interact with the system by validating credentials such as passwords, tokens, or biometrics. Weak or improper authentication can lead to __account takeovers, unauthorized access, and credential stuffing attacks__ — making it a critical aspect of API security.

![alt text](assets/image-13.png)

---

#### Authentication vs Authorization

__Authentication__ is the process of verifying __who__ a user is. It typically involves checking credentials like usernames and passwords, tokens (e.g., JWT, OAuth), or biometric data. Authentication ensures that users are who they claim to be before granting access to a system. Common issues related to authentication include weak passwords, vulnerability to brute-force attacks, token theft, and session hijacking, all of which can compromise security.

__Authorization__, on the other hand, determines __what__ an authenticated user is allowed to do within a system. After authentication, authorization mechanisms define access controls such as read/write permissions or admin rights. Common problems with authorization include Insecure Direct Object References (IDOR), where users can access resources they shouldn't, privilege escalation, and broken access controls that allow unauthorized actions, leading to potential security breaches.

---

#### Basic Authentication vs. Token-Based Authentication  

- __Basic Authentication__: Uses a static username and password encoded in Base64 and sent with each request. While simple to implement, it lacks security since credentials are repeatedly exposed unless protected by HTTPS.  

- __Token-Based Authentication__: Uses dynamically generated tokens instead of static credentials, improving security and scalability. Common types include:  
  - __JWT (JSON Web Token)__: A self-contained token containing claims about the user, signed for integrity but not encrypted.  
  - __Bearer Token__: A token sent in the `Authorization` header, typically short-lived and used with OAuth 2.0 for secure access.  

Token-based methods enhance security by reducing credential exposure and enabling session management without storing sensitive user details.  


# Attacking Authentication

Authentication vulnerabilities in APIs and web applications are common targets for attackers. In many cases, brute force attacks can be easily launched if the system lacks proper protections such as rate limiting, account lockout mechanisms, or CAPTCHA. A deeper inspection of authentication mechanisms may also reveal logic flaws, such as improper error messages or vulnerable endpoints. These flaws can be leveraged by attackers to gain unauthorized access.

A typical issue occurs when error messages are inconsistent, allowing attackers to identify whether the username or the password is incorrect. Additionally, lack of rate limiting or brute force protection makes it possible to conduct large-scale attacks without being detected.

__Key Issues to Consider:__
- __Brute Force Attacks__: Lack of rate limiting or protection makes the authentication vulnerable to brute force. Attackers can repeatedly attempt various credentials without facing significant barriers.
- __Logic Flaws__: The authentication mechanism might reveal subtle information through inconsistent error messages or response codes, aiding attackers in refining their attack.
- __Injection Vulnerabilities__: While this may appear to be an authentication issue, the root cause could often be an injection vulnerability. Attackers may exploit flaws like SQL injection to bypass authentication altogether, thus categorizing the issue as an injection rather than broken authentication.

## Lab

#### Login Prompt

The lab starts with a simple login page where users are asked to enter their credentials (username and password).

![alt text](assets/image-26.png)

---

#### User Enumeration via Brute Force

By checking the error messages returned, it's easy to spot the difference between "Invalid username!" and "Invalid password!" messages. This inconsistency makes it possible to figure out valid usernames.

Using the `-fs` option in **ffuf**, with a filter size of 30, we can differentiate the responses based on the "Invalid username!" error message.

This reveals two valid usernames: `admin` and `jeremy`.

![alt text](assets/image-27.png)

---

#### Brute Forcing the Password

Once `admin` is confirmed as a valid username, the next step is brute-forcing the password with a wordlist. After testing, the correct password turns out to be `ramirez`.

Now, the system returns an HTTP status code 200 for successful logins, confirming the correct password.

![alt text](assets/image-28.png)

With the valid credentials (`admin` / `ramirez`), access is granted. After logging in, a flag is obtained, confirming the exploit was successful.

![alt text](assets/image-29.png)

# Attacking Tokens

APIs rely on tokens for authentication and session management, but weak implementation can expose them to attacks. Poor entropy, predictable token generation, and improper validation mechanisms allow attackers to forge or hijack tokens, leading to unauthorized access.

A common issue arises when tokens follow a structured pattern (e.g., `username-timestamp-random_suffix`), making them predictable. If entropy is low, brute-forcing or guessing valid tokens becomes feasible. Additionally, weak token signing or lack of verification can allow attackers to modify or reuse expired tokens.

__Key Issues to Consider:__  
- **Predictable Token Generation**: If tokens use timestamps, incremental IDs, or weak entropy, attackers can guess or reconstruct valid tokens.  
- **Token Hijacking & Replay Attacks**: Weak session expiration and lack of proper invalidation allow attackers to reuse stolen tokens.  
- **Signature Bypass & Manipulation**: If tokens are improperly signed, missing integrity checks, or using weak cryptographic algorithms, attackers can forge them to escalate privileges.  
- **Token Disclosure**: Tokens exposed in URLs, logs, or client-side storage can be intercepted and reused by attackers.  

Weak token management can lead to complete account takeovers, privilege escalation, and session persistence beyond intended lifetimes. Proper implementation requires secure generation, validation, and expiration mechanisms.

## Lab

The lab starts with a login prompt. Upon providing valid credentials (`admin` / `ramirez`), the application returns an `access` token.

```http
POST /v1/verify.php HTTP/1.1
Host: 172.18.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.18.0.2/
Content-Type: application/json
Content-Length: 38
Origin: http://172.18.0.2
Connection: keep-alive
Priority: u=0

{"email":"admin","password":"ramirez"}
```

![alt text](assets/image-30.png)

### Token Analysis with Sequencer

To assess randomness, the token is analyzed using Burp Suite's Sequencer. A large sample size is necessary for statistical reliability.

![alt text](assets/image-31.png)

Results:

- **Randomness Quality:** Extremely poor  
- **Estimated Entropy:** 5 bits at a 1% significance level  
- **Sample Size:** 20,000 tokens  
- **Token Length:** 18 characters (Base64-decoded)  

#### Entropy Analysis:

The entropy chart represents the estimated randomness of token values at different significance levels. Each significance level sets a threshold probability, determining whether the observed token values could reasonably occur in a truly random sequence.

If the observed patterns fall below the significance threshold, it indicates a lack of randomness, suggesting that token generation follows a predictable structure. A lower significance level demands stronger statistical evidence to reject randomness, reducing the likelihood of false positives but increasing the risk of overlooking weak randomness.

![alt text](assets/image-32.png)

---

#### Significance levels

This chart visualizes the probability that each character position in the token follows a random distribution. If certain positions show low randomness, it suggests deterministic token generation, making it easier for attackers to predict or reconstruct tokens. A weak entropy distribution increases the risk of token forgery and replay attacks.

![alt text](assets/image-33.png)

Decoding the Base64 token reveals a structured format: `username - timestamp - three-character suffix`

This predictable pattern allows attackers to reconstruct or forge tokens.

![alt text](assets/image-34.png)

---

#### Brute Forcing the Token

The token follows a structured format of `username - timestamp - three-character suffix`, which makes it susceptible to predictability. This pattern allows attackers to focus on brute-forcing only the suffix portion of the token. 

To demonstrate this, i built a simple [Python script](src/token_brute_force.py) to generate and test potential tokens for the user jeremy. The script iterates through all lowercase letter combinations for the three-character suffix, encodes each into Base64, and sends it as a session token. If the response reveals a successful login message, a valid token has been found.

```python
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

```

![alt text](assets/image-35.png)

## JSON Web Tokens

JSON Web Tokens (JWTs) are a compact, URL-safe means of representing claims between two parties. A JWT consists of three parts: the header, the payload, and the signature. Each part is base64-encoded and separated by a dot (`.`), forming the complete token. While it's easy to decode each part manually, tools like [jwt.io](https://jwt.io) can simplify the process.

- **Header**: The header typically contains metadata about the token, such as the signing algorithm used (e.g., `HS256`, `RS256`). It's a JSON object that is base64-encoded.
  
- **Payload**: The payload contains the "claims"—statements about an entity (usually the user) and additional data. Claims are categorized as:
  - **Registered Claims**: Predefined claims like `sub` (subject), `exp` (expiration), `iat` (issued at), etc.
  - **Public Claims**: Claims defined by the user that can be used across systems.
  - **Private Claims**: Custom claims meant to be shared between parties who have agreed on their usage.

- **Signature**: The signature ensures the token’s integrity and authenticity. It's created by signing the header and payload with a secret key (HMAC) or a private key (RSA, ECDSA). If the token is altered in any way, the signature becomes invalid.

Other options to inspect and manipulate JWTs include using [jwt_tool](https://github.com/ticarpi/jwt_tool) or the [jwt-editor](https://github.com/portswigger/jwt-editor) Burp Suite plugin.

To use __jwt_tool__, simply run the following command:

```bash
python3 jwt_tool.py <token>
```

This will output detailed information about the token, including the header, payload, and signature, making it easier to understand and potentially modify the contents or identify weaknesses in the token structure.

![alt text](assets/image-40.png)

If you're working in Burp Suite, the __jwt-editor__ plugin provides a user-friendly interface for analyzing and manipulating JWTs directly within the Burp Suite environment, offering features like real-time decoding, editing, and signing.


When transferring JWTs, they are typically included in the `Authorization` header of an HTTP request:

```http
POST /v1/protected-resource HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Content-Length: 55

{
  "param1": "value1",
  "param2": "value2"
}
```

It's important to remember that sometimes the secret used to sign a JWT can be weak. When combined with the fact that this type of attack can be carried out offline against a single token, it becomes a critical test. Weak secrets make it easier for attackers to brute-force the token signature, which can ultimately lead to unauthorized access. This makes testing the strength of JWT secrets essential for ensuring the security of the authentication mechanism.


## Lab

The lab involved testing a simple web app that issues and validates JWTs for user authentication. The application consisted of two main routes: `/login` for receiving user credentials and issuing a token, and `/dashboard` for validating the JWT and granting access to a protected resource.

The login route was designed to accept `POST` requests with a `username` and `password` in the request body. Upon successful authentication, a JWT is generated using the `jsonwebtoken` library and returned to the user. 

```bash
curl -X POST http://localhost/login --header "Content-Type: application/json" --data '{"username": "user", "password": "user"}'

```

Once the valid token was obtained, it was tested by sending a `GET` request to the `/dashboard` route, passing the token in the `Authorization` header. This route performed a token validation check by decoding the JWT using the same secret key. If the token was valid, the server granted access to the dashboard and returned a personalized message, confirming the validity of the session.

```bash
curl -i http://localhost/dashboard --header "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiJ1c2VyIiwiaWF0IjoxNzM5MjE2MDE3fQ.tEx3iyh51cmJm5DlzMeJrblmle_t2uJOQNaIUMxtrpE"
```

The use of JWTs for both authentication and authorization was validated, demonstrating a typical flow where the server relies on the client to provide the token for subsequent requests.

![alt text](assets/image-36.png)

---

#### Cracking the application secret

To demonstrate how to crack the JWT secret, we can use Hashcat to brute force the token's signature. Given that the secret used for signing the token (`ucyxu6`) is weak and has low entropy, it was cracked quickly.

```bash
./hashcat.bin -a 0 -m 16500 hashes/jwt.token ../wordlists/rockyou.txt
```

![alt text](assets/image-37.png)

---

#### Forging an admin token

With the secret in hand, the next step was to forge a valid admin token. Using [jwt.io](https://jwt.io), the payload and header were crafted manually with the admin user’s details.

![alt text](assets/image-38.png)

This newly forged token was then used to authenticate against the app, providing access to the dashboard as an admin. The visual evidence shows the application responding with a successful authentication.

![alt text](assets/image-39.png)

The critical point here is that using a weak, low-entropy secret like `ucyxu6` makes it extremely vulnerable to offline cracking. Once the secret is known, it becomes trivial to forge valid tokens for any user, bypassing authentication altogether.
