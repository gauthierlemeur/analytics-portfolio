#!/usr/bin/env python
# coding: utf-8

# # Analyzing CIA Factbook Data Using SQLite and Python
# 
# ### In this project, we'll work with data from the CIA World Factbook, a compendium of statistics about all of the countries on Earth. The Factbook contains demographic information like:
# 
# - population - The population as of 2015.
# - population_growth - The annual population growth rate, as a percentage.
# - area - The total land and water area.

# In[1]:


import sqlite3
import pandas as pd
conn = sqlite3.connect("factbook.db")

q = "SELECT * FROM sqlite_master WHERE type='table';"
pd.read_sql_query(q, conn)


# In[4]:


q2 = "select * from facts limit 5"
pd.read_sql_query(q2, conn)


# ## Summary Statistics

# In[6]:


q3 = '''
SELECT 
MIN(population) min_pop, 
MAX(population) max_pop, 
MIN(population_growth) min_pop_growth, 
MAX(population_growth) max_pop_growth 
FROM facts
'''
pd.read_sql_query(q3, conn)


# ## Exploring Outliers

# A few things stick out from the summary statistics in the last screen:
# 
# - there's a country with a population of 0
# - there's a country with a population of 7256490011 (or more than 7.2 billion people)
# 
# Let's zoom in on just these countries.

# In[7]:


q4 = '''
SELECT *
FROM facts
WHERE population == (select max(population) from facts);
'''
pd.read_sql_query(q4, conn)


# In[8]:


q5 = '''
select *
from facts
where population == (select min(population) from facts);
'''

pd.read_sql_query(q5, conn)


# We find that the world's population is marked into a country name "World" and that Antarctica has a population of "0".

# ## Histograms

# In[9]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib inline')

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

q6 = '''
select population, population_growth, birth_rate, death_rate
from facts
where population != (select max(population) from facts)
and population != (select min(population) from facts);
'''
pd.read_sql_query(q6, conn).hist(ax=ax)


# ##  Which countries have the highest population density?

# In[10]:


q7 = "select name, cast(population as float)/cast(area as float) density from facts order by density desc limit 20"
pd.read_sql_query(q7, conn)


# In[11]:


q7 = '''select population, population_growth, birth_rate, death_rate
from facts
where population != (select max(population) from facts)
and population != (select min(population) from facts);
'''
pd.read_sql_query(q7, conn)


# In[ ]:




