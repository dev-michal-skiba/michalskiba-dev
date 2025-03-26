---
title: "Web Parameter Tampering: Simple, but very serious security risk"
lead: 'In 2021 OWASP placed "Broken Access Control" at first place amongst Top 10 Web Application Security Risks. Web Parameter Tampering is just one type of web attack that falls into this group. Even if it seems simple, and you think that "only junior can introduce such threat to web application", you should still be aware of this attack. As the OWASP ranking shows, a lot of developers think like that and hackers will be happy to exploit it.'
draft: false
type: "blog"
layout: "post"
---

## What is Web Parameter Tampering

Web Parameter Tampering is a type of web-based cyberattack in which certain parameters in a request sent to server are changed in a way that is not expected by the server. Vulnerable site may expose confidential information to user that normally should not have the access to the given resources. Such user can obtain it by simply changing url path or query/body parameters.

## Introduction to demo scenario

Let's leave theory behind and get our hands on real live example. Imagine a site for an imaginary music festival that allows press organizations to apply for press accreditation and then check the status of it. In correctly implemented site, press organization member, after logging in to the press portal, should see theirs application. It should not change after modifying url path or query/body parameters.

## Exploiting Web Parameter Tampering vulnerability

Go to the [demo site](/demos/web-parameter-tampering/press/), by default you will start with secure version on. Please log in to press portal either as a victim (username: *victim*, password: *Victim1234!*) or a hacker (username: *hacker*, password: *Hacker1234!*). No matter as who you are logged in, you will see the page with press application: approved for the victim with the accreditation number and waiting application for the hacker.

Please notice, in the network tab of the browser developer tools, that in secure version of the demo site, the request does not contain any user identifier in GET url. When you switch security off, you will see that the username is present in the url. **That is huge security threat**. It implies that basically anyone can try different user's names and try to steal accreditation of the other press organization.

You can try to change the url query parameter to see others' press applications. For example, if you are logged in as a hacker, you can intercept the request using a tool like Burp Suite, Fiddler, or Charles Proxy, and change the url query parameter to `username=victim` to see the victim's press application. You can also copy the request as cURL in the network tab and then paste the cURL in the terminal or in a tool like Postman, modify the url query parameter and send the request. For the ease of the demo scenario you can also modify the local storage variable `wptUsername` to tamper the username sent to API.

## Example of correctly applied access control

When you set security to be on, and you log in, you will see that username disappears from the url. That is how it should be. User can only see the press application that belongs to them. Server authorize that based on user information safely stored in JWT token in `auth_token` http cookie. Cookie cannot be accessed and changed from javascript code. JWT Token is also securely signed and verified on backend, so it is impossible to correctly tamper the username on the JWT token.

## Conclusion

Although, the given demo presents tampering the GET method parameters, the same may apply for changing url path and body/query parameters in POST, PUT, PATCH and DELETE methods. The idea is the same: the hacker can easily manipulate parameters sent in either of the methods which result in unexpected behaviour from the server. Always make sure that parameters that can be modified by user are not raising any threat. I hope that I explained Web Parameter Tampering clearly and that  despite it being simple web attack, you will stay on guard and will always have in mind to  design web applications in such way that access to the resource is limited only to the  resource's owner.
