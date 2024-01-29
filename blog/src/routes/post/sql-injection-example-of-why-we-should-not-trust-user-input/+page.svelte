<h1>SQL Injection: Example of why we should not trust user input</h1>
<i>Published on 2024.01.28</i>
<br>
<br>
<p>
    In the digital age, where data fuels our everyday transactions and interactions, the security
    of our databases stands as one of the main concerns. SQL Injection, common and vicious attack
    vector, exemplifies the critical importance of guarding databases against potential bad actors.
    The attack may result in a breach or loss of data, so that is why we should take a close look
    at this attack.
</p>

<div class="toc_container">
    <p class="toc_title">Table of Contents</p>
    <ol class="toc_list">
    <li><a class="link" href="#what-is-sql-injection">What is SQL Injection</a></li>
    <li><a class="link" href="#how-to-prevent-sql-injection-attack">How to prevent SQL Injection attack</a></li>
    <li><a class="link" href="#introduction-to-demo-scenario">Introduction to demo scenario</a></li>
    <li><a class="link" href="#exploiting-sql-injection-vulnerability">Exploiting SQL Injection vulnerability</a></li>
    <li><a class="link" href="#example-of-correctly-implemented-search-mechanism">Example of correctly implemented search mechanism</a></li>
    <li><a class="link" href="#conclusion">Conclusion</a></li>
    </ol>
</div>

<h2 id="what-is-sql-injection">What is SQL Injection</h2>
<p>
    If you want the detailed definition please see <a class="link" href="https://owasp.org/www-community/attacks/SQL_Injection">OWASP definition</a>.
    It is a well known attack and I couldn't add more. I focus more on the practical examples and that
    is why I will give you a short example to understand how it works. Imagine this SQL query
    <code>SELECT * FROM table WHERE name='%{'{'}name{'}'}%'</code>. Imagine also that we store it as
    a normal text and we replace the <code>{'{'}name{'}'}</code> with whatever is inputed by the user.
    Then we pass the query to the engine and display returned data to the user. At first glance it 
    seems fine and until users will provide standard values it will be fine, but this implementation
    will result in SQL Injection vulnerability. Try to think what will happen if user inputs such value:
    <code>abc'; DROP DATABASE databasename;--</code>. In our scenario it will result in the following
    query <code>SELECT * FROM table WHERE name='%abc'; DROP DATABASE databasename;--%'</code>. Kaboom, your
    database is removed. You can argue that user need to know database name, but further in the demonstration
    section I will show you that it won't be the problem to find the database name.
</p>

<h2 id="how-to-prevent-sql-injection-attack">How to prevent SQL Injection attack</h2>
<p>
    SQL Injection attack works when we pass SQL query built with user input as a normal text. This way 
    whatever is inputed by the user is used to construct SQL query. This is a naive approach, because,
    as shown in previous section, user can exploit that to completely modify the query. Modern database
    engines provide a way to pass query and parameters independently, so we are always sure that the value
    inputed by user will be treated as sql query parameter and not as part of the query. For example in
    PostgreSQL we can prepare parametrized statement that implements this solution. To make SQL query from
    previous section safe, in PostgreSQL we would need to write it in the following way: <code>PREPARE
    query_table_by_name (text) AS SELECT * FROM table WHERE name=%$1%</code>. User can input whatever and we
    are always sure that it is treated only as a parameter. It cannot escape being a parameter and modify
    the query. Prevention is as simple as that. What's more, it is implemented in most of the modern
    frameworks or object oriented mappings (ORMs). Anyway it is crucial to understand this attack, because
    there is always a way to execute raw SQL query (even with ORM) and sometimes it may be tempting to do so.
</p>

<h2 id="introduction-to-demo-scenario">Introduction to demo scenario</h2>
<p>
    Let's leave theory behind and get our hands on real live example. Demontration is available under this
    address <a class="link" href="https://sql-injection.michalskiba.dev/">sql-injection.michalskiba.dev</a>.
    It is a simple mockup site of fake carrier that provides user with view to search for parcel stores
    by address. The site itself is primitive, but what is most important it provides a way for user to input
    search query which is later used in SQL query to filter parcel stores. In the navbar you can also specify
    whether you want to use secure version of the application (with SQL Injection protection) or whether
    you want to use insecure version (without SQL Injection protection).
</p>

