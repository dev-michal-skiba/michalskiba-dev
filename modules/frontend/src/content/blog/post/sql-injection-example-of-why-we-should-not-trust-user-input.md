---
title: "SQL Injection: Example of why we should not trust user input"
lead: "In the digital age, where data fuels our everyday transactions and interactions, the
security of our databases stands as one of the main concerns. SQL Injection, common and vicious
attack vector, exemplifies the critical importance of guarding databases against potential bad
actors. The attack may result in a breach or loss of data, so that is why we should take a
close look at this attack."
draft: false
type: "blog"
layout: "post"
---

## What is SQL Injection

If you want the detailed definition please see
[OWASP definition](https://owasp.org/www-community/attacks/SQL_Injection).
It is a well known attack and I couldn't add more. I focus more on the practical examples and
that is why I will give you a short example to understand how it works. Imagine this SQL query
`SELECT * FROM table WHERE name='%{name}%'`. Imagine also that we store it as a normal 
text, and we replace the `{name}` with whatever is inputted by the user. Then we pass 
the query to the engine and display returned data to the user. At first glance it seems fine 
and until users will provide standard values it will be fine, but this implementation will 
result in SQL Injection vulnerability. Try to think what will happen if user inputs such value:
`abc'; DROP DATABASE databasename;--`. In our scenario it will result in the following query
`SELECT * FROM table WHERE name='%abc'; DROP DATABASE databasename;--%'`. Kaboom, your database is
removed. You can argue that user need to know database name, but further in the demonstration
section I will show you that it won't be the problem to find the database name.

## How to prevent SQL Injection attack

SQL Injection attack works when we pass SQL query built with user input as a normal text. This way 
whatever is inputted by the user is used to construct SQL query. This is a naive approach, because,
as shown in previous section, user can exploit that to completely modify the query. Modern database
engines provide a way to pass query and parameters independently, so we are always sure that
the value inputted by user will be treated as sql query parameter and not as part of the query. 
For example in PostgreSQL we can prepare parametrized statement that implements this solution. 
To make SQL query from previous section safe, in PostgreSQL we would need to write it in the 
following way: `PREPARE query_table_by_name (text) AS SELECT * FROM table WHERE name=%$1%`. 
User can input whatever, and we are always sure that it is treated only as a parameter. It 
cannot escape being a parameter and modify the query. Prevention is as simple as that. What's 
more, it is implemented in most of the modern frameworks or object-oriented mappings (ORMs). 
Anyway it is crucial to understand this attack, because there is always a way to execute raw 
SQL query (even with ORM) and sometimes it may be tempting to do so.

## Introduction to demo scenario

Let's leave theory behind and get our hands on real live example. Demonstration is available under
this address [sql-injection.michalskiba.dev](https://sql-injection.michalskiba.dev/). It is a
simple mockup site of fake carrier that provides user with view to search for parcel stores by 
address. The site itself is primitive, but what is most important it provides a way for user to 
input search query which is later used in SQL query to filter parcel stores. In the navbar you 
can also specify whether you want to use secure version of the application (with SQL Injection 
protection) or whether you want to use insecure version (without SQL Injection protection).

## Exploiting SQL Injection vulnerability

Please open demo site without SQL Injection protection. Let's try to recreate the reasoning 
and actions attacker performs when he wants to exploit potential SQL Injection vulnerability. 
Let's check that the search mechanism works by inputting `Warsaw`. It should display two parcel 
stores as expected. With knowledge we have from previous sections let's see whether form is 
vulnerable to SQL Injection by using `UNION` keyword. The idea behind it is that it should 
"union" two query results into one under two conditions: number of returned values must match 
and values in the same column of different tables must have the same type, unless it is `NULL` 
value. We will use this `NULL` value exception to check how many values are returned in the 
query. In the search output we can see three values per parcel store, so it is logical to 
conclude that query returns three values. Let's try `abc' UNION SELECT NULL, NULL, NULL;--` 
then. It does not work. Maybe some field is not displayed (many times also primary key is 
returned from query), so let's try it with one more `NULL` by inputting this `abc' UNION SELECT 
NULL, NULL, NULL, NULL;--`. Great (not great for fake carrier), that is working. We are now 
sure that site is really vulnerable.

![sql_injection_1.png](/post/sql_injection/1.png)

Now it may be useful to know on what database we are operating. Most of the modern database 
provides some kind of command to check it. Let's skip part of guessing and with the knowledge 
that this app is using postgres let's search for `abc' UNION SELECT NULL, version(), NULL, NULL;
--`.

![sql_injection_2.png](/post/sql_injection/2.png)
 
That is very useful information. In PostgreSQL table names are stored in the table called
`information_schema.tables`. We can search for all tables with this input
`abc' UNION SELECT NULL, table_name, NULL, NULL FROM information_schema.tables;--`.

![sql_injection_3.png](/post/sql_injection/3.png)

Once we find interesting table we can also display all columns on that table by selecting
values from `information_schema.columns` table. Let's check columns in parcel store table with
following input `abc' UNION SELECT NULL, column_name, NULL, NULL FROM information_schema.
columns WHERE table_name = 'sql_injection_parcelstore';--`.

![sql_injection_4.png](/post/sql_injection/4.png)

That is interesting, we found `access_code` column that is not shown in the search result.
Probably that is code that if provided will open locked doors of parcel store! (let's assume 
that such access code really exists and is stored on the same table for the sake of this 
example :D). Now all we need to do to get all access codes is to input this `abc' UNION SELECT 
NULL, name, address, access_code FROM sql_injection_parcelstore;--` and we now know all access 
codes with the exact locations of parcel stores.

![sql_injection_5.png](/post/sql_injection/5.png)

In real life scenario using SQL Injection you could also add data to the tables (for example 
users with admin privileges), drop tables or drop whole database, but because I expose this 
vulnerability online I validate the input, so only read queries are allowed. There is (hopefully)
no way of dropping the database. I also use different database for this demo than for other 
demos, so there is also no risk of breaking my other demo sites.

## Example of correctly implemented search mechanism

You can switch the site to the secure version and check all previous inputs that helped us to get
access codes. It won't work, because now SQL queries are parametrized. You can check out the
code that is responsible for querying in secure and insecure way in my
[open repository](https://github.com/dev-michal-skiba/michalskiba-dev/blob/master/michalskiba_dev/sql_injection/utils.py).
For secure querying I use Django ORM that parametrize the query under the hood. Using
framework recommended way of communicating with database is always the safest option. If we
are using bare language there are always ORMs available (for example SQLAlchemy 
fo Python) which should be used. Anyway, as you can see in the code, Django ORM allows 
executing bare SQL queries. It is not recommended, but you can do this. There is mechanism for 
parametrizing raw SQL queries in Django (see 
[docs](https://docs.djangoproject.com/en/5.0/topics/db/sql/#passing-parameters-into-raw)), but you
are not forced to use it. That is why developers should be aware of SQL Injection. Not knowing this
can result in introducing major vulnerabilities to the web applications.
