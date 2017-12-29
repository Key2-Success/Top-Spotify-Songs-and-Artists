
# coding: utf-8

# # Cleaning Dataset

# In[1]:

# loading packages
import pandas as pd
import plotly.plotly as py
import plotly
from plotly.graph_objs import *
import plotly.graph_objs as go


# In[2]:

# load data
spotify = pd.read_csv(r"C:\Users\KK\Documents\Kitu\College\Senior Year\Extracurriculars\Python\Spotify\.spyproject\data.csv")


# In[3]:

# explore data
spotify.head()
spotify.shape
spotify.dtypes


# As we can see, the dataset has 2017625 observations and 7 variables.
# Moreover, some of the variable's data types are incorrect. Let's correct that.

# In[4]:

# change variable data types
spotify.Region = spotify.Region.astype("category")
spotify.Date = pd.to_datetime(spotify["Date"])
spotify.dtypes


# Now all of the variables' data type are correct.

# In[5]:

# look into counts of Region
spotify["Region"].value_counts()
len(spotify["Region"].value_counts())


# Here is the list of all of the countries included in this dataset.
# Furthermore, we see that there are a total of 54 countries (including the global "country").
# I am going to choose a select few countries to analyze; I am interested in seeing how song and artist choices are affected by region.

# In[6]:

# make new dataframes for global, usa, great britain, mexico, taiwan, and singapore
globe = spotify[spotify.Region == "global"]
usa = spotify[spotify.Region == "us"]
great_britain = spotify[spotify.Region == "gb"]
mexico = spotify[spotify.Region == "mx"]
taiwan = spotify[spotify.Region == "tw"]
singapore = spotify[spotify.Region == "sg"]


# # Preparing Top Songs Streamed

# In[7]:

# create descending table of top songs by total stream count per country
# also add new country variable for use in merging
top_globe = globe.groupby("Track Name").agg({"Streams": "sum"})
top_globe = top_globe.sort_values(["Streams"], ascending = False)
top_globe["country"] = "Globe"

top_usa = usa.groupby("Track Name").agg({"Streams": "sum"})
top_usa = top_usa.sort_values(["Streams"], ascending = False)
top_usa["country"] = "USA"

top_great_britain = great_britain.groupby("Track Name").agg({"Streams": "sum"})
top_great_britain = top_great_britain.sort_values(["Streams"], ascending = False)
top_great_britain["country"] = "Great Britain"

top_mexico = mexico.groupby("Track Name").agg({"Streams": "sum"})
top_mexico = top_mexico.sort_values(["Streams"], ascending = False)
top_mexico["country"] = "Mexico"

top_taiwan = taiwan.groupby("Track Name").agg({"Streams": "sum"})
top_taiwan = top_taiwan.sort_values(["Streams"], ascending = False)
top_taiwan["country"] = "Taiwan"

top_singapore = singapore.groupby("Track Name").agg({"Streams": "sum"})
top_singapore = top_singapore.sort_values(["Streams"], ascending = False)
top_singapore["country"] = "Singapore"


# We are going to first look into the top songs streamed by country. I have created separate dataframes for each country, descending by the top songs. I have also added a new country variable that will be used for when we merge these dataframes together.

# In[8]:

# add a new variable of the proportion of the song from all streams
top_globe["prop"] = top_globe["Streams"]/sum(top_globe["Streams"])*100
top_usa["prop"] = top_usa["Streams"]/sum(top_usa["Streams"])*100
top_great_britain["prop"] = top_great_britain["Streams"]/sum(top_great_britain["Streams"])*100
top_mexico["prop"] = top_mexico["Streams"]/sum(top_mexico["Streams"])*100
top_taiwan["prop"] = top_taiwan["Streams"]/sum(top_taiwan["Streams"])*100
top_singapore["prop"] = top_singapore["Streams"]/sum(top_singapore["Streams"])*100


# It's important to standardize the stream count, so I will do that by using proportion - by using the percent the song was streamed relative to all other songs. Otherwise, we will be left with an unevent distribution of stream counts, which would confound our analysis, since higher stream counts overall are related to population of the country and not song interest. Thus, to interpret the proportion variable, we would say: "from all songs streamed on Spotify, this song was streamed x% of the time during January 2017 to August 2017 in country y."

# In[9]:

# subset to only top 3 songs
top_globe = top_globe[0:3]
top_usa = top_usa[0:3]
top_great_britain = top_great_britain[0:3]
top_mexico = top_mexico[0:3]
top_taiwan = top_taiwan[0:3]
top_singapore = top_singapore[0:3]