<h2 id="exploiting-sql-injection-vulnerability">Exploiting SQL Injection vulnerability</h2>
<p>
    Please open demo site without SQL Injection protection. Let's try to recreate the reasoning and actions
    attacker performs when he wants to exploit potential SQL Injection vulnerability. Let's check that the
    search mechanism works by inputing <code>Warsaw</code>. It should display two parcel stores as expected.
    With knowledge we have from previous sections let's see whether form is vulnerble to SQL Injection by
    using <code>UNION</code> keyword. The idea behind it is that it should "union" two query results into
    one under two conditions: number of returned values must match and values in the same column of
    different tables must have the same type, unless it is <code>NULL</code> value. We will use this
    <code>NULL</code> value exception to check how many values are returned in the query. In the search
    output we can see three values per parcel store, so it is logical to conclude that query returns three values. Let's
    try <code>abc' UNION SELECT NULL, NULL, NULL;--</code> then. It does not work. Maybe some field is not
    displayed (many times also primary key is returned from query), so let's try it with one more
    <code>NULL</code> by inputing this <code>abc' UNION SELECT NULL, NULL, NULL, NULL;--</code>. Great (not
    great for fake carrier), that is working. We are now sure that site is really vulnerbale.
</p>
<img class="img-fluid post-img" src="1.png" alt="sql_injection_1.png">

<p>
    Now it may be useful to know on what database we are operating. Most of the modern database provides some
    kind of command to check it. Let's skip part of guessing and with the knowledge that this app is using
    postgres let's search for <code>abc' UNION SELECT NULL, version(), NULL, NULL;--</code>.
</p>
<img class="img-fluid post-img" src="2.png" alt="sql_injection_2.png">

<p>    
    That is very useful information. In PostgreSQL table names are stored in the table called
    <code>information_schema.tables</code>. We can search for all tables with this input
    <code>abc' UNION SELECT NULL, table_name, NULL, NULL FROM information_schema.tables;--</code>.
</p>
<img class="img-fluid post-img" src="3.png" alt="sql_injection_3.png">

<p>
    Once we find interesting table we can also display all columns on that table by selecting values from
    <code>information_schema.columns</code> table. Let's check columns in parcel store table with
    following input <code>abc' UNION SELECT NULL, column_name, NULL, NULL FROM 
    information_schema.columns WHERE table_name = 'sql_injection_parcelstore';--</code>.
</p>
<img class="img-fluid post-img" src="4.png" alt="sql_injection_4.png">

<p>
    That is interesting, we found <code>access_code</code> column that is not shown in the search result.
    Probably that is code that if provided will open locked doors of parcel store! (let's assume that such
    access code really exists and is stored on the same table for the sake of this example :D). Now all we
    need to do to get all access codes is to input this <code>abc' UNION SELECT NULL, name, address,
    access_code FROM sql_injection_parcelstore;--</code> and we now know all access codes with the exact
    locations of parcel stores.
</p>
<img class="img-fluid post-img" src="5.png" alt="sql_injection_5.png">

<p>
    In real life scenario using SQL Injection you could also add data to the tables (for example users with
    admin privileges), drop tables or drop whole database, but because I expose this vulnerbility online I
    validate the input, so only read queries are allowed. There is (hopefully) no way of dropping the database.
    I also use different database for this demo than for other demos, so there is also no risk of breking my
    other demo sites.
</p>

<h2 id="example-of-correctly-implemented-search-mechanism">Example of correctly implemented search mechanism</h2>
<p>
    You can switch the site to the secure version and check all previous inputs that helped us to get access codes.
    It won't work, because now SQL queries are parametrized. You can checkout the code that is responsible for
    querying in secure and insecure way in my <a class="link"
    href="https://github.com/dev-michal-skiba/michalskiba-dev/blob/master/michalskiba_dev/sql_injection/utils.py">
    open repository</a>. For secure querying I use Django ORM that parametrize the query under the hood. Using
    framework recommended way of communicating with database is always the safest option. If we are using bare language there are
    always ORMs available (for example SQLAlchemy fo Python) which should be used. Anyway, as you can see in the code,
    Django ORM allows executing bare SQL queries. It is not recommended, but you can do this. There is mechanism
    for parametrizing raw SQL queries in Django (see <a class="link" href="https://docs.djangoproject.com/en/5.0/topics/db/sql/#passing-parameters-into-raw">docs</a>), but you are not forced to
    use it. That is why developers should be aware of SQL Injection. Not knowing this can result in
    introducing major vulnerabilities to the web applications. 
</p>
