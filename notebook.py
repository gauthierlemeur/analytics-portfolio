
# coding: utf-8

# ## 1. TV, halftime shows, and the Big Game
# <p>Whether or not you like football, the Super Bowl is a spectacle. There's a little something for everyone at your Super Bowl party. Drama in the form of blowouts, comebacks, and controversy for the sports fan. There are the ridiculously expensive ads, some hilarious, others gut-wrenching, thought-provoking, and weird. The half-time shows with the biggest musicians in the world, sometimes <a href="https://youtu.be/ZD1QrIe--_Y?t=14">riding giant mechanical tigers</a> or <a href="https://youtu.be/mjrdywp5nyE?t=62">leaping from the roof of the stadium</a>. It's a show, baby. And in this notebook, we're going to find out how some of the elements of this show interact with each other. After exploring and cleaning our data a little, we're going to answer questions like:</p>
# <ul>
# <li>What are the most extreme game outcomes?</li>
# <li>How does the game affect television viewership?</li>
# <li>How have viewership, TV ratings, and ad cost evolved over time?</li>
# <li>Who are the most prolific musicians in terms of halftime show performances?</li>
# </ul>
# <p><img src="https://assets.datacamp.com/production/project_684/img/left_shark.jpg" alt="Left Shark Steals The Show">
# <em><a href="https://www.flickr.com/photos/huntleypaton/16464994135/in/photostream/">Left Shark Steals The Show</a>. Katy Perry performing at halftime of Super Bowl XLIX. Photo by Huntley Paton. Attribution-ShareAlike 2.0 Generic (CC BY-SA 2.0).</em></p>
# <p>The dataset we'll use was <a href="https://en.wikipedia.org/wiki/Web_scraping">scraped</a> and polished from Wikipedia. It is made up of three CSV files, one with <a href="https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions">game data</a>, one with <a href="https://en.wikipedia.org/wiki/Super_Bowl_television_ratings">TV data</a>, and one with <a href="https://en.wikipedia.org/wiki/List_of_Super_Bowl_halftime_shows">halftime musician data</a> for all 52 Super Bowls through 2018. Let's take a look, using <code>display()</code> instead of <code>print()</code> since its output is much prettier in Jupyter Notebooks.</p>

# In[70]:


# Import pandas
import pandas as pd

# Load the CSV data into DataFrames
super_bowls = pd.read_csv('datasets/super_bowls.csv')
tv = pd.read_csv('datasets/tv.csv')
halftime_musicians = pd.read_csv('datasets/halftime_musicians.csv')

# Display the first five rows of each DataFrame
display(super_bowls.head())
display(tv.head())
display(halftime_musicians.head())


# In[71]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\ndef test_pandas_loaded():\n    assert \'pd\' in globals(), \\\n    \'Did you import the pandas module under the alias pd?\'\n    \ndef test_super_bowls_correctly_loaded():\n    correct_super_bowls = pd.read_csv(\'datasets/super_bowls.csv\')\n    assert correct_super_bowls.equals(super_bowls), "The variable super_bowls does not contain the data in super_bowls.csv."\n\ndef test_tv_correctly_loaded():\n    correct_tv = pd.read_csv(\'datasets/tv.csv\')\n    assert correct_tv.equals(tv), "The variable tv does not contain the data in tv.csv."\n    \ndef test_halftime_musicians_correctly_loaded():\n    correct_halftime_musicians = pd.read_csv(\'datasets/halftime_musicians.csv\')\n    assert correct_halftime_musicians.equals(halftime_musicians), "The variable halftime_musicians does not contain the data in halftime_musicians.csv."')