# In[10]:

# delete Streams variable, since we will be using prop to compare
del top_globe["Streams"]
del top_usa["Streams"]
del top_great_britain["Streams"]
del top_mexico["Streams"]
del top_taiwan["Streams"]
del top_singapore["Streams"]


# In[11]:

# row bind all dataframes
top_all_merged = top_globe.append([top_usa, top_great_britain, top_mexico, top_taiwan, top_singapore])


# In[12]:

# reset index to include index as a variable
top_all_merged = top_all_merged.reset_index()


# In[13]:

# find all unique songs
all_songs = top_all_merged["Track Name"].value_counts()
all_songs = all_songs.reset_index()
len(top_all_merged["Track Name"].value_counts())


# We see that there are 9 unique songs across the 6 countries' (including global) top 3 songs streamed. This means that there is an overlap of (6*3) - 9 = 18 - 9 = 9 shared song occurrences among these countries' top 3 songs.

# # Plotting Top Songs Streamed

# In[23]:

# bar plot of top 3 songs by country...interactive via plotly 
# did not use Python's visualizations because they are not as powerful or engaging as plotly

# each trace represents one of nine of the unique songs
# y represents the proportion value for each country
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('sweetmusicality', 'dtCZVpCg9ovcOUWQsmMp')

trace1 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [2.54, 1.45, 2.47, 1.75, 2.11, 2.7], 
  "name": "Shape of You", 
  "type": "bar", 
  "uid": "d81641", 
  "visible": True, 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:593809"
}
trace2 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [1.48, 0, 1.4, 0, 0, 1.48], 
  "name": "Despacito - Remix", 
  "type": "bar", 
  "uid": "c15c84", 
  "visible": True, 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:724a8c"
}
trace3 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 0, 1.97, 1.78], 
  "name": "Something Just Like This", 
  "type": "bar", 
  "uid": "1dbc1b", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:31cdb8"
}
trace4 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [1.3, 0, 0, 2.22, 0, 0], 
  "name": "Despacito (Featuring Daddy Yankee)", 
  "type": "bar", 
  "uid": "c6b042", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:4583e2"
}
trace5 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 2.16, 0, 0], 
  "name": "Me Rehúso", 
  "type": "bar", 
  "uid": "be7d95", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:b9ea50"
}
trace6 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 1.2, 0, 0, 0, 0], 
  "name": "Mask Off", 
  "type": "bar", 
  "uid": "60d6b8", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:989da6"
}
trace7 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 0, 1.23, 0], 
  "name": "演員", 
  "type": "bar", 
  "uid": "f912b1", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:cd61ac"
}
trace8 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 1.67, 0, 0, 0], 
  "name": "Castle on the Hill", 
  "type": "bar", 
  "uid": "c01a7b", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:083ede"
}
trace9 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 1.51, 0, 0, 0, 0], 
  "name": "HUMBLE.", 
  "type": "bar", 
  "uid": "d9ea4a", 
  "xsrc": "sweetmusicality:7:ff97bb", 
  "ysrc": "sweetmusicality:7:1008dc"
}

# assign the data and create the layout for the barplot
data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9]
layout = {
  "annotations": [
    {
      "x": 1.09648221896, 
      "y": 0.671878877124, 
      "font": {"size": 21}, 
      "showarrow": False, 
      "text": "<b>Song</b>", 
      "xanchor": "middle", 
      "xref": "paper", 
      "yanchor": "bottom", 
      "yref": "paper"
    }
  ], 
  "autosize": True, 
  "barmode": "stack", 
  "font": {"size": 18}, 
  "hovermode": "closest", 
  "legend": {
    "x": 1.01935845381, 
    "y": 0.673239347844, 
    "borderwidth": 0, 
    "orientation": "v", 
    "traceorder": "normal"
  }, 
  "margin": {"b": 80}, 
  "title": "<b>Top 3 Streamed Songs on Spotify from Jan 2017 - Aug 2017 by Country</b>", 
  "titlefont": {"size": 28}, 
  "xaxis": {
    "autorange": False, 
    "domain": [0, 1.01], 
    "range": [-0.5, 5.51343670089], 
    "side": "bottom", 
    "title": "<b>Country</b>", 
    "type": "category"
  }, 
  "yaxis": {
    "anchor": "x", 
    "autorange": False, 
    "domain": [-0.01, 1], 
    "range": [0, 6.66421250763], 
    "title": "<b>% this song was streamed in its country</b>", 
    "type": "linear"
  }
}

# let's plot it!
fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# # Analyzing Top Songs Streamed

