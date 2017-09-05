
# Summary

1. There are 575 players who made 780 purchases. Total revenue generated is $2,286.33
2. Of the total players, 81% are male players who made purchase of $1867.68
3. 45% of the players are of age between 20-24 years which contributed ~1000$ towords the total revenues.
4. "Undirrala66" is the top spender
5. "Betrayal, Whisper of Grieving Widows" is the most favorite game
6. "Retribution Axe" is the most revenue generated game



```python
import pandas as pd
import numpy as nb
```


```python
file_read=pd.read_json("HeroesOfPymoli/raw_data/purchase_data.json")
```

**Player Count**


```python
# Total Number of Plays
Total_player=file_read["SN"].unique()
Total_counts=Total_player.shape[0]
Total_player_count=pd.DataFrame(pd.Series(Total_player.shape[0]))
Total_player_count.columns=["Total Player"]
Total_player_count

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Player</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>



 **Purchasing Analysis (Total)**


```python
# Number of Unique Items

Unique_items=pd.Series(file_read["Item Name"].unique()).count()
Unique_items
```




    179




```python
# Average Purchase Price
Average_price=file_read["Price"].mean()
Average_price=round(Average_price,2)
```


```python
# Total Number of Purchases
Total_Number_Purchases=file_read["Price"].count()
Total_Number_Purchases
```




    780




```python
# Total Revenue
Total_Revenue=file_read["Price"].sum()
Total_Revenue=round(Total_Revenue,2)
```


```python
Analysis=pd.DataFrame(pd.Series({"Unique Items":Unique_items,"Avg Price":Average_price,"No. Purchases":Total_Number_Purchases,
                "Total Revenue":Total_Revenue})).transpose()

Analysis["Avg Price"]=Analysis["Avg Price"].map('${:,.2f}'.format)
Analysis["Total Revenue"]=Analysis["Total Revenue"].map('${:,.2f}'.format)
Analysis
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Avg Price</th>
      <th>No. Purchases</th>
      <th>Total Revenue</th>
      <th>Unique Items</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>$2.93</td>
      <td>780.0</td>
      <td>$2,286.33</td>
      <td>179.0</td>
    </tr>
  </tbody>
</table>
</div>



**Gender Demographics**






```python

#Percentage and Count of Male Player
maleplayer=file_read.loc[file_read["Gender"]=="Male"]
male_unique=maleplayer["SN"].unique().shape[0]
male_count_percent=(male_unique/Total_counts)*100
male_count_percent=round(male_count_percent,2)

#Percentage and Count of Female Players
Femaleplayer=file_read.loc[file_read["Gender"]=="Female"]
Female_unique=Femaleplayer["SN"].unique().shape[0]
Female_count_percent=(Female_unique/Total_counts)*100
Female_count_percent=round(Female_count_percent,2)
#Percentage and Count of Other / Non-Disclosed
Otherplayer=file_read.loc[file_read["Gender"]=='Other / Non-Disclosed']
Otherplayer_unique=Otherplayer["SN"].unique().shape[0]
Otherplayer_count_percent=(Otherplayer_unique/Total_counts)*100
Otherplayer_count_percent=round(Otherplayer_count_percent,2)

#Display all the data
Demographics_Analysis=pd.DataFrame({"Total Count":[male_unique,Female_unique,Otherplayer_unique],
                                    "Count Percent":[male_count_percent,Female_count_percent,Otherplayer_count_percent]
                                })

Demographics_Analysis.rename(index={0:'Male',1:'Female',2:'Others'},inplace=True)

Demographics_Analysis["Count Percent"]=Demographics_Analysis["Count Percent"].values
Demographics_Analysis["Count Percent"]=Demographics_Analysis["Count Percent"].map('{0:.2f}%'.format)

Demographics_Analysis


```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Count Percent</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15%</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.45%</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Others</th>
      <td>1.40%</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>



# **Purchasing Analysis (Gender)** 

The below each broken by gender:

*1.Male player*

*2.Female player*

*3.Other player*


