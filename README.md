# What is an API?

#### An application programming interface is a connection between computers or between computer programs. It is a type of software interface, offering a service to other pieces of software. A document or standard that describes how to build such a connection or interface is called an API specification. A computer system that meets this standard is said to implement or expose an API. 

<img width="396" height="338" alt="image-0" src="https://github.com/user-attachments/assets/80862cd4-7d8c-458c-97e2-e1cedd8f5ab8" />

# API protocols and architectures

### REST

REST (Representational State Transfer) is a software architectural style that was created to describe the design and guide the development of the architecture for the World Wide Web. REST defines a set of constraints for how the architecture of a distributed, Internet-scale hypermedia system, such as the Web, should behave.

The REST architectural style emphasises uniform interfaces, independent deployment of components, the scalability of interactions between them, and creating a layered architecture to promote caching to reduce user-perceived latency, enforce security, and encapsulate legacy systems.

- Client-Server architecture
- Statelessness
- Cacheability
- Layered system
- Use of HTTP methods (GET, POST, etc)
- Use of URIs to identify resources

#### RPC

The remote procedural call (RPC) protocol is a simple means to send multiple parameters and receive results. RPC APIs invoke executable actions or processes, while REST APIs mainly exchange data or resources such as documents. RPC can employ two different languages, JSON and XML, for coding; these APIs are dubbed JSON-RPC and XML-RPC, respectively.

#### SOAP

The simple object access protocol (SOAP) is a messaging standard defined by the World Wide Web Consortium and broadly used to create web APIs, usually with XML. SOAP supports a wide range of communication protocols found across the internet, such as HTTP, SMTP and TCP/IP. SOAP is also extensible and style-independent, which enables developers to write SOAP APIs in varied ways and easily add features and functionality. The SOAP approach defines how the SOAP message is processed, the features and modules included, the communication protocol(s) supported and the construction of SOAP messages.

Compared with the flexibility of REST, SOAP is a highly structured, tightly controlled and clearly defined standard. For example, SOAP messages can contain up to four components, including an envelope, header, body and fault -- the latter used for error handling.

# Types of web APIs

#### Open / Public APIs

Open or public APIs are available for external developers or third parties. These APIs are typically shared freely and publicly to encourage external users (developers) to integrate with their systems. 

They are often used to provide access to a service or data, such as social media platforms offering APIs for posting content or retrieving user data. These APIs often have some level of authentication and access control, but their primary goal is to allow public access.

#### Partner APIs

A partner API, only available to specifically selected and authorized outside developers or API consumers, is a means to facilitate business-to-business activities. For example, if a business wants to selectively share its customer data with outside CRM firms, a partner API can connect the internal customer data system with those external parties -- no other API use is permitted.

Partners have clear rights and licenses to access such APIs. For this reason, partner APIs generally incorporate stronger authentication, authorization and security mechanisms. Enterprises also typically do not monetize such APIs directly; partners are paid for their services rather than through API use.

#### Internal APIs

An internal or private API is intended only for use within the enterprise to connect systems and data within the business. For example, an internal API might connect an organization's payroll and HR systems.

Internal APIs traditionally present weak security and authentication -- or none at all -- because the APIs are intended for internal use, and such security levels are assumed to be in place through other policies. This is changing, however, as greater threat awareness and regulatory compliance demands increasingly influence an organization's API strategy.

#### Composite APIs

Composite APIs generally combine two or more APIs to craft a sequence of related or interdependent operations. Composite APIs can be beneficial to address complex or tightly related API behaviors and can sometimes improve speed and performance over individual APIs.

# API Security

- https://www.ibm.com/think/topics/api-security

API security refers to the practices and procedures that protect application programming interfaces (APIs) from misuse, malicious bot attacks and other cybersecurity threats. It functions as a subset of web security but with a specific focus on APIs, which are increasingly vital to enterprise IT management.

If not properly secured, API endpoints can allow malicious actors to gain unauthorized access to sensitive data, disrupt service operations, or both, with potentially devastating consequences. Common threats include:

- Authentication-based attacks—where hackers try to guess or steal user passwords or use weak authentication mechanisms to gain access to API servers.

- Man-in-the-middle attacks—where a bad actor steals or modifies data (for example, login credentials or payment information) by intercepting API requests or responses.

- Code injections/injection attacks—where the hacker transmits a harmful script (to insert false information, delete or reveal data, or disrupt app functionality) through an API request, displaying weaknesses in the API interpreters that read and translate data.

- Security misconfiguration—where sensitive user information or system details are exposed due to inadequate default configurations, overly permissive cross-origin resource sharing (CORS) or incorrect HTTP headers.

- Denial-of-service (DoS) attack—these attacks send scores of API requests to crash or slow down the server. DoS attacks can often come from multiple attackers simultaneously in what is called a distributed denial-of-service (DDoS) attack.

- Broken object level authorization (BOLA) attacks—occur when cybercriminals manipulate object identifiers at API endpoints to widen the attack surface and gain unauthorized access to user data. BOLA attacks are especially common, because implementing proper object-level authorization checks can be difficult and time-consuming.

