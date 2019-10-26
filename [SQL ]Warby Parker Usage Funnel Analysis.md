# Warby Parker Marketing Analysis

## Date: October 25 2019

Warby Parker is a transformative lifestyle brand with a lofty objective: to offer designer eyewear at a revolutionary price while leading the way for socially conscious businesses. Founded in 2010 and named after two characters in an early Jack Kerouac journal, Warby Parker believes in creative thinking, smart design, and doing good in the world — for every pair of eyeglasses and sunglasses sold, a pair is distributed to someone in need.

In this project, we will analyze different Warby Parker’s marketing funnels in order to calculate conversion rates. Here are the funnels and the tables that we are given:
### Quiz Funnel:
- Survey
### Home Try-On Funnel:
- quiz
- home_try_on
- purchase

*please note: this is fictional data provided by Warby Parker*

To help users find their perfect frame, Warby Parker has a Style Quiz that has the following questions:

“What are you looking for?”
“What’s your fit?”
“Which shapes do you like?”
“Which colors do you like?”
“When was your last eye exam?”

Let's first look at our data: 
```sql
SELECT * 
FROM survey
LIMIT 10;
```

Next, we want to understand how users move through the funnel:
```sql
SELECT question, COUNT(DISTINCT user_id)
FROM survey
GROUP BY question;
```

1. What are you looking for?	500
2. What's your fit?	475
3. Which shapes do you like?	380
4. Which colors do you like?	361
5. When was your last eye exam?	270

That's helpful, let's look at conversion rates in %:
Questions	Conversion Rate from the previous step
1.	100
2.	95.00%
3.	80.00%
4.	95.00%
5.	74.79%

Takeaway: question 3 and 5 have the lowest completion rates.
The reason may be that 3 is too broad, and 5 goes off the assumption that the user has had eye exams in the past. 

**We're now going to join the other two tables that will allow us to understands which users went from the survey to home try on program, how many pairs they tried, and which purchased.**

First, we will create the following query: 
- Each row will represent a single user from the browse table:
- If the user has any entries in home_try_on, then is_home_try_on will be ‘True’.
number_of_pairs comes from home_try_on table
- If the user has any entries in is_purchase, then is_purchase will be ‘True’.

```sql
SELECT q.user_id ,
CASE WHEN h.user_id IS NOT NULL THEN 'True' ELSE 'False' END AS 'is_home_try_on',
h.number_of_pairs, 
CASE WHEN p.user_id IS NOT NULL THEN 'True' ELSE 'False' END AS 'is_purchase'
FROM quiz AS q
LEFT JOIN home_try_on AS h ON
q.user_id = h.user_id
LEFT JOIN purchase AS p ON
q.user_id = p.user_id
LIMIT 10;
```

Output:

| user_id                              | is_home_try_on | number_of_pairs | is_purchase |
|--------------------------------------|----------------|-----------------|-------------|
| 4e8118dc-bb3d-49bf-85fc-cca8d83232ac | True           | 3 pairs         | False       |
| 291f1cca-e507-48be-b063-002b14906468 | True           | 3 pairs         | True        |
| 75122300-0736-4087-b6d8-c0c5373a1a04 | False          |                 | False       |
| 75bc6ebd-40cd-4e1d-a301-27ddd93b12e2 | True           | 5 pairs         | False       |
| ce965c4d-7a2b-4db6-9847-601747fa7812 | True           | 3 pairs         | True        |
| 28867d12-27a6-4e6a-a5fb-8bb5440117ae | True           | 5 pairs         | True        |
| 5a7a7e13-fbcf-46e4-9093-79799649d6c5 | False          |                 | False       |
| 0143cb8b-bb81-4916-9750-ce956c9f9bd9 | False          |                 | False       |
| a4ccc1b3-cbb6-449c-b7a5-03af42c97433 | True           | 5 pairs         | False       |
| b1dded76-cd60-4222-82cb-f6d464104298 | True           | 3 pairs         | False       |

Once we have the data in this format, we can analyze it in several ways:

1. We can calculate overall conversion rates by aggregating across all rows.
2. We can compare conversion from quiz→home_try_on and home_try_on→purchase.
3. We can calculate the difference in purchase rates between customers who had 3 number_of_pairs with ones who had 5.

```SQL
WITH funnel AS (SELECT q.user_id ,
  CASE 
    WHEN h.user_id IS NOT NULL THEN '1'
    ELSE '0' END AS 'is_home_try_on',
h.number_of_pairs, 
  CASE 
    WHEN p.user_id IS NOT NULL THEN '1'
    ELSE '0' END AS 'is_purchase'
FROM quiz AS q
LEFT JOIN home_try_on AS h ON q.user_id = h.user_id
LEFT JOIN purchase AS p ON q.user_id = p.user_id)
SELECT COUNT(*) AS 'total users', 
SUM(is_home_try_on) AS 'home trials',
SUM(number_of_pairs) AS 'pairs tried',
SUM(is_purchase) AS 'purchases',
1.0 * SUM(is_home_try_on) / COUNT(user_id) AS 'Quiz to Trial',
1.0 * SUM(is_purchase) / SUM(is_home_try_on) AS 'Trial to Purchase'
FROM funnel;
```

Output:

| total users | home trials | pairs tried | purchases | Quiz to Trial % | Trial to Purchase % |
|-------------|-------------|-------------|-----------|-----------------|---------------------|
| 1000        | 750         | 2992.0      | 495       | 7.5             | 6.6                 |

3 pair vs. 5 pair trials conversions:

| 3 pair conversion rate |
|------------------------|
| 0.53                   |
| 5 pair conversion rate |
| 0.79                   |
