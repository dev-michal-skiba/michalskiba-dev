---
title: "Host Header Injection: Don't trust request headers"
lead: "In the realm of web security, Host Header Injection (HHI) is a subtle yet potent vulnerability that can compromise the integrity of web applications. This vulnerability arises when an application implicitly trusts the Host header in HTTP requests without adequate validation, allowing attackers to manipulate server behavior, potentially redirecting users to malicious sites or intercepting sensitive data. This blog post primarily focuses on demonstrating this vulnerability through the demo application. By understanding the mechanics and impact of HHI, developers can fortify their applications against such threats."
draft: false
type: "blog"
layout: "post"
---

## What is Host Header Injection?

Host Header Injection (HHI) is a security vulnerability that occurs when an application implicitly trusts the Host header in HTTP requests without proper validation. This vulnerability can be exploited by attackers to manipulate server behavior in several ways. For instance, attackers can craft requests with a malicious Host header to redirect users to fraudulent sites, intercept sensitive data, or even conduct cache poisoning attacks.

In a typical HTTP request, the Host header specifies the domain name of the server to which the request is being sent. However, if an application uses this header to construct URLs or make security decisions without verifying its authenticity, it opens the door to potential exploitation. Attackers can alter the Host header to trick the server into generating links or responses that point to a malicious domain.

The impact of HHI can be severe, especially in applications that rely on the Host header for generating password reset links, constructing absolute URLs, or performing access control checks. By understanding and addressing this vulnerability, developers can prevent attackers from exploiting these weaknesses and ensure the security and integrity of their applications.

## The Vulnerability in Password Reset

In many applications, the password reset process involves sending a reset link to the user's email. The demo application features a password reset form where users can provide their email address to receive a reset link. However, if the application constructs this link using the Host header, it becomes vulnerable to manipulation.

Imagine an attacker who knows that a victim has an account on this service and is aware of the victim's email address. The attacker can input the victim's email into the password reset form and manipulate the Host header so that the password reset URL is created using a malicious host. When the victim receives the email and clicks on the reset link, they are redirected to a malicious site.

The reset link might look like this:

`<a href="http://malicious.com/reset?token=abc123">Reset your password</a>`

In this scenario, the token to reset the password is included in the query parameters. The malicious site can log this token and use it to change the victim's password, effectively compromising the victim's account.

The demo application includes a "secure version" checkbox, allowing users to toggle between a secure and insecure version of the password reset form. This feature demonstrates how proper validation and construction of URLs can prevent such attacks.

## Demonstration

The demo application provides a hands-on experience of both insecure and secure methods for handling password reset links. By toggling the "secure version" checkbox in the upper right corner of the demo interface, you can observe the differences in behavior. Explore the demo and see these scenarios in action at the [Host Header Injection Demo](/demos/host-header-injection/password-reset/initiate/)

### Insecure Scenario

1. Input Victim's Email: In the demo, you can input any email address into the password reset form. Note that no actual email is sent; instead, a modal is shown with the "email" content.

2. Intercept the Request: Use a tool like [Burp Suite](https://portswigger.net/burp) to intercept the HTTP request. This allows you to view and modify the request headers.

3. Modify the X-Forwarded-Host Header: Change the `X-Forwarded-Host` header to a malicious domain of your choice. In some web applications, especially those behind reverse proxies or load balancers, the `X-Forwarded-Host` header is used instead of the `Host` header. This is because the `Host` header typically contains the hostname of the proxy or load balancer, rather than the original hostname requested by the client. Using `X-Forwarded-Host` allows the backend server to reconstruct the original request context, which is crucial for generating URLs or performing routing based on the original host.

4. Check the Link: Observe that the link in the "email" points to the malicious site and includes the password reset token as a query parameter.

5. Exploit the Vulnerability: The attacker can use the token from the query parameter and append the proper host to change the victim's password, effectively compromising the account. Additionally, the server may log and store each token in a database, which the attacker can exploit to automate or repeat the attack.

### Secure Scenario

1. As in the insecure scenario, input any email address into the password reset form.

2. Again, use a tool like Burp Suite to intercept the HTTP request.

3. Even if you change the `X-Forwarded-Host` header, the link generation process is unaffected.

4. The link is generated based on an environment variable on the server, not the Host header. This ensures that the link always points to the legitimate site, preventing redirection to a malicious domain.

## Mitigation Strategies

To protect against Host Header Injection, developers should:

1. **Validate Host Headers**: Ensure that the Host header matches a whitelist of allowed domains.
2. **Use Absolute URLs**: Construct URLs using absolute paths rather than relying on the Host header.
3. **Use Environment Variables**: Construct URLs using environment variables to define the base URL, ensuring that the link always points to the legitimate site.

## Conclusion

Host Header Injection is a critical vulnerability that can undermine the security of password reset mechanisms. By understanding and addressing this threat, developers can enhance the security posture of their applications, safeguarding user data and maintaining trust.
