/** @type {import('./$types').PageLoad} */
export function load({ params }) {
    return {
        posts: [
            {
                "title": "SQL Injection: Example of why we should not trust user input",
                "slug": "sql-injection-example-of-why-we-should-not-trust-user-input",
                "lead": "In the digital age, where data fuels our everyday transactions and interactions, the security of our databases stands as one of the main concerns.SQL Injection, common and vicious attack vector, exemplifies the critical importance of guarding databases against potential bad actors. The attack may result in a breach or loss of data, so that is why we should take a close look at this attack.",
            },
            {
                "title": "Web Parameter Tampering: Simple, but very serious security risk",
                "slug": "web-parameter-tampering-simple-but-very-serious-security-risk",
                "lead": "In 2021 OWASP placed \"Broken Access Control\" at first place amongst Top 10 Web Application Security Risks (<a class=\"link\" href=\"https://owasp.org/Top10/A01_2021-Broken_Access_Control/\">link</a>). Web Parameter Tampering is just one type of web attack that falls into this group. Even if it seems simple, and you think that\"only junior can introduce such threat to web application\", you should still be aware of this attack. As the OWASP ranking shows, a lot of developers think like that and hackers will be happy to exploit it.",
            },
        ]
    };
    
}