# ## 2. Taking note of dataset issues
# <p>For the Super Bowl game data, we can see the dataset appears whole except for missing values in the backup quarterback columns (<code>qb_winner_2</code> and <code>qb_loser_2</code>), which make sense given most starting QBs in the Super Bowl (<code>qb_winner_1</code> and <code>qb_loser_1</code>) play the entire game.</p>
# <p>From the visual inspection of TV and halftime musicians data, there is only one missing value displayed, but I've got a hunch there are more. The Super Bowl goes all the way back to 1967, and the more granular columns (e.g. the number of songs for halftime musicians) probably weren't tracked reliably over time. Wikipedia is great but not perfect.</p>
# <p>An inspection of the <code>.info()</code> output for <code>tv</code> and <code>halftime_musicians</code> shows us that there are multiple columns with null values.</p>

# In[72]:


# Summary of the TV data to inspect
tv.info()

print('\n')

# Summary of the halftime musician data to inspect
halftime_musicians.info()


# In[73]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\n# def test_nothing_task_2():\n#     assert True, "Nothing to test."\n\nlast_input = In[-2]\n\ndef test_not_empty_task_2():\n    assert "# ... YOUR CODE FOR TASK" not in last_input, \\\n        "It appears that # ... YOUR CODE FOR TASK X ... is still in the code cell, which suggests that you might not have attempted the code for this task. If you have, please delete # ... YOUR CODE FOR TASK X ... from the cell and resubmit."')


# ## 3. Combined points distribution
# <p>For the TV data, the following columns have missing values and a lot of them:</p>
# <ul>
# <li><code>total_us_viewers</code> (amount of U.S. viewers who watched at least some part of the broadcast)</li>
# <li><code>rating_18_49</code> (average % of U.S. adults 18-49 who live in a household with a TV that were watching for the entire broadcast)</li>
# <li><code>share_18_49</code> (average % of U.S. adults 18-49 who live in a household with a TV <em>in use</em> that were watching for the entire broadcast)</li>
# </ul>
# <p>For the halftime musician data, there are missing numbers of songs performed (<code>num_songs</code>) for about a third of the performances.</p>
# <p>There are a lot of potential reasons for these missing values. Was the data ever tracked? Was it lost in history? Is the research effort to make this data whole worth it? Maybe. Watching every Super Bowl halftime show to get song counts would be pretty fun. But we don't have the time to do that kind of stuff now! Let's take note of where the dataset isn't perfect and start uncovering some insights.</p>
# <p>Let's start by looking at combined points for each Super Bowl by visualizing the distribution. Let's also pinpoint the Super Bowls with the highest and lowest scores.</p>

# In[74]:


# Import matplotlib and set plotting style
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn')

# Plot a histogram of combined points
plt.hist(super_bowls['combined_pts'])
plt.xlabel('Combined Points')
plt.ylabel('Number of Super Bowls')
plt.show()

# Display the Super Bowls with the highest and lowest combined scores
display(super_bowls[super_bowls['combined_pts'] > 70])
display(super_bowls[super_bowls['combined_pts'] < 25 ])


# In[75]:


get_ipython().run_cell_magic('nose', '', "# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student's code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\ndef test_matplotlib_loaded():\n    assert 'plt' in globals(), \\\n    'Did you import the pyplot module from matplotlib under the alias plt?'")


# ## 4. Point difference distribution
# <p>Most combined scores are around 40-50 points, with the extremes being roughly equal distance away in opposite directions. Going up to the highest combined scores at 74 and 75, we find two games featuring dominant quarterback performances. One even happened recently in 2018's Super Bowl LII where Tom Brady's Patriots lost to Nick Foles' underdog Eagles 41-33 for a combined score of 74.</p>
# <p>Going down to the lowest combined scores, we have Super Bowl III and VII, which featured tough defenses that dominated. We also have Super Bowl IX in New Orleans in 1975, whose 16-6 score can be attributed to inclement weather. The field was slick from overnight rain, and it was cold at 46 °F (8 °C), making it hard for the Steelers and Vikings to do much offensively. This was the second-coldest Super Bowl ever and the last to be played in inclement weather for over 30 years. The NFL realized people like points, I guess.</p>
# <p><em>UPDATE: In Super Bowl LIII in 2019, the Patriots and Rams broke the record for the lowest-scoring Super Bowl with a combined score of 16 points (13-3 for the Patriots).</em></p>
# <p>Let's take a look at point <em>difference</em> now.</p>