# I really like this barplot, for many reasons. I appreciate that it's interactive, so that when you hover over a stacked bar, you can see the country, the song name, and the proportion it was streamed in that country. Another cool feature of this graph is that in the legend, you can disable and re-enable song names, if you would like to only compare select songs.
# 
# Now to actually analyze our findings: wow! This is pretty neat, actually. Across all the countries chosen and across the globe, Shape of You was a genuine hit! This truly cements the saying that music brings people together globally, regardless of language. I am especially pleased to see this finding because I had included Mexico and Taiwan, whose national language is not English, as well as Singapore, which is a cultural hub.
# 
# Besides Shape of You, Despacito also took off across many countries. Interestingly, the version that was most popular in Mexico was the one featuring Daddy Yankee - perhaps because he is of Hispanic origin. 
# 
# Something Just Like This was a popular streaming choice in both Taiwan and Singapore, which leads me to contemplate whether neighboring share similar song tastes, since these two countries are Asian.
# 
# After these three songs, however, the remaining songs are specific to each country. As an American, I can definitely attest to the popularity of HUMBLE. and Mask Off. Whereas the other countries' top 3 songs are English (besides Despacito), Mexico and Taiwan both share a top song from their language, which is quite sweet, since it shows how different cultures and languages have their own unique sense of music, reminding me again of the importance of diversity - without it, others would not be able to engage and immerse in the beauty of others' cultures. 
# 
# Besides simply looking at the top songs, looking at each song's proportion is also fascinating. Singapore very much enjoyed Shape of You, above the global proportion, whereas the top 3 song streamed in the USA have relatively small proportions, leading me to believe that the USA has many popular song streams, each of which most likely share a lower proportion of streaming.
# 
# These songs, in general, fall under the categories pop, rap, or hip-hop. These genres seem to be universally streamed.
# 
# However, I realize that release date has a huge role to play in stream count, and a quick Google search showed that 9 of these songs were released no later than April 2017. Shape of You was released in the first week of January itself, so to be a "popularly streamed" song for a year, one must release the song earlier in the year. In the future, I would be curious to explore stream count for up until a month after the song release date, to normalize the difference in release date.
# 
# I am very intrigued by these findings, and I would be interested in further exploring this data by looking into other countries or into more than just the top 3 songs. Unfortunately, I was limited by 6 countries and 3 top songs for the sake of simplicity in my barplot visualization - any more, and it would look too cluttered (originally, I had also included France, but it corrupted the simplicity of the barplot). Perhaps I will look into other types of visualizations, such as the donut plot or global map, or look into creating more than just 1 visualization. In the time being, however, I am going to listen to 演員 and Me Rehúso for the first time, as introduced to me by Taiwan and Mexico, respectively.

# # Preparing Top Artists Streamed

# I am interested in seeing the correlation between the top songs that we just explored to the top artists. Are there artists who have multiple songs that are streamed at lower counts, but overall, have a higher stream count? Do the songs from our previous investigation correlate to the top artists streamed? Are there songs that are a hit, but whose artist is not, because the artist only produced one top song? These are some of the questions I hope to answer.

# In[15]:

# create descending table of top artists by total stream count per country
# also add new country variable for use in merging
top_globe2 = globe.groupby("Artist").agg({"Streams": "sum"})
top_globe2 = top_globe2.sort_values(["Streams"], ascending = False)
top_globe2["country"] = "Globe"

top_usa2 = usa.groupby("Artist").agg({"Streams": "sum"})
top_usa2 = top_usa2.sort_values(["Streams"], ascending = False)
top_usa2["country"] = "USA"

top_great_britain2 = great_britain.groupby("Artist").agg({"Streams": "sum"})
top_great_britain2 = top_great_britain2.sort_values(["Streams"], ascending = False)
top_great_britain2["country"] = "Great Britain"

top_mexico2 = mexico.groupby("Artist").agg({"Streams": "sum"})
top_mexico2 = top_mexico2.sort_values(["Streams"], ascending = False)
top_mexico2["country"] = "Mexico"

top_taiwan2 = taiwan.groupby("Artist").agg({"Streams": "sum"})
top_taiwan2 = top_taiwan2.sort_values(["Streams"], ascending = False)
top_taiwan2["country"] = "Taiwan"

top_singapore2 = singapore.groupby("Artist").agg({"Streams": "sum"})
top_singapore2 = top_singapore2.sort_values(["Streams"], ascending = False)
top_singapore2["country"] = "Singapore"