```python
#Purchase Count
male_unique
Female_unique
Otherplayer_unique

#Average Purchase Price
avg_male_pr=round(maleplayer["Price"].mean(),2)

avg_female_pr=round(Femaleplayer["Price"].mean(),2)

avg_other_pr=round(Otherplayer["Price"].mean(),2)

#Total Purchase Value

Total_Revenue_male=round(maleplayer["Price"].sum(),2)

Total_Revenue_Female=round(Femaleplayer["Price"].sum(),2)

Total_Revenue_Otherplayer=round(Otherplayer["Price"].sum(),2)

#Normalized Totals

Total_male_normalized=round((Total_Revenue_male/male_unique),2)
Total_female_normalized=round(Total_Revenue_Female/Female_unique,2)
Total_Otherplayer_normalized=round(Total_Revenue_Otherplayer/Otherplayer_unique,2)


Purchase_Analysis=pd.DataFrame({"Purchase Count":[male_unique,Female_unique,Otherplayer_unique],
                                "Average Purchase":[avg_male_pr,avg_female_pr,avg_other_pr],
                                "Total Purchase":[Total_Revenue_male,Total_Revenue_Female,Total_Revenue_Otherplayer],
                                "Normalized Totals":[Total_male_normalized,Total_female_normalized,Total_Otherplayer_normalized]
                                })

Purchase_Analysis.rename(index={0:'Male',1:'Female',2:'Others'},inplace=True)
Purchase_Analysis.index.name="Gender"


Purchase_Analysis["Average Purchase"]=Purchase_Analysis["Average Purchase"].map('${:,.2f}'.format)
Purchase_Analysis["Total Purchase"]=Purchase_Analysis["Total Purchase"].map('${:,.2f}'.format)
Purchase_Analysis["Normalized Totals"]=Purchase_Analysis["Normalized Totals"].map('${:,.2f}'.format)

Purchase_Analysis
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase</th>
      <th>Normalized Totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>$2.95</td>
      <td>$4.02</td>
      <td>465</td>
      <td>$1,867.68</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>$2.82</td>
      <td>$3.83</td>
      <td>100</td>
      <td>$382.91</td>
    </tr>
    <tr>
      <th>Others</th>
      <td>$3.25</td>
      <td>$4.47</td>
      <td>8</td>
      <td>$35.74</td>
    </tr>
  </tbody>
</table>
</div>



# **Age Demographics**

* The below each broken into bins of 4 years (i.e. &lt;10, 10-14, 15-19, etc.) 
  * Purchase Count
  * Percent



```python
# age under 10
Age_1=file_read.loc[file_read["Age"]<10]

total_age1_player=Age_1["SN"].unique()
total_age1_player_count=total_age1_player.shape[0]

Total_percent_1= (total_age1_player_count/Total_counts)*100
Total_percent_1=round(Total_percent_1,2)
Total_percent_1


# age between 10 to 15
Age_2=file_read.loc[(file_read["Age"]>=10) & (file_read["Age"]<15)]

total_age2_player=Age_2["SN"].unique()
total_age2_player_count=total_age2_player.shape[0]

Total_percent_2= (total_age2_player_count/Total_counts)*100
Total_percent_2=round(Total_percent_2,2)


# age between 15 to 20
Age_3=file_read.loc[(file_read["Age"]>=15) & (file_read["Age"]<20)]

total_age3_player=Age_3["SN"].unique()
total_age3_player_count=total_age3_player.shape[0]

Total_percent_3= (total_age3_player_count/Total_counts)*100
Total_percent_3=round(Total_percent_3,2)



# age between 20 to 25
Age_4=file_read.loc[(file_read["Age"]>=20) & (file_read["Age"]<25)]

total_age4_player=Age_4["SN"].unique()
total_age4_player_count=total_age4_player.shape[0]

Total_percent_4= (total_age4_player_count/Total_counts)*100
Total_percent_4=round(Total_percent_4,2)


# age between 25 to 30
Age_5=file_read.loc[(file_read["Age"]>=25) & (file_read["Age"]<30)]

total_age5_player=Age_5["SN"].unique()
total_age5_player_count=total_age5_player.shape[0]

Total_percent_5= (total_age5_player_count/Total_counts)*100
Total_percent_5=round(Total_percent_5,2)