# In[76]:


# Plot a histogram of point differences
plt.hist(super_bowls.difference_pts)
plt.xlabel('Point Difference')
plt.ylabel('Number of Super Bowls')
plt.show()

# Display the closest game(s) and biggest blowouts
display(super_bowls[super_bowls['difference_pts'] == 1])
display(super_bowls[super_bowls['difference_pts'] >= 35])


# In[77]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\nlast_input = In[-2]\n\ndef test_not_empty_task_4():\n    assert "# ... YOUR CODE FOR TASK" not in last_input, \\\n        "It appears that # ... YOUR CODE FOR TASK X ... is still in the code cell, which suggests that you might not have attempted the code for this task. If you have, please delete # ... YOUR CODE FOR TASK X ... from the cell and resubmit."')


# ## 5. Do blowouts translate to lost viewers?
# <p>The vast majority of Super Bowls are close games. Makes sense. Both teams are likely to be deserving if they've made it this far. The closest game ever was when the Buffalo Bills lost to the New York Giants by 1 point in 1991, which was  best remembered for Scott Norwood's last-second missed field goal attempt that went <em><a href="https://www.youtube.com/watch?v=RPFZCGgjDSg">wide right</a></em>, kicking off four Bills Super Bowl losses in a row. Poor Scott. The biggest point discrepancy ever was 45 points (!) where Hall of Famer Joe Montana's led the San Francisco 49ers to victory in 1990, one year before the closest game ever.</p>
# <p>I remember watching the Seahawks crush the Broncos by 35 points (43-8) in 2014, which was a boring experience in my opinion. The game was never really close. I'm pretty sure we changed the channel at the end of the third quarter. Let's combine our game data and TV to see if this is a universal phenomenon. Do large point differences translate to lost viewers? We can plot <a href="https://en.wikipedia.org/wiki/Nielsen_ratings">household share</a> <em>(average percentage of U.S. households with a TV in use that were watching for the entire broadcast)</em> vs. point difference to find out.</p>

# In[78]:


# Join game and TV data, filtering out SB I because it was split over two networks
games_tv = pd.merge(tv[tv['super_bowl'] > 1], super_bowls, on='super_bowl')

# Import seaborn
import seaborn as sns

# Create a scatter plot with a linear regression model fit
sns.regplot(x=games_tv['difference_pts'], y=games_tv['share_household'], data=games_tv)


# In[79]:


get_ipython().run_cell_magic('nose', '', "# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student's code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\nlast_value = _\n\ndef test_seaborn_loaded():\n    assert 'sns' in globals(), \\\n    'Did you import the seaborn module under the alias sns?'\n\ndef test_plot_exists_5():\n    try:\n        assert type(last_value) == type(sns.regplot(x='difference_pts', y='share_household', data=games_tv))\n    except AssertionError:\n        assert False, 'A plot was not the last output of the code cell.'")


# ## 6. Viewership and the ad industry over time
# <p>The downward sloping regression line and the 95% confidence interval for that regression <em>suggest</em> that bailing on the game if it is a blowout is common. Though it matches our intuition, we must take it with a grain of salt because the linear relationship in the data is weak due to our small sample size of 52 games.</p>
# <p>Regardless of the score though, I bet most people stick it out for the halftime show, which is good news for the TV networks and advertisers. A 30-second spot costs a pretty <a href="https://www.businessinsider.com/super-bowl-commercials-cost-more-than-eagles-quarterback-earns-2018-1">\$5 million</a> now, but has it always been that way? And how have number of viewers and household ratings trended alongside ad cost? We can find out using line plots that share a "Super Bowl" x-axis.</p>

# In[80]:


# Create a figure with 3x1 subplot and activate the top subplot
plt.subplot(3, 1, 1)
plt.plot(games_tv['super_bowl'], games_tv['avg_us_viewers'], color='#648FFF')
plt.title('Average Number of US Viewers')