# Similar to our song analysis, we are going to first look into the top artists streamed by country. I have created separate dataframes for each country, descending by the top artists. I have also added a new country variable that will be used for when we merge these dataframes together.

# In[16]:

# add a new variable of the proportion of the artist from all streams
top_globe2["prop"] = top_globe2["Streams"]/sum(top_globe2["Streams"])*100
top_usa2["prop"] = top_usa2["Streams"]/sum(top_usa2["Streams"])*100
top_great_britain2["prop"] = top_great_britain2["Streams"]/sum(top_great_britain2["Streams"])*100
top_mexico2["prop"] = top_mexico2["Streams"]/sum(top_mexico2["Streams"])*100
top_taiwan2["prop"] = top_taiwan2["Streams"]/sum(top_taiwan2["Streams"])*100
top_singapore2["prop"] = top_singapore2["Streams"]/sum(top_singapore2["Streams"])*100


# Since I have already explained my motive behind using proportions in the song analysis, we are going to carry the same reasoning to the top artists. Now, to interpret the proportion variable, we would say: "from all artists streamed on Spotify, this artist was streamed x% of the time during January 2017 to August 2017 in country y."

# In[17]:

# subset to only top 3 artists
top_globe2 = top_globe2[0:3]
top_usa2 = top_usa2[0:3]
top_great_britain2 = top_great_britain2[0:3]
top_mexico2 = top_mexico2[0:3]
top_taiwan2 = top_taiwan2[0:3]
top_singapore2 = top_singapore2[0:3]


# In[18]:

# delete Streams variable, since we will be using prop to compare
del top_globe2["Streams"]
del top_usa2["Streams"]
del top_great_britain2["Streams"]
del top_mexico2["Streams"]
del top_taiwan2["Streams"]
del top_singapore2["Streams"]


# In[19]:

# row bind all dataframes
top_all_merged2 = top_globe2.append([top_usa2, top_great_britain2, top_mexico2, top_taiwan2, top_singapore2])


# In[20]:

# reset index to include index as a variable
top_all_merged2 = top_all_merged2.reset_index()


# In[21]:

# find all unique artists
all_artists = top_all_merged2["Artist"].value_counts()
all_artists = all_artists.reset_index()
len(top_all_merged2["Artist"].value_counts())


# We see that there are 8 unique artists across the 6 countries' (including global) top 3 artists streamed. This means that there is an overlap of (6 * 3) - 8 = 18 - 8 = 10 shared artist occurrences among these countries' top 3 artists. Interestingly, there were 9 unique songs in the top 3, and only 8 unique artists in the top 3. This suggests a slight extent of shuffling around in the top 3 between the songs and artists.

# # Plotting Top Artists Streamed

# In[25]:

# bar plot of top 5 artists by country...interactive via plotly 
# did not use Python's visualizations because they are not as powerful or engaging as plotly

# each trace represents one of fourteen of the unique artists
# y represents the proportion value for each country
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('sweetmusicality', 'dtCZVpCg9ovcOUWQsmMp')

trace1 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [7.31, 3.61, 13.1, 3.3, 5.6, 8.41], 
  "name": "Ed Sheeran", 
  "type": "bar", 
  "uid": "955263", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:ef572e"
}
trace2 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [3.91, 0, 2.85, 0, 6.15, 6.26], 
  "name": "The Chainsmokers", 
  "type": "bar", 
  "uid": "067b27", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:c677a0"
}
trace3 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [4.28, 6.92, 5.64, 0, 0, 0], 
  "name": "Drake", 
  "type": "bar", 
  "uid": "41897b", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:ddcce6"
}
trace4 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 3.8, 0, 0], 
  "name": "J Balvin", 
  "type": "bar", 
  "uid": "1e2640", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:0e6f78"
}
trace5 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 3.56, 0, 0], 
  "name": "Maluma", 
  "type": "bar", 
  "uid": "82752c", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:5279b7"
}
trace6 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 0, 0, 2.43], 
  "name": "Bruno Mars", 
  "type": "bar", 
  "uid": "7d1dea", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:91136f"
}
trace7 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 5.53, 0, 0, 0, 0], 
  "name": "Kendrick Lamar", 
  "type": "bar", 
  "uid": "e3f565", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:7a8be3"
}
trace8 = {
  "x": ["Global", "USA", "Great Britain", "Mexico", "Taiwan", "Singapore"], 
  "y": [0, 0, 0, 0, 2.09, 0], 
  "name": "Martin Garrix", 
  "type": "bar", 
  "uid": "c384a5", 
  "xsrc": "sweetmusicality:5:824c9c", 
  "ysrc": "sweetmusicality:5:554b1c"
}