# age between 30 to 35
Age_6=file_read.loc[(file_read["Age"]>=30) & (file_read["Age"]<35)]

total_age6_player=Age_6["SN"].unique()
total_age6_player_count=total_age6_player.shape[0]

Total_percent_6= (total_age6_player_count/Total_counts)*100
Total_percent_6=round(Total_percent_6,2)


# age between 35 to 40
Age_7=file_read.loc[(file_read["Age"]>=35) & (file_read["Age"]<40)]

total_age7_player=Age_7["SN"].unique()
total_age7_player_count=total_age7_player.shape[0]

Total_percent_7= (total_age7_player_count/Total_counts)*100
Total_percent_7=round(Total_percent_7,2)

# age above 40
Age_8=file_read.loc[file_read["Age"]>=40]

total_age8_player=Age_8["SN"].unique()
total_age8_player_count=total_age8_player.shape[0]

Total_percent_8= (total_age8_player_count/Total_counts)*100
Total_percent_8=round(Total_percent_8,2)

# create dataframe to display all the values

Age_Demographics=pd.DataFrame({"Total Count":[total_age1_player_count,total_age2_player_count,total_age3_player_count,total_age4_player_count,total_age5_player_count,total_age6_player_count,total_age7_player_count,total_age8_player_count],
                               
                               "Percent Player":[Total_percent_1,Total_percent_2,Total_percent_3,Total_percent_4,Total_percent_5,Total_percent_6,Total_percent_7,Total_percent_8]
                              })

Age_Demographics.rename(index={0:'<10',1:'10-14',2:'15-19',3:'20-24',4:'25-29',5:'30-34',6:'35-39',7:'40+'},inplace=True)

Age_Demographics


```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percent Player</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>3.32</td>
      <td>19</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>4.01</td>
      <td>23</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>17.45</td>
      <td>100</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>45.20</td>
      <td>259</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>15.18</td>
      <td>87</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>8.20</td>
      <td>47</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>4.71</td>
      <td>27</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>1.92</td>
      <td>11</td>
    </tr>
  </tbody>
</table>
</div>



# **Age Demographics**

*The below each broken into bins of 4 years (i.e. <10, 10-14, 15-19, etc.)*

Purchase Count
Average Purchase Price
Total Purchase Value
Normalized Totals


```python
# age under 10



Avg_price_1=round(Age_1["Price"].mean(),2)

Total_Purchase_1=round(Age_1["Price"].sum(),2)

Normalized_total_age1=round(Total_Purchase_1/total_age1_player_count,2)


# age between 10 to 15




Avg_price_2=Age_2["Price"].mean()

Total_Purchase_2=Age_2["Price"].sum()

Normalized_total_age2=round(Total_Purchase_2/total_age2_player_count,2)


# age between 15 to 20



Avg_price_3=round(Age_3["Price"].mean(),2)

Total_Purchase_3=round(Age_3["Price"].sum(),2)

Normalized_total_age3=round(Total_Purchase_3/total_age3_player_count,2)

# age between 20 to 25


Avg_price_4=round(Age_4["Price"].mean(),2)

Total_Purchase_4=round(Age_4["Price"].sum(),2)

Normalized_total_age4=round(Total_Purchase_4/total_age4_player_count,2)


# age between 25 to 30


Avg_price_5=round(Age_5["Price"].mean(),2)

Total_Purchase_5=round(Age_5["Price"].sum(),2)

Normalized_total_age5=round(Total_Purchase_5/total_age5_player_count,2)


# age between 30 to 35




Avg_price_6=round(Age_6["Price"].mean(),2)

Total_Purchase_6=round(Age_6["Price"].sum(),2)

Normalized_total_age6=round(Total_Purchase_6/total_age6_player_count,2)

# age between 35 to 40




Avg_price_7=round(Age_7["Price"].mean(),2)

Total_Purchase_7=round(Age_7["Price"].sum(),2)

Normalized_total_age7=round(Total_Purchase_7/total_age7_player_count,2)

# age above 40



Avg_price_8=round(Age_8["Price"].mean(),2)

Total_Purchase_8=round(Age_8["Price"].sum(),2)

Normalized_total_age8=round(Total_Purchase_8/total_age8_player_count,2)