# Activate the middle subplot
plt.subplot(3, 1, 2)
plt.plot(games_tv['super_bowl'], games_tv['rating_household'], '#DC267F')
plt.title('Household Rating')

# Activate the bottom subplot
plt.subplot(3, 1, 3)
plt.plot(games_tv['super_bowl'], games_tv['ad_cost'], '#FFB000')
plt.title('Ad Cost')
plt.xlabel('SUPER BOWL')

# Improve the spacing between subplots
plt.tight_layout()


# In[81]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\nlast_input = In[-2]\n\ndef test_not_empty_task_6():\n    assert "# ... YOUR CODE FOR TASK" not in last_input, \\\n        "It appears that # ... YOUR CODE FOR TASK X ... is still in the code cell, which suggests that you might not have attempted the code for this task. If you have, please delete # ... YOUR CODE FOR TASK X ... from the cell and resubmit."')


# ## 7. Halftime shows weren't always this great
# <p>We can see viewers increased before ad costs did. Maybe the networks weren't very data savvy and were slow to react? Makes sense since DataCamp didn't exist back then.</p>
# <p>Another hypothesis: maybe halftime shows weren't that good in the earlier years? The modern spectacle of the Super Bowl has a lot to do with the cultural prestige of big halftime acts. I went down a YouTube rabbit hole and it turns out the old ones weren't up to today's standards. Some offenders:</p>
# <ul>
# <li><a href="https://youtu.be/6wMXHxWO4ns?t=263">Super Bowl XXVI</a> in 1992: A Frosty The Snowman rap performed by children.</li>
# <li><a href="https://www.youtube.com/watch?v=PKQTL1PYSag">Super Bowl XXIII</a> in 1989: An Elvis impersonator that did magic tricks and didn't even sing one Elvis song.</li>
# <li><a href="https://youtu.be/oSXMNbK2e98?t=436">Super Bowl XXI</a> in 1987: Tap dancing ponies. (Okay, that's pretty awesome actually.)</li>
# </ul>
# <p>It turns out Michael Jackson's Super Bowl XXVII performance, one of the most watched events in American TV history, was when the NFL realized the value of Super Bowl airtime and decided they needed to sign big name acts from then on out. The halftime shows before MJ indeed weren't that impressive, which we can see by filtering our <code>halftime_musician</code> data.</p>

# In[82]:


halftime_musicians[halftime_musicians.super_bowl <= 27]


# In[83]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\nlast_value = _\n        \ndef test_head_output():\n    try:\n        assert "Wynonna Judd" not in last_value.to_string()\n    except AttributeError:\n        assert False, "Please do not use the display() or print() functions to display the filtered DataFrame. Write your line of code as the last line in the cell instead."\n    except AssertionError:\n        assert False, "Hmm, it seems halftime_musicians wasn\'t filtered correctly and/or displayed as the last output of the cell. Michael Jackson\'s performance should be the first row displayed."')


# ## 8. Who has the most halftime show appearances?
# <p>Lots of marching bands. American jazz clarinetist Pete Fountain. Miss Texas 1973 playing a violin. Nothing against those performers, they're just simply not <a href="https://www.youtube.com/watch?v=suIg9kTGBVI">Beyoncé</a>. To be fair, no one is.</p>
# <p>Let's see all of the musicians that have done more than one halftime show, including their performance counts.</p>

# In[84]:


# Count halftime show appearances for each musician and sort them from most to least
halftime_appearances = halftime_musicians.groupby('musician').count()['super_bowl'].reset_index()
halftime_appearances = halftime_appearances.sort_values('super_bowl', ascending=False)

# Display musicians with more than one halftime show appearance
halftime_appearances[halftime_appearances['super_bowl'] > 1]


# In[85]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\nlast_value = _\n\ndef test_filter_correct_8():\n    try:\n        assert len(last_value) == 14\n    except TypeError:\n        assert False, "Hmm, it seems halftime_appearances wasn\'t filtered correctly and/or displayed as the last line of code in the cell (i.e., displayed without the display() or print() functions). There should be 14 repeat halftime show acts."\n    except AssertionError:\n        assert False, "Hmm, it seems halftime_appearances wasn\'t filtered correctly. There should be 14 repeat halftime show acts."')