# create the data and layout of the graph
data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]
layout = {
  "annotations": [
    {
      "x": 1.08896492729, 
      "y": 0.659509202454, 
      "font": {"size": 21}, 
      "showarrow": False, 
      "text": "<b>Artist</b>", 
      "xanchor": "middle", 
      "xref": "paper", 
      "yanchor": "bottom", 
      "yref": "paper"
    }
  ], 
  "autosize": True, 
  "barmode": "stack", 
  "font": {"size": 18}, 
  "hovermode": "closest", 
  "legend": {
    "x": 1.01935845381, 
    "y": 0.673239347844, 
    "borderwidth": 0, 
    "orientation": "v", 
    "traceorder": "normal"
  }, 
  "title": "<b>Top 3 Streamed Artists on Spotify from Jan 2017 - Aug 2017 by Country</b>", 
  "titlefont": {"size": 28}, 
  "xaxis": {
    "autorange": True, 
    "range": [-0.5, 5.5], 
    "title": "<b>Country</b>", 
    "type": "category"
  }, 
  "yaxis": {
    "autorange": True, 
    "range": [0, 22.7263157895], 
    "title": "<b>% this artist was streamed in its country</b>", 
    "type": "linear"
  }
}

# let's plot it!
fig = go.Figure(data = data, layout = layout)
py.iplot(fig)


# # Analyzing Top Artists Streamed

# Wow, this is some neat stuff! Again, as explained earlier in the top songs streamed, this interactive plot allows hovering upon each stacked bar to view its values as well as disable and re-enable artist names.
# 
# Besides the cool aspects of plotly, let's dive into analyzing what we see. Ed Sheeran is sure a hit across all these countries! And this makes sense, since Shape of You was also the most streamed song. It's especially captivating to see how Ed Sheeran's highest stream proportion is in Great Britain, his homeland country, by nearly twice as much as the global proportion. Seeing this makes me believe that a country is quite loyal to its citizens, since an artist is most likely most appreciated and listened to in his or her own country. How comforting to hear.
# 
# Besides Ed Sheeran, The Chainsmokers also made quite a ripple across the globe, besides in Mexico and USA. Interestingly, both Taiwan and Singapore listen to The Chainsmokers at the highest proportion, which again solidifies my belief that countries in similar regions listen to similar music. This also makes sense because Something Just Like This was a top song choice for both of these two countries.
# 
# Drake has a huge presence in the USA, Great Britain, and across the globe. I'm fascinated to see how he is popular in natively English speaking countries over the other countries analyzed.
# 
# Once again, for the USA, I can attest that Ed Sheeran, Drake, and Kendrick Lamar were very popular this past year. 
# 
# I'm also fascinated to see that the globe's top 3 artists align with Great Britain's, although at different proportions. 
# 
# I was initially curious to see how top songs compared to the top artists, so here is some insight: although Despacito was a success, Luis Fonsi did not make any country's top 3 artists list. Mask Off was also popular in the USA, but Future was not. These findings show that a top song may be popular in a country, but its artist might not be, or at least not to the song's extent.
# 
# Unfortunately, from these 8 artists, all 8 are male. I am a bit sad to see this, but it's no news that women aren't appreciated as much as men in most industries, music not being an exception to this tale. I am surprised not to see artists like Beyonce, Taylor Swift, Selena Gomez, and Nicki Minaj, because the top songs fall in these artists' specialty: rap, hip-hop, and pop. Hopefully users can bridge the gap between male and female artists after being aware of such a disparity.

# # Conclusions

# The two barplots have discovered some unique insights:
# 1. Shape of You and Ed Sheeran are very popular on Spotify across the globe.
# 2. There is strong correlation between top songs and top artists.
# 3. Not all artists of the top songs are as streamed as their song itself.
# 4. There global preference for top songs and artists aligns pretty well with other countries.
# 5. Many of the non-native English speaking countries' top songs and artists belong to their country.
# 6. Countries with similar cultures share similar music tastes.
# 7. An artist is most streamed in his or her own country.
# 8. The top artists are dominated by men.
# 9. The most streamed songs and artists are of genres hip-hop, rap, and pop.
# 10. The top songs of 2017 were released earlier in the year.

# # Future Work

# In order to fully capture the entirety of this project, a few other ways to explore the data would be:
# 1. Only compare the streams played within the first month of a song's release date.
# 2. Compare more countries, using different visualization techniques, such as a global map or donut visualization.
# 3. Expand to more than the top 3 songs and artists to discover other insights...where are female artists ranked, for instance?