Age_Demographics=pd.DataFrame({"Purchase Count":[total_age1_player_count,total_age2_player_count,total_age3_player_count,total_age4_player_count,total_age5_player_count,total_age6_player_count,total_age7_player_count,total_age8_player_count],
                               "Average Purchase":[Avg_price_1,Avg_price_2,Avg_price_3,Avg_price_4,Avg_price_5,Avg_price_6,Avg_price_7,Avg_price_8],
                               "Total Purchase":[Total_Purchase_1,Total_Purchase_2,Total_Purchase_3,Total_Purchase_4,Total_Purchase_5,Total_Purchase_6,Total_Purchase_7,Total_Purchase_8],
                               "Normalized Totals":[Normalized_total_age1,Normalized_total_age2,Normalized_total_age3,Normalized_total_age4,Normalized_total_age5,Normalized_total_age6,Normalized_total_age7,Normalized_total_age8]
                                })

Age_Demographics.rename(index={0:'<10',1:'10-14',2:'15-19',3:'20-24',4:'25-29',5:'30-34',6:'35-39',7:'40+'},inplace=True)


Age_Demographics["Average Purchase"]=Age_Demographics["Average Purchase"].map('${:,.2f}'.format)
Age_Demographics["Total Purchase"]=Age_Demographics["Total Purchase"].map('${:,.2f}'.format)
Age_Demographics["Normalized Totals"]=Age_Demographics["Normalized Totals"].map('${:,.2f}'.format)

Age_Demographics


```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase</th>
      <th>Normalized Totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>$2.98</td>
      <td>$4.39</td>
      <td>19</td>
      <td>$83.46</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>$2.77</td>
      <td>$4.22</td>
      <td>23</td>
      <td>$96.95</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>$2.91</td>
      <td>$3.86</td>
      <td>100</td>
      <td>$386.42</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>$2.91</td>
      <td>$3.78</td>
      <td>259</td>
      <td>$978.77</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>$2.96</td>
      <td>$4.26</td>
      <td>87</td>
      <td>$370.33</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>$3.08</td>
      <td>$4.20</td>
      <td>47</td>
      <td>$197.25</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>$2.84</td>
      <td>$4.42</td>
      <td>27</td>
      <td>$119.40</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>$3.16</td>
      <td>$4.89</td>
      <td>11</td>
      <td>$53.75</td>
    </tr>
  </tbody>
</table>
</div>



# **Top Spenders**

* Identify the the top 5 spenders in the game by total purchase value, then list (in a table):
  * SN
  * Purchase Count
  * Average Purchase Price
  * Total Purchase Value


```python
file_group_total=pd.DataFrame(file_read.groupby("SN")["Price"].sum())


file_group_sorted=file_group_total.sort_values("Price",ascending=False)

file_group_max=file_group_sorted.iloc[0:5]

file_group_index=pd.DataFrame(pd.Series(file_group_max.index))

list_max=pd.merge(file_group_index,file_read,on="SN")

list_max_count=pd.DataFrame(pd.Series(list_max.groupby(["SN"])["Item ID"].count()))

list_max_Avg=pd.DataFrame(pd.Series(list_max.groupby(["SN"])["Price"].mean()))

list_max_Avg=list_max_Avg.round(2)

list_max_total=pd.DataFrame(pd.Series(list_max.groupby(["SN"])["Price"].sum()))

spender=list_max_Avg.join(list_max_total,lsuffix=" Avg",rsuffix=" Total", how="outer").join(list_max_count,how="outer")

spender.columns = ['Avg','Total','Count']

spender=spender.sort_values("Count",ascending=False)

spender["Total"]=spender["Total"].map('${:,.2f}'.format)

spender["Avg"]=spender["Avg"].map('${:,.2f}'.format)

spender=spender.sort_values("Total",ascending=False)
spender
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Avg</th>
      <th>Total</th>
      <th>Count</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>$3.41</td>
      <td>$17.06</td>
      <td>5</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>$3.39</td>
      <td>$13.56</td>
      <td>4</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>$3.18</td>
      <td>$12.74</td>
      <td>4</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>$4.24</td>
      <td>$12.73</td>
      <td>3</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>$3.86</td>
      <td>$11.58</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