# ## 9. Who performed the most songs in a halftime show?
# <p>The world famous <a href="https://www.youtube.com/watch?v=RL_3oqpHiDg">Grambling State University Tiger Marching Band</a> takes the crown with six appearances. Beyoncé, Justin Timberlake, Nelly, and Bruno Mars are the only post-Y2K musicians with multiple appearances (two each).</p>
# <p>From our previous inspections, the <code>num_songs</code> column has lots of missing values:</p>
# <ul>
# <li>A lot of the marching bands don't have <code>num_songs</code> entries.</li>
# <li>For non-marching bands, missing data starts occurring at Super Bowl XX.</li>
# </ul>
# <p>Let's filter out marching bands by filtering out musicians with the word "Marching" in them and the word "Spirit" (a common naming convention for marching bands is "Spirit of [something]"). Then we'll filter for Super Bowls after Super Bowl XX to address the missing data issue, <em>then</em> let's see who has the most number of songs.</p>

# In[86]:


# Filter out most marching bands
no_bands = halftime_musicians[~halftime_musicians.musician.str.contains('Marching')]
no_bands = no_bands[~no_bands.musician.str.contains('Spirit')]

# Plot a histogram of number of songs per performance
most_songs = int(max(no_bands['num_songs'].values))
plt.hist(no_bands.num_songs.dropna(), bins=most_songs)
plt.xlabel('Number of Songs Per Halftime Show Performance')
plt.ylabel('Number of Musicians')
plt.show()

# Sort the non-band musicians by number of songs per appearance...
no_bands = no_bands.sort_values('num_songs', ascending=False)
# ...and display the top 15
display(no_bands.head(15))


# In[87]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\nlast_input = In[-2]\n\ndef test_not_empty_task_9():\n    assert "# ... YOUR CODE FOR TASK" not in last_input, \\\n        "It appears that # ... YOUR CODE FOR TASK X ... is still in the code cell, which suggests that you might not have attempted the code for this task. If you have, please delete # ... YOUR CODE FOR TASK X ... from the cell and resubmit."')


# ## 10. Conclusion
# <p>So most non-band musicians do 1-3 songs per halftime show. It's important to note that the duration of the halftime show is fixed (roughly 12 minutes) so songs per performance is more a measure of how many hit songs you have. JT went off in 2018, wow. 11 songs! Diana Ross comes in second with 10 in her medley in 1996.</p>
# <p>In this notebook, we loaded, cleaned, then explored Super Bowl game, television, and halftime show data. We visualized the distributions of combined points, point differences, and halftime show performances using histograms. We used line plots to see how ad cost increases lagged behind viewership increases. And we discovered that blowouts do appear to lead to a drop in viewers.</p>
# <p>This year's Big Game will be here before you know it. Who do you think will win Super Bowl LIII?</p>
# <p><em>UPDATE: <a href="https://en.wikipedia.org/wiki/Super_Bowl_LIII">Spoiler alert</a>.</em></p>

# In[88]:


# 2018-2019 conference champions
patriots = 'New England Patriots'
rams = 'Los Angeles Rams'

# Who will win Super Bowl LIII?
super_bowl_LIII_winner = patriots
print('The winner of Super Bowl LIII will be the', super_bowl_LIII_winner)


# In[89]:


get_ipython().run_cell_magic('nose', '', '# %%nose needs to be included at the beginning of every @tests cell\n\n# One or more tests of the student\'s code\n# The @solution should pass the tests\n# The purpose of the tests is to try to catch common errors and\n# to give the student a hint on how to resolve these errors\n\ndef test_valid_winner_chosen():\n    assert super_bowl_LIII_winner == \'New England Patriots\' or super_bowl_LIII_winner == \'Los Angeles Rams\', \\\n    "It appears a valid potential winner was not selected. Please assign the patriots variable or the rams variable to super_bowl_LIII_winner."')

