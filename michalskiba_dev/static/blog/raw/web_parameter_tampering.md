[start title]

Web Parameter Tampering: Simple, but very serious security risk

[end title]

[start tags]

wpt, web_parameter_tampering, demo, web_attack, web_attack_prevention 

[end tags]

[start lead]

In 2021 OWASP placed "Broken Access Control" at first place amongst Top 10 Web Application Security Risks ([link](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)). Web Parameter Tampering is just one type of web attack that falls into this group. Even if it seems simple, and you think that"only junior can introduce such threat to web application", you should still be aware of this attack. As the OWASP ranking shows, a lot of developers think like that and hackers will be happy to exploit it.

[end lead]

[start content]

# What is Web Parameter Tampering

Web Parameter Tampering is a type of web-based cyberattack in which certain parameters in a request sent to server are changed in a way that is not expected by the server. Vulnerable site may expose confidential information to user that normally should not have the access to the given resources. Such user can obtain it by simply changing url path or query/body parameters.

# Introduction to demo scenario

Let's leave theory behind and get our hands on real live example. Imagine a site for an imaginary music festival that allows press organizations to apply for press accreditation and then check the status of it. In correctly implemented site, press organization member, after logging in to the press portal, should see theirs application. It should not change after modifying url path or query parameters.

The whole code for the Web Parameter Tampering demo, which is Django app, can be found in public [repository](https://github.com/dev-michal-skiba/michalskiba-dev/tree/master/michalskiba_dev/web_parameter_tampering) on GitHub.

# Exploiting Web Parameter Tampering vulnerability

Going to the demo site [https://wpt.michalskiba.dev/](https://wpt.michalskiba.dev/), by default you will start with secure version off. You can access press portal either as a victim (username: *victim*, password: *Victim1234!*) or a hacker (username: *hacker*, password: *Hacker1234!*). No matter as who you are logged in, you will see the page with press application: approved for the victim with the accreditation number and waiting application for the hacker.

![wpt_1.png](..%2Fimages%2Fweb_parameter_tampering%2F1.png)
![wpt_2.png](..%2Fimages%2Fweb_parameter_tampering%2F2.png)
![wpt_3.png](..%2Fimages%2Fweb_parameter_tampering%2F3.png)

You can also notice that urls for the victim and hacker look as follows: [http://wpt.michalskiba.dev/press/2](http://wpt.michalskiba.dev/press/2) and [http://wpt.michalskiba.dev/press/1](http://wpt.michalskiba.dev/press/1). As you can easily guess, the number in the url represents the user's primary key from the database. **That is huge security threat**. It implies that basically anyone can try different user's primary keys and try to steal accreditation of the other press organization. If you are logged in as the hacker, you can change "1" in url to "2" which will result in obtaining press application from the victim!. If you log out and try the same url [http://wpt.michalskiba.dev/press/2](http://wpt.michalskiba.dev/press/2), you will be redirected to the home page of the demo site. That is the issue for many broken access controls vulnerabilities. User can get any confidential resource based on being authenticated without authorizing user for a given resource.

# Example of correctly applied access control

When you set security to be on, and you log in, you will see that user primary key disappears from the url. That is how it should be. User can only see the press application that belongs to them. Server authorize that based on user information safely encrypted in `auth_token` cookie. Potential hacker cannot decrypt, modify and change the value of the cookie without the secret that is stored securely on the server. There is no room for tampering the request data.

# Conclusion

Although, the given demo presents tampering the GET method parameters, the same may apply for changing url path and body/query parameters in POST, PUT, PATCH and DELETE methods. The idea is the same: the hacker can easily manipulate parameters sent in either of the methods which result in unexpected behaviour from the server. Always make sure that parameters that can be modified by user are not raising any threat.

I hope that I explained Web Parameter Tampering clearly and that despite it being simple web attack, you will stay on guard and will always have in mind to design web applications in such way that access to the resource is limited only to the resource's owner.

[end content]