# **Most Popular Items**

* Identify the 5 most popular items by purchase count, then list (in a table):
  * Item ID
  * Item Name
  * Purchase Count
  * Item Price
  * Total Purchase Value


```python
#popular item

file_group_popular=pd.DataFrame(file_read.groupby("Item ID")["Price"].count())

file_popular_sorted=file_group_popular.sort_values("Price",ascending=False)

file_popular_max=file_popular_sorted.iloc[0:5]

file_popular_index=pd.DataFrame(pd.Series(file_popular_max.index))

list_popular=pd.merge(file_popular_index,file_read,on="Item ID")

popular_ct=pd.DataFrame(pd.Series(list_popular.groupby("Item ID")["Price"].count()))

popular_Price=pd.DataFrame(pd.Series(list_popular.groupby("Item ID")["Price"].sum()))

popular=popular_ct.join(popular_Price,lsuffix="Count",rsuffix="Total",how="outer")

files_import=file_read[["Item ID","Item Name","Price"]]

a=files_import.set_index("Item ID")

a=a.drop_duplicates(subset=None, keep='first', inplace=False)

a

list_pop=a.join(popular, how="inner")

list_pop=list_pop.rename(columns={"PriceCount":"Count","PriceTotal":"Total"})

list_pop["Price"]=list_pop["Price"].map('${:,.2f}'.format)

list_pop["Total"]=list_pop["Total"].map('${:,.2f}'.format)

list_pop=list_pop.sort_values("Count",ascending=False)

list_pop
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Price</th>
      <th>Count</th>
      <th>Total</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <td>Betrayal, Whisper of Grieving Widows</td>
      <td>$2.35</td>
      <td>11</td>
      <td>$25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <td>Arcane Gem</td>
      <td>$2.23</td>
      <td>11</td>
      <td>$24.53</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Serenity</td>
      <td>$1.49</td>
      <td>9</td>
      <td>$13.41</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Trickster</td>
      <td>$2.07</td>
      <td>9</td>
      <td>$18.63</td>
    </tr>
    <tr>
      <th>175</th>
      <td>Woeful Adamantite Claymore</td>
      <td>$1.24</td>
      <td>9</td>
      <td>$11.16</td>
    </tr>
  </tbody>
</table>
</div>



# **Most Profitable Items**

* Identify the 5 most profitable items by total purchase value, then list (in a table):
  * Item ID
  * Item Name
  * Purchase Count
  * Item Price
  * Total Purchase Value


```python


file_purchase=pd.DataFrame(file_read.groupby("Item ID")["Price"].sum())
file_purchase_sorted=file_purchase.sort_values("Price",ascending=False)
file_purchase_max=file_purchase_sorted.iloc[0:5]

profit=file_group_popular.join(file_purchase_max,lsuffix="Count",rsuffix="Total",how="inner").join(a,how="inner")

profit=profit.rename(columns={"PriceCount":"Count","PriceTotal":"Total"})
profit["Total"]=profit["Total"].map('${:,.2f}'.format)
profit["Price"]=profit["Price"].map('${:,.2f}'.format)
profit=profit.sort_values("Total",ascending=False)

profit
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Count</th>
      <th>Total</th>
      <th>Item Name</th>
      <th>Price</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <td>9</td>
      <td>$37.26</td>
      <td>Retribution Axe</td>
      <td>$4.14</td>
    </tr>
    <tr>
      <th>115</th>
      <td>7</td>
      <td>$29.75</td>
      <td>Spectral Diamond Doomblade</td>
      <td>$4.25</td>
    </tr>
    <tr>
      <th>32</th>
      <td>6</td>
      <td>$29.70</td>
      <td>Orenmir</td>
      <td>$4.95</td>
    </tr>
    <tr>
      <th>103</th>
      <td>6</td>
      <td>$29.22</td>
      <td>Singed Scalpel</td>
      <td>$4.87</td>
    </tr>
    <tr>
      <th>107</th>
      <td>8</td>
      <td>$28.88</td>
      <td>Splitter, Foe Of Subtlety</td>
      <td>$3.61</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
