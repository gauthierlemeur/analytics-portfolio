# Project: Analyzing First and Last touch attribution

## Date: October 26 2019

### Data schema: CoolTshirts (fictional data) 
1. user_id - A unique identifier for each visitor to a page
2. timestamp - The time at which the visitor came to the page
3. page_name - The title of the section of the page that was visited
4. utm_source - Identifies which touchpoint sent the traffic (e.g. google, email, or facebook)
5. utm_medium - Identifies what type of link was used (e.g. cost-per-click or email)
6. utm_campaign - Identifies the specific ad or email blast (e.g. retargetting-ad or weekly-newsletter)

First 10 rows: 

| page_name         | timestamp           | user_id | utm_campaign                 | utm_source |
|-------------------|---------------------|---------|------------------------------|------------|
| 1 - landing_page  | 2018-01-24 03:12:16 | 10006   | getting-to-know-cool-tshirts | nytimes    |
| 2 - shopping_cart | 2018-01-24 04:04:16 | 10006   | getting-to-know-cool-tshirts | nytimes    |
| 3 - checkout      | 2018-01-25 23:10:16 | 10006   | weekly-newsletter            | email      |
| 1 - landing_page  | 2018-01-25 20:32:02 | 10030   | ten-crazy-cool-tshirts-facts | buzzfeed   |
| 2 - shopping_cart | 2018-01-25 23:05:02 | 10030   | ten-crazy-cool-tshirts-facts | buzzfeed   |
| 3 - checkout      | 2018-01-28 13:26:02 | 10030   | retargetting-campaign        | email      |
| 4 - purchase      | 2018-01-28 13:38:02 | 10030   | retargetting-campaign        | email      |
| 1 - landing_page  | 2018-01-05 18:31:17 | 10045   | getting-to-know-cool-tshirts | nytimes    |
| 2 - shopping_cart | 2018-01-05 21:16:17 | 10045   | getting-to-know-cool-tshirts | nytimes    |
| 3 - checkout      | 2018-01-09 03:05:17 | 10045   | retargetting-ad              | facebook   |

Example of first touch: Buzzfeed

```sql
 SELECT *
 FROM page_visits
 WHERE user_id = 10069
 AND utm_source = 'buzzfeed';
 ```
 
 Output: 
 
| page_name         | timestamp           | user_id | utm_campaign                 | utm_source |
|-------------------|---------------------|---------|------------------------------|------------|
| 1 - landing_page  | 2018-01-02 23:14:01 | 10069   | ten-crazy-cool-tshirts-facts | buzzfeed   |
| 2 - shopping_cart | 2018-01-02 23:55:01 | 10069   | ten-crazy-cool-tshirts-facts | buzzfeed   |

Example of last touch: Facebook

| page_name         | timestamp           | user_id | utm_campaign                 | utm_source |
|-------------------|---------------------|---------|------------------------------|------------|
| 1 - landing_page  | 2018-01-02 23:14:01 | 10069   | ten-crazy-cool-tshirts-facts | buzzfeed   |
| 2 - shopping_cart | 2018-01-02 23:55:01 | 10069   | ten-crazy-cool-tshirts-facts | buzzfeed   |
| 3 - checkout      | 2018-01-04 08:12:01 | 10069   | retargetting-ad              | facebook   |
| 4 - purchase      | 2018-01-04 08:13:01 | 10069   | retargetting-ad              | facebook   |

- *First-touch attribution* only considers the first utm_source for each customer, which would be buzzfeed in this case. This is a good way of knowing how visitors initially discover a website.
- *Last-touch attribution* only considers the last utm_source for each customer, which would be facebook in this case. This is a good way of knowing how visitors are drawn back to a website, especially for making a final purchase.

###Let's now look at the most common first and last touches for our users

We first need to create MIN and MAX touchpoints for each users: 
```sql
SELECT user_id,
   MIN(timestamp) AS 'first_touch_at',
   MAX(timestamp) AS 'last_touch_at'
FROM page_visits
GROUP BY user_id;
```
Then, we can join these results back to the original table:

```sql
WITH first_touch AS (
   SELECT user_id,
      MIN(timestamp) AS 'first_touch_at'
   FROM page_visits
   GROUP BY user_id)
SELECT ft.user_id,
  ft.first_touch_at,
  pv.utm_source
FROM first_touch AS 'ft'
JOIN page_visits AS 'pv'
  ON ft.user_id = pv.user_id
  AND ft.first_touch_at = pv.timestamp;
```

Now that we understand the basic process, we can answer a few questions:

1. Get familiar with the company.

- How many campaigns and sources does CoolTShirts use and how are they related? Be sure to explain the difference between utm_campaign and utm_source.
- What pages are on their website?

2. What is the user journey?

- How many first touches is each campaign responsible for?
- How many last touches is each campaign responsible for?
- How many visitors make a purchase?
- How many last touches on the purchase page is each campaign responsible for?
- What is the typical user journey?

