# Intro

Authorization is a critical security mechanism in APIs that determines __what actions__ a user or system can perform after authentication. It ensures that users only access the resources and operations they are permitted to. Weak or improper authorization can lead to __privilege escalation, data leaks, and unauthorized actions__ — making it a prime target for web/API hackers.  

<img width="2400" height="1350" alt="image-13" src="https://github.com/user-attachments/assets/b69c934e-cb86-4a37-b26e-102ddd1586e0" />

---
#### Authorization vs. Authentication

__Authentication__ is the process of verifying __who__ a user is. It typically involves checking credentials like usernames and passwords, tokens (e.g., JWT, OAuth), or biometric data. Authentication ensures that users are who they claim to be before granting access to a system. Common issues related to authentication include weak passwords, vulnerability to brute-force attacks, token theft, and session hijacking, all of which can compromise security.

__Authorization__, on the other hand, determines __what__ an authenticated user is allowed to do within a system. After authentication, authorization mechanisms define access controls such as read/write permissions or admin rights. Common problems with authorization include Insecure Direct Object References (IDOR), where users can access resources they shouldn't, privilege escalation, and broken access controls that allow unauthorized actions, leading to potential security breaches.


# BOLA

Broken object level authorization (BOLA) arises when an API fails to enforce proper permissions for individual objects within its endpoints. BOLA allows attackers to manipulate object identifiers (such as IDs) to access or modify resources they shouldn’t have access to. This is typically due to missing or inadequate authorization checks for specific object references at the API level.

For instance, an e-commerce API may permit an attacker to fetch or alter sensitive data, such as customers' postal addresses, by replacing an object ID in the request URL or payload for an "orders" endpoint. BOLA can lead to unauthorized access, data manipulation, and even deletion of critical resources.

__Threat agents/Attack vectors__: Attackers can exploit API endpoints that are vulnerable to broken object-level authorization by manipulating the ID of an object that is sent within the request. Object IDs can be anything from sequential integers, UUIDs, or generic strings. Regardless of the data type, they are easy to identify in the request target (path or query string parameters), request headers, or even as part of the request payload.

__Security Weakness__: This issue is extremely common in API-based applications because the server component usually does not fully track the client’s state, and instead, relies more on parameters like object IDs, that are sent from the client to decide which objects to access. The server response is usually enough to understand whether the request was successful.

__Impacts__: Unauthorized access to other users’ objects can result in data disclosure to unauthorized parties, data loss, or data manipulation. Under certain circumstances, unauthorized access to objects can also lead to full account takeover.

## Lab

- https://github.com/owasp/crAPI

Upon signing up for an account on crAPI, the application sends a confirmation email via MailHog with details about a newly purchased vehicle, including a VIN code and a PIN code.

<img width="914" height="340" alt="image-22" src="https://github.com/user-attachments/assets/a23dac9d-b939-45db-87c0-db14bb274f52" />

### `/identity/api/v2/vehicle/$ID/location`

After adding the vehicle information to the dashboard, the application displays additional details about the car, along with a Google Maps snippet showing the current location of the vehicle and a "Refresh Location" button. 

The API response includes the `carId`, GPS coordinates of the vehicle, as well as the vehicle owner's name and email.

<img width="1919" height="1078" alt="image-15" src="https://github.com/user-attachments/assets/d15db9cf-7dbb-4cd0-8f2d-6bed3cf52f76" />

The `/forum` page displays three posts from users: Robot, Pogba, and Adam. Inspecting the response from `/community/api/v2/post/recent` reveals an example of __API3: Excessive Data Exposure__, which discloses unnecessary details about the authors of the forum posts.


Using __cURL__ and __jq__, the `vehicleId` can be extracted from the response and utilized to retrieve further information associated with the vehicles.

<img width="1681" height="306" alt="image-17" src="https://github.com/user-attachments/assets/ccd111f5-a741-418b-87d4-e51fb71e5da6" />
<img width="1741" height="908" alt="image-18" src="https://github.com/user-attachments/assets/dd6e6d63-e380-47c3-9d5b-694d5b93617f" />

### `/workshop/api/merchant/contact_mechanic`

