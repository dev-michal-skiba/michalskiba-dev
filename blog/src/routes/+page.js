/** @type {import('./$types').PageLoad} */
export function load({ params }) {
    return {
        posts: [
            {
                "title": "Web Parameter Tampering: Simple, but very serious security risk",
                "slug": "web-parameter-tampering-simple-but-very-serious-security-risk",
                "release_date": "2023.08.03",
                "lead": "In 2021 OWASP placed \"Broken Access Control\" at first place amongst Top 10 Web Application Security Risks (<a class=\"link\" target=\"_blank\" href=\"https://owasp.org/Top10/A01_2021-Broken_Access_Control/\">link</a>). Web Parameter Tampering is just one type of web attack that falls into this group. Even if it seems simple, and you think that\"only junior can introduce such threat to web application\", you should still be aware of this attack. As the OWASP ranking shows, a lot of developers think like that and hackers will be happy to exploit it.",
            },
        ]
    };
    
}