3. Optimize the campaign budget.

- CoolTShirts can re-invest in 5 campaigns. Which should they pick and why?

### Step by step:

- What are the distinct campaigns? 

```sql
SELECT DISTINCT utm_campaign
FROM page_visits;
```

| utm_campaign                        |
|-------------------------------------|
| getting-to-know-cool-tshirts        |
| weekly-newsletter                   |
| ten-crazy-cool-tshirts-facts        |
| retargetting-campaign               |
| retargetting-ad                     |
| interview-with-cool-tshirts-founder |
| paid-search                         |
| cool-tshirts-search                 |

- What are the distinct sources?

| utm_source |
|------------|
| nytimes    |
| email      |
| buzzfeed   |
| facebook   |
| medium     |
| google     |

- What source is used for each campaign? 

| utm_campaign                        | utm_source |
|-------------------------------------|------------|
| getting-to-know-cool-tshirts        | nytimes    |
| weekly-newsletter                   | email      |
| ten-crazy-cool-tshirts-facts        | buzzfeed   |
| retargetting-campaign               | email      |
| retargetting-ad                     | facebook   |
| interview-with-cool-tshirts-founder | medium     |
| paid-search                         | google     |
| cool-tshirts-search                 | google     |

- What pages are on the website? 

| page_name         |
|-------------------|
| 1 - landing_page  |
| 2 - shopping_cart |
| 3 - checkout      |
| 4 - purchase      |

- How many first touches / last touches is each campaign responsible for? 

```sql
WITH first_touch AS (
    SELECT user_id,
        MIN(timestamp) as first_touch_at
    FROM page_visits
    GROUP BY user_id),
ft_attr AS (
  SELECT ft.user_id,
         ft.first_touch_at,
         pv.utm_source,
         pv.utm_campaign
  FROM first_touch ft
  JOIN page_visits pv
    ON ft.user_id = pv.user_id
    AND ft.first_touch_at = pv.timestamp
)
SELECT ft_attr.utm_source source,
       ft_attr.utm_campaign campaign,
       COUNT(*) as 'first touch attributed'
FROM ft_attr
GROUP BY 1, 2
ORDER BY 3 DESC;

WITH last_touch AS (
    SELECT user_id,
        MAX(timestamp) as last_touch_at
    FROM page_visits
    GROUP BY user_id),
lt_attr AS (
  SELECT lt.user_id,
         lt.last_touch_at,
         pv.utm_source,
         pv.utm_campaign
  FROM last_touch lt
  JOIN page_visits pv
    ON lt.user_id = pv.user_id
    AND lt.last_touch_at = pv.timestamp
)
SELECT lt_attr.utm_source source,
       lt_attr.utm_campaign campaign,
       COUNT(*) as 'last touch attributed'
FROM lt_attr
GROUP BY 1, 2
ORDER BY 3 DESC;
```

Output:

| source   | campaign                            | first touch attributed |
|----------|-------------------------------------|------------------------|
| medium   | interview-with-cool-tshirts-founder | 622                    |
| nytimes  | getting-to-know-cool-tshirts        | 612                    |
| buzzfeed | ten-crazy-cool-tshirts-facts        | 576                    |
| google   | cool-tshirts-search                 | 169                    |

| source   | campaign                            | last touch attributed  |
|----------|-------------------------------------|------------------------|
| email    | weekly-newsletter                   | 447                    |
| facebook | retargetting-ad                     | 443                    |
| email    | retargetting-campaign               | 245                    |
| nytimes  | getting-to-know-cool-tshirts        | 232                    |
| buzzfeed | ten-crazy-cool-tshirts-facts        | 190                    |
| medium   | interview-with-cool-tshirts-founder | 184                    |
| google   | paid-search                         | 178                    |
| google   | cool-tshirts-search                 | 60                     |

- How many visitors made a purchase?

```sql
SELECT COUNT (DISTINCT user_id)
FROM page_visits
WHERE page_name = '4 - purchase';
```

Output: 361

- How many last touches on the purchase page is each campaign responsible for?

| source   | campaign                            | last touch attributed |
|----------|-------------------------------------|-----------------------|
| email    | weekly-newsletter                   | 115                   |
| facebook | retargetting-ad                     | 113                   |
| email    | retargetting-campaign               | 54                    |
| google   | paid-search                         | 52                    |
| buzzfeed | ten-crazy-cool-tshirts-facts        | 9                     |
| nytimes  | getting-to-know-cool-tshirts        | 9                     |
| medium   | interview-with-cool-tshirts-founder | 7                     |
| google   | cool-tshirts-search                 | 2                     |


- CoolTShirts can re-invest in 5 campaigns. Given your findings in the project, which should we pick? 

Best first touch campaigns are: medium, nytimes, and buzzfeed
Best last touch campaigns for conversions are: email (weekly-newsletter / retargeting), facebook(retargeting)

They should reinvest in both sides of the funnel, for these five campaigns. 