The `contact_mechanic` API call returns a `report_link` object that provides status updates on the car.

```json
{
    "response_from_mechanic_api": {
        "id": 36,
        "sent": true,
        "report_link": "http://localhost:8888/workshop/api/mechanic/mechanic_report?report_id=36"
    }
}
```

<img width="1875" height="641" alt="image-19" src="https://github.com/user-attachments/assets/96a7cf99-c2c8-42b2-8e90-90823ff13a18" />

The __BOLA (Broken Object Level Authorization)__ vulnerability in this case allows access to reports from other users, even when the JWT does not match the owner of the vehicle for the `report_id`. 

By fuzzing a sequence of numbers against the API call, it's possible to identify other user reports.

<img width="1689" height="838" alt="image-20" src="https://github.com/user-attachments/assets/8ef10734-b1db-4292-ba99-7fe026c94a26" />

Once valid `report_id`s are located, __cURL__ can be used to extract the associated information, revealing further details about users and their vehicles.

<img width="1920" height="432" alt="image-21" src="https://github.com/user-attachments/assets/350f72f4-dc2b-4ed6-87ba-e7512c5e95c8" />


# BFLA

Broken function level authorization occurs when APIs fail to enforce adequate authorization checks, allowing attackers to access or manipulate sensitive functions or data they are not authorized to. This vulnerability is common in systems where the security mechanisms depend heavily on URL paths or inconsistent role verification.

Attackers often exploit these vulnerabilities by guessing API endpoints, manipulating HTTP methods, or modifying parameters to perform unauthorized actions. Examples include accessing administrative APIs as a regular user or using a public API to perform sensitive operations like deleting data or escalating privileges.


__Threat agents/Attack vectors__: Exploitation requires the attacker to send legitimate API calls to an API endpoint that they should not have access to as anonymous users or regular, non-privileged users. Exposed endpoints will be easily exploited.

__Security Weakness__: Authorization checks for a function or resource are usually managed via configuration or code level. Implementing proper checks can be a confusing task since modern applications can contain many types of roles, groups, and complex user hierarchies (e.g. sub-users, or users with more than one role). It's easier to discover these flaws in APIs since APIs are more structured, and accessing different functions is more predictable.

__Impacts__: Such flaws allow attackers to access unauthorized functionality. Administrative functions are key targets for this type of attack and may lead to data disclosure, data loss, or data corruption. Ultimately, it may lead to service disruption.

## Lab

- https://github.com/roottusk/vapi

The application provides an endpoint for user registration, allowing users to create an account by submitting their details in a JSON request. However, a hint suggests that additional, potentially hidden functionality may exist, particularly related to administrator authentication via a different route.

<img width="1920" height="1080" alt="image-23" src="https://github.com/user-attachments/assets/daca97b5-7709-4c49-b33d-bab6adacc6c9" />

Due to insufficient authorization mechanisms, unauthorized users can query the `/vapi/api5/users` endpoint and retrieve user information beyond their intended scope. 

This flaw enables attackers to enumerate existing users, gaining access to sensitive details without appropriate authentication checks. The absence of __role-based access control (RBAC)__ further exposes user data, potentially leading to privilege escalation and unauthorized access to administrative functions.


<img width="1479" height="659" alt="image-24" src="https://github.com/user-attachments/assets/c4777f61-5768-4c5b-a6cf-38ad660581c5" />

### [Challenge 7](https://owasp.org/crAPI/docs/challenges.html#challenge-7---delete-a-video-of-another-user) --- Delete a video of another user

In _crAPI_, attempting to delete a user video via `/identity/api/v2/user/videos/{{video_id}}` results in a _403 Forbidden error_, indicating that the operation is restricted to administrators.  

```json
{
    "message": "This is an admin function. Try to access the admin API",
    "status": 403
}
```


However, an alternative endpoint, `/identity/api/v2/admin/videos/{{video_id}}`, lacks proper authorization checks. This allows attackers to delete any user's video by exploiting the API, effectively bypassing user-level restrictions and undermining the security model.

<img width="1477" height="626" alt="image-25" src="https://github.com/user-attachments/assets/85c3e134-96aa-45b2-a7ec-20fd59014c50" />

