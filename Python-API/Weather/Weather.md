

# Weather Analysis

-Tempeature is comparitive more on the higher value near Equator

-Humidity is more towards North-hamisphere(40 - 60 latitude)

-Cloudiness has no effect with respect to change of latitude

-Wind speed has no relation with change of latitude




```python
#import the dependencies

from citipy import citipy
import random
import csv
import sys
import math
import pandas as pd
import requests as req
import matplotlib.pyplot as plt
import seaborn as sns
import time
import datetime
import os

var1=datetime.datetime.now()

#all the values of api keys

gkey = "AIzaSyDehYwx_mkgNA8qUnS6a4XqALdqaChXwis"
akey="2bf97998be001d3babddbe80bb73edb4"

#all the values of api keys

if os.path.isfile("apikey.csv"):
    key_df=pd.read_csv("apikey.csv")
    akey=key_df.loc[0,'akey']
    gkey=key_df.loc[0,'gkey']
    print("file exist",",akey=",akey)

else:
    akey=input("Enter the Openweather API Key: ")
    gkey=input("Enter the Google API Key: ")
    data = [{'akey': akey,'gkey':gkey}]
    df = pd.DataFrame(data)
    df.to_csv('apikey.csv', index=False)
    print("file do not exist,creating..")
```

    file exist ,akey= 2bf97998be001d3babddbe80bb73edb4



```python
#create empty dataframe to collect all city values and respective weather component

city_df = pd.DataFrame(columns=('Cities', 'Latitude', 'Longitude','Temperature(F)',
                                'Humidity(%)','Cloudiness(%)','Wind Speed(mph)'))

city_df
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
      <th>Cities</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Temperature(F)</th>
      <th>Humidity(%)</th>
      <th>Cloudiness(%)</th>
      <th>Wind Speed(mph)</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>




```python
#assign the values to variable that are need for the programs

radius = 70000                       
r=radius/111300            
call_limit=55
call_sleep=50
citylist=[]
item=1
metric="imperial"
api_counter=0
length=500
count=1
break_count=0

#run the loop till we have required number of rows in the dataframe

while item<=length:
    
#generate random value of lat and lng based on the radius of search

    u = float(random.uniform(1.0,80000.0))
    v = float(random.uniform(1.0,80000.0))
    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    
#find the city near to the lat n lng

    city=citipy.nearest_city(x, y)
    city_name=city.city_name
    country=city.country_code
    namelist=city_name+","+country

#check if the city is already in the generated list.if not creat the url for API call

    if namelist not in citylist:
        
        citylist.append(namelist)
        text=namelist
        url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(text,gkey)
        response=req.get(url).json()

# collect the values of lat and lng of the specific cities

        try:
            lat=response["results"][0]["geometry"]["location"]["lat"]
            lon=response["results"][0]["geometry"]["location"]["lng"]

#deplay the api call to avoid the max limit in openweather API call

            if api_counter>call_limit:
                time.sleep(call_sleep)
                print("time delay")
                api_counter=0
            else:
                api_counter+=1
            

#Created url to get the data from weather api using lat and lng     
                
            url_1="http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=%s&APPID=%s"%(lat,lon,metric,akey)
            response1=req.get(url_1).json()
            
# Value of Temperature,Humidity,Cloudiness,Wind Speed of the city selected

            try:
                temp=response1["main"]["temp_max"]
                humid=response1["main"]["humidity"]
                cloud=response1["clouds"]["all"]
                wnd_speed=response1["wind"]["speed"]
                print("The valid url # %s for location of %s \n %s" %(count,text,url_1))
                count+=1
                
#Entering the values in dataframe
                city_df = city_df.append([{'Cities':text,
                          'Latitude':lat,
                          'Longitude':lon,
                          'Temperature(F)':temp,
                          'Humidity(%)':humid,
                          'Cloudiness(%)':cloud,
                          'Wind Speed(mph)':wnd_speed}],ignore_index=True)
                item+=1

#check the value of the status of the error for openweather API and break if query limit is reached

            except:
                status1=response1["status"]
                
                if "QUERY_LIMIT" in status:
                    
                    print(status1)
                    break_count+=1
                    break
                    
                else:
                    print("Missing values")
                    continue
                    
#check the value of the status of the error for Google API and break if query limit is reached  

        except:
            
                status=response["status"]
                
                if "QUERY_LIMIT" in status:
                    
                    print(status)
                    break_count+=1
                    break
                
                elif break_count>0:
                    
                    break
                    
                else:
                    print("Missing values")
                    continue
                    
#check if the query limit is reached,break out from the program or else continue to find new city                
    else:
        
        if break_count>0:
            
            break
            
        else:
            
            continue
        
city_df 
```

    The valid url # 1 for location of mataura,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=-23.3470634&lon=-149.4850445&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 2 for location of ushuaia,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-54.8019121&lon=-68.3029511&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 3 for location of kirakira,sb 
     http://api.openweathermap.org/data/2.5/weather?lat=-10.4487148&lon=161.8964131&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 4 for location of boyuibe,bo 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.4413004&lon=-63.27982249999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 5 for location of tuktoyaktuk,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=69.445358&lon=-133.034181&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 6 for location of sinnamary,gf 
     http://api.openweathermap.org/data/2.5/weather?lat=5.3746712&lon=-52.9545991&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 7 for location of manaure,co 
     http://api.openweathermap.org/data/2.5/weather?lat=11.772778&lon=-72.444227&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 8 for location of kattivakkam,in 
     http://api.openweathermap.org/data/2.5/weather?lat=12.9682126&lon=80.2599427&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 9 for location of vestmanna,fo 
     http://api.openweathermap.org/data/2.5/weather?lat=62.16316999999999&lon=-7.165286099999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 10 for location of hithadhoo,mv 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.6060574&lon=73.0892245&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 11 for location of qaanaaq,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=77.4670434&lon=-69.2284827&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 12 for location of port elizabeth,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.7139247&lon=25.5207358&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 13 for location of busselton,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.6554927&lon=115.3500188&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 14 for location of hermanus,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-34.4092004&lon=19.2504436&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 15 for location of tocopilla,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.0857976&lon=-70.1930064&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 16 for location of barentsburg,sj 
     http://api.openweathermap.org/data/2.5/weather?lat=78.0648475&lon=14.2334597&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 17 for location of rikitea,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=-23.119901&lon=-134.9702654&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 18 for location of bundaberg,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-24.8669736&lon=152.3509714&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 19 for location of longyearbyen,sj 
     http://api.openweathermap.org/data/2.5/weather?lat=78.22317220000001&lon=15.6267229&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 20 for location of ribeira grande,pt 
     http://api.openweathermap.org/data/2.5/weather?lat=37.8210369&lon=-25.5148137&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 21 for location of corum,tr 
     http://api.openweathermap.org/data/2.5/weather?lat=40.54992560000001&lon=34.9537242&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 22 for location of alofi,nu 
     http://api.openweathermap.org/data/2.5/weather?lat=-19.0553711&lon=-169.9178709&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 23 for location of cape town,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.9248685&lon=18.4240553&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 24 for location of kudahuvadhoo,mv 
     http://api.openweathermap.org/data/2.5/weather?lat=2.6707039&lon=72.8914233&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 25 for location of bowen,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.0014803&lon=148.2262176&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 26 for location of brigham city,us 
     http://api.openweathermap.org/data/2.5/weather?lat=41.5102129&lon=-112.0155015&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 27 for location of port alfred,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.5864065&lon=26.8851448&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 28 for location of ukiah,us 
     http://api.openweathermap.org/data/2.5/weather?lat=39.1501709&lon=-123.2077831&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 29 for location of atuona,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.803279999999999&lon=-139.0425741&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 30 for location of belaya gora,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=68.549671&lon=146.232876&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 31 for location of vila franca do campo,pt 
     http://api.openweathermap.org/data/2.5/weather?lat=37.7157269&lon=-25.4345063&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 32 for location of albany,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-35.0275298&lon=117.883959&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 33 for location of dikson,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=73.50489&lon=80.58091689999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 34 for location of ridgecrest,us 
     http://api.openweathermap.org/data/2.5/weather?lat=35.6224561&lon=-117.6708966&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 35 for location of narsaq,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=60.9129622&lon=-46.0504831&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 36 for location of carnarvon,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-24.884&lon=113.661&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 37 for location of namibe,ao 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.1978317&lon=12.1575544&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 38 for location of airai,pw 
     http://api.openweathermap.org/data/2.5/weather?lat=7.396611799999999&lon=134.5690225&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 39 for location of torbay,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=47.6580777&lon=-52.7355238&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 40 for location of waddan,ly 
     http://api.openweathermap.org/data/2.5/weather?lat=29.1560917&lon=16.1463317&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 41 for location of castro,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-42.4801402&lon=-73.7624137&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 42 for location of arraial do cabo,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.9657374&lon=-42.02798689999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 43 for location of touros,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-5.1961669&lon=-35.4635381&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 44 for location of taolanaro,mg 
     http://api.openweathermap.org/data/2.5/weather?lat=-24.5965316&lon=46.9028375&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 45 for location of bandarbeyla,so 
     http://api.openweathermap.org/data/2.5/weather?lat=9.498579999999999&lon=50.8105261&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 46 for location of jamestown,sh 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.9286343&lon=-5.7151749&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 47 for location of lompoc,us 
     http://api.openweathermap.org/data/2.5/weather?lat=34.6391501&lon=-120.4579409&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 48 for location of khatanga,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=71.964027&lon=102.4406129&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 49 for location of mongoumba,cf 
     http://api.openweathermap.org/data/2.5/weather?lat=3.6378484&lon=18.5908437&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 50 for location of punta arenas,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-53.1638329&lon=-70.9170683&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 51 for location of bambous virieux,mu 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.3438619&lon=57.7636821&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 52 for location of new norfolk,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-42.7828332&lon=147.0593848&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 53 for location of hobart,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-42.8821377&lon=147.3271949&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 54 for location of ucluelet,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=48.9415997&lon=-125.5463446&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 55 for location of young,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-34.3&lon=148.3&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 56 for location of dolbeau,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=48.881683&lon=-72.2321138&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 57 for location of cayenne,gf 
     http://api.openweathermap.org/data/2.5/weather?lat=4.92242&lon=-52.3134531&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 58 for location of port hedland,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.3106621&lon=118.5878223&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 59 for location of ferme-neuve,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=46.8143448&lon=-75.6124452&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 60 for location of faya,td 
     http://api.openweathermap.org/data/2.5/weather?lat=17.9236623&lon=19.1107114&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 61 for location of kodiak,us 
     http://api.openweathermap.org/data/2.5/weather?lat=57.79000000000001&lon=-152.4072221&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 62 for location of naqadeh,ir 
     http://api.openweathermap.org/data/2.5/weather?lat=36.956333&lon=45.3878348&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 63 for location of souillac,mu 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.5180739&lon=57.52638589999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 64 for location of kavieng,pg 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.5781167&lon=150.8086082&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 65 for location of norman wells,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=65.28149379999999&lon=-126.8286524&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 66 for location of palmer,us 
     http://api.openweathermap.org/data/2.5/weather?lat=61.5997222&lon=-149.1127777&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 67 for location of askiz,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=53.14188069999999&lon=90.4372401&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 68 for location of illoqqortoormiut,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=70.48556909999999&lon=-21.9628757&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 69 for location of tura,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=64.2738514&lon=100.2187928&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 70 for location of upernavik,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=72.7862882&lon=-56.1375527&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 71 for location of puerto ayora,ec 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.7432918&lon=-90.3156893&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 72 for location of boende,cd 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.2842862&lon=20.8850949&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 73 for location of bredasdorp,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-34.5385222&lon=20.0568771&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 74 for location of butaritari,ki 
     http://api.openweathermap.org/data/2.5/weather?lat=3.1166667&lon=172.8&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 75 for location of ygatimi,py 
     http://api.openweathermap.org/data/2.5/weather?lat=-24.12219&lon=-55.648449&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 76 for location of severo-kurilsk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=50.66808&lon=156.1138803&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 77 for location of lydenburg,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-25.0815817&lon=30.447285&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 78 for location of naze,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=26.2123124&lon=127.6791568&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    Missing values
    The valid url # 79 for location of saint-philippe,re 
     http://api.openweathermap.org/data/2.5/weather?lat=-21.358118&lon=55.764656&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 80 for location of belushya guba,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=71.54555599999999&lon=52.32027799999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 81 for location of tuatapere,nz 
     http://api.openweathermap.org/data/2.5/weather?lat=-46.1357909&lon=167.6892231&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 82 for location of anloga,gh 
     http://api.openweathermap.org/data/2.5/weather?lat=5.7872343&lon=0.8913523&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 83 for location of bluff,nz 
     http://api.openweathermap.org/data/2.5/weather?lat=-46.5996116&lon=168.3457088&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 84 for location of skopelos,gr 
     http://api.openweathermap.org/data/2.5/weather?lat=39.1251493&lon=23.6799766&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 85 for location of saleaula,ws 
     http://api.openweathermap.org/data/2.5/weather?lat=-13.4482906&lon=-172.3367114&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 86 for location of thompson,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=38.23917&lon=-122.28056&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 87 for location of kefamenanu,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.4442228&lon=124.4780429&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 88 for location of saldanha,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.0276981&lon=17.9176312&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 89 for location of yellowknife,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=62.4539717&lon=-114.3717887&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 90 for location of linxia,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=35.601182&lon=103.210538&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 91 for location of nizhneyansk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=71.450058&lon=136.1122279&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 92 for location of tubruq,ly 
     http://api.openweathermap.org/data/2.5/weather?lat=32.0681759&lon=23.941751&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 93 for location of champerico,gt 
     http://api.openweathermap.org/data/2.5/weather?lat=14.2974022&lon=-91.9087026&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 94 for location of kuito,ao 
     http://api.openweathermap.org/data/2.5/weather?lat=-12.3940412&lon=16.9417632&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 95 for location of mooi river,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-29.2106317&lon=30.0029572&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 96 for location of hilo,us 
     http://api.openweathermap.org/data/2.5/weather?lat=19.7070942&lon=-155.0884869&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 97 for location of kerouane,gn 
     http://api.openweathermap.org/data/2.5/weather?lat=9.2702601&lon=-9.0073673&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 98 for location of ola,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=59.5818476&lon=151.2885614&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 99 for location of canavieiras,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.6752242&lon=-38.9469418&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 100 for location of riachao das neves,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-11.7511866&lon=-44.9146637&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 101 for location of clyde river,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=70.47636500000002&lon=-68.60126509999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 102 for location of mergui,mm 
     http://api.openweathermap.org/data/2.5/weather?lat=12.4492291&lon=98.62706279999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 103 for location of gushikawa,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=26.3577675&lon=127.8691991&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 104 for location of stornoway,gb 
     http://api.openweathermap.org/data/2.5/weather?lat=58.209435&lon=-6.3848692&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 105 for location of kloulklubed,pw 
     http://api.openweathermap.org/data/2.5/weather?lat=7.040244599999999&lon=134.256193&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 106 for location of vardo,no 
     http://api.openweathermap.org/data/2.5/weather?lat=70.37063979999999&lon=31.1095471&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 107 for location of samusu,ws 
     http://api.openweathermap.org/data/2.5/weather?lat=-14.0056774&lon=-171.4299586&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 108 for location of sentyabrskiy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=60.493056&lon=72.19638909999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 109 for location of puerto del rosario,es 
     http://api.openweathermap.org/data/2.5/weather?lat=28.500821&lon=-13.8628367&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 110 for location of cabra,ph 
     http://api.openweathermap.org/data/2.5/weather?lat=53.3578134&lon=-6.2895607&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 111 for location of formoso do araguaia,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-11.8165893&lon=-49.51892650000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 112 for location of vila velha,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.3477821&lon=-40.2949528&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 113 for location of borama,so 
     http://api.openweathermap.org/data/2.5/weather?lat=9.936009199999999&lon=43.184402&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 114 for location of plainfield,us 
     http://api.openweathermap.org/data/2.5/weather?lat=39.70421229999999&lon=-86.39943869999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 115 for location of cidreira,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-30.1768543&lon=-50.2089307&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 116 for location of carbonia,it 
     http://api.openweathermap.org/data/2.5/weather?lat=39.16442809999999&lon=8.522885300000002&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 117 for location of santa cruz de la palma,es 
     http://api.openweathermap.org/data/2.5/weather?lat=28.6839885&lon=-17.7645747&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 118 for location of saint-augustin,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=51.2327688&lon=-58.65154440000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 119 for location of wilmington,us 
     http://api.openweathermap.org/data/2.5/weather?lat=39.7390721&lon=-75.5397878&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 120 for location of vaini,to 
     http://api.openweathermap.org/data/2.5/weather?lat=-21.1935&lon=-175.1751534&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 121 for location of attawapiskat,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=52.9258846&lon=-82.42889219999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 122 for location of katsuura,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=35.152283&lon=140.3209324&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 123 for location of utiroa,ki 
     http://api.openweathermap.org/data/2.5/weather?lat=-1.204189&lon=174.75942&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 124 for location of ancud,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-41.8675003&lon=-73.8276965&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 125 for location of samalaeulu,ws 
     http://api.openweathermap.org/data/2.5/weather?lat=-13.4973599&lon=-172.3105939&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 126 for location of urumqi,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=43.825592&lon=87.61684799999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 127 for location of tiksi,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=71.6374819&lon=128.8644717&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 128 for location of sherlovaya gora,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=50.5245767&lon=116.3409532&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 129 for location of hokitika,nz 
     http://api.openweathermap.org/data/2.5/weather?lat=-42.7173686&lon=170.9665427&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 130 for location of cabo rojo,us 
     http://api.openweathermap.org/data/2.5/weather?lat=36.1721945&lon=-115.3625718&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 131 for location of urfa,tr 
     http://api.openweathermap.org/data/2.5/weather?lat=37.1674039&lon=38.7955149&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 132 for location of grand river south east,mu 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.2888094&lon=57.78141199999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 133 for location of ibanda,ug 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.096489&lon=30.5739579&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 134 for location of de panne,be 
     http://api.openweathermap.org/data/2.5/weather?lat=51.0962794&lon=2.5905629&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 135 for location of kapaa,us 
     http://api.openweathermap.org/data/2.5/weather?lat=22.0881391&lon=-159.3379818&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 136 for location of korla,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=41.725891&lon=86.17463300000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 137 for location of codrington,ag 
     http://api.openweathermap.org/data/2.5/weather?lat=17.6425736&lon=-61.8204456&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 138 for location of bilma,ne 
     http://api.openweathermap.org/data/2.5/weather?lat=18.6929789&lon=12.9176518&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 139 for location of satitoa,ws 
     http://api.openweathermap.org/data/2.5/weather?lat=-14.0287893&lon=-171.4327056&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 140 for location of puerto cabezas,ni 
     http://api.openweathermap.org/data/2.5/weather?lat=14.0391161&lon=-83.39496319999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 141 for location of wamba,cd 
     http://api.openweathermap.org/data/2.5/weather?lat=2.1468409&lon=27.9834738&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 142 for location of olafsvik,is 
     http://api.openweathermap.org/data/2.5/weather?lat=64.89604849999999&lon=-23.7060262&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 143 for location of ixtapa,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=17.6625661&lon=-101.58734&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 144 for location of hofn,is 
     http://api.openweathermap.org/data/2.5/weather?lat=64.24970259999999&lon=-15.2020077&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 145 for location of likhoslavl,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=57.1246162&lon=35.4614485&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 146 for location of aksu,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=41.167548&lon=80.263387&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 147 for location of port macquarie,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-31.433333&lon=152.9&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 148 for location of lieksa,fi 
     http://api.openweathermap.org/data/2.5/weather?lat=63.3185051&lon=30.02645279999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 149 for location of iqaluit,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=63.74669300000001&lon=-68.5169669&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 150 for location of mangochi,mw 
     http://api.openweathermap.org/data/2.5/weather?lat=-14.4861733&lon=35.253304&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 151 for location of camocim,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.9014475&lon=-40.8388865&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 152 for location of harper,lr 
     http://api.openweathermap.org/data/2.5/weather?lat=4.3759676&lon=-7.700941599999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 153 for location of banswara,in 
     http://api.openweathermap.org/data/2.5/weather?lat=23.5461394&lon=74.4349761&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 154 for location of tulu bolo,et 
     http://api.openweathermap.org/data/2.5/weather?lat=8.663281399999999&lon=38.2163717&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 155 for location of sechura,pe 
     http://api.openweathermap.org/data/2.5/weather?lat=-5.5622396&lon=-80.8187744&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 156 for location of burns lake,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=54.2334148&lon=-125.763613&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 157 for location of ahipara,nz 
     http://api.openweathermap.org/data/2.5/weather?lat=-35.17133889999999&lon=173.1532718&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 158 for location of klaksvik,fo 
     http://api.openweathermap.org/data/2.5/weather?lat=62.2271922&lon=-6.5779064&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 159 for location of cocobeach,ga 
     http://api.openweathermap.org/data/2.5/weather?lat=0.9931336&lon=9.5770844&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 160 for location of kahului,us 
     http://api.openweathermap.org/data/2.5/weather?lat=20.8893351&lon=-156.4729469&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 161 for location of zamora,es 
     http://api.openweathermap.org/data/2.5/weather?lat=41.5034712&lon=-5.7467879&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 162 for location of fairmont,us 
     http://api.openweathermap.org/data/2.5/weather?lat=39.4850848&lon=-80.1425781&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 163 for location of naples,us 
     http://api.openweathermap.org/data/2.5/weather?lat=26.1420358&lon=-81.7948103&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 164 for location of chokurdakh,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=70.622169&lon=147.916168&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 165 for location of victoria,us 
     http://api.openweathermap.org/data/2.5/weather?lat=28.8052674&lon=-97.0035982&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 166 for location of noumea,nc 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.2558234&lon=166.4505243&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 167 for location of lasa,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=29.652491&lon=91.17210999999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 168 for location of avarua,ck 
     http://api.openweathermap.org/data/2.5/weather?lat=-21.2129007&lon=-159.7823059&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 169 for location of brookings,us 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3113573&lon=-96.79838769999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 170 for location of vostok,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=46.4467186&lon=135.825196&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 171 for location of yulara,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-25.2334936&lon=130.9848698&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 172 for location of dukat,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=47.216351&lon=39.63639&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 173 for location of rokytnice nad jizerou,cz 
     http://api.openweathermap.org/data/2.5/weather?lat=50.7291276&lon=15.4486873&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 174 for location of barrow,us 
     http://api.openweathermap.org/data/2.5/weather?lat=71.29055559999999&lon=-156.788611&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 175 for location of nushki,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=29.5558052&lon=66.0195894&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 176 for location of saryozek,kz 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3590349&lon=77.9681544&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 177 for location of senanga,zm 
     http://api.openweathermap.org/data/2.5/weather?lat=-16.1178235&lon=23.2960171&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 178 for location of hirara,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=24.8051928&lon=125.2789544&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 179 for location of qaqortoq,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=60.71898640000001&lon=-46.03534579999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 180 for location of rudnaya pristan,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3630667&lon=135.8151076&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 181 for location of kochubey,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3912121&lon=46.5565748&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 182 for location of necochea,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-38.5544968&lon=-58.73960879999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 183 for location of santa rosalia,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=27.3361939&lon=-112.2701486&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 184 for location of bajah,tn 
     http://api.openweathermap.org/data/2.5/weather?lat=36.7333193&lon=9.1843676&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 185 for location of marsh harbour,bs 
     http://api.openweathermap.org/data/2.5/weather?lat=26.5241653&lon=-77.09098089999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 186 for location of cabo san lucas,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=22.8905327&lon=-109.9167371&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 187 for location of palabuhanratu,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-6.9852341&lon=106.5475399&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 188 for location of praia da vitoria,pt 
     http://api.openweathermap.org/data/2.5/weather?lat=38.7339162&lon=-27.0646976&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 189 for location of sitka,us 
     http://api.openweathermap.org/data/2.5/weather?lat=57.0530556&lon=-135.33&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 190 for location of faanui,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=-16.5004126&lon=-151.7414904&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 191 for location of srednekolymsk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=67.43730699999999&lon=153.728674&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    Missing values
    The valid url # 192 for location of mahebourg,mu 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.4059505&lon=57.7034222&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 193 for location of trincomalee,lk 
     http://api.openweathermap.org/data/2.5/weather?lat=8.5873638&lon=81.2152121&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 194 for location of abha,sa 
     http://api.openweathermap.org/data/2.5/weather?lat=18.2464685&lon=42.5117238&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 195 for location of gijon,es 
     http://api.openweathermap.org/data/2.5/weather?lat=43.5322015&lon=-5.6611195&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 196 for location of kortkeros,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=61.81713560000001&lon=51.5568693&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 197 for location of honningsvag,no 
     http://api.openweathermap.org/data/2.5/weather?lat=70.9822909&lon=25.9702075&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 198 for location of nanortalik,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=60.1424955&lon=-45.2394951&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 199 for location of pierre,us 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3683156&lon=-100.3509665&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 200 for location of kawalu,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-7.410349200000001&lon=108.2021667&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 201 for location of luderitz,na 
     http://api.openweathermap.org/data/2.5/weather?lat=-26.6420382&lon=15.1639082&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 202 for location of ambilobe,mg 
     http://api.openweathermap.org/data/2.5/weather?lat=-13.2026069&lon=49.0514094&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 203 for location of praia,cv 
     http://api.openweathermap.org/data/2.5/weather?lat=14.93305&lon=-23.5133267&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 204 for location of hasaki,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=35.7453776&lon=140.8272903&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 205 for location of batesville,us 
     http://api.openweathermap.org/data/2.5/weather?lat=35.769799&lon=-91.6409721&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 206 for location of avera,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=-16.789539&lon=-151.4099893&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 207 for location of comodoro rivadavia,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-45.8656149&lon=-67.4822429&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 208 for location of kruisfontein,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.9843356&lon=24.732102&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 209 for location of amurzet,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=47.6999935&lon=131.1243299&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 210 for location of saint-pierre,pm 
     http://api.openweathermap.org/data/2.5/weather?lat=46.8852&lon=-56.3159&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 211 for location of sarh,td 
     http://api.openweathermap.org/data/2.5/weather?lat=9.141208599999999&lon=18.3682641&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 212 for location of bethel,us 
     http://api.openweathermap.org/data/2.5/weather?lat=40.6098147&lon=-122.3585019&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 213 for location of nantucket,us 
     http://api.openweathermap.org/data/2.5/weather?lat=41.2834704&lon=-70.099451&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 214 for location of tasiilaq,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=65.6134561&lon=-37.6335696&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 215 for location of aklavik,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=68.219916&lon=-135.0077881&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 216 for location of tucurui,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-3.8036143&lon=-49.7728757&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 217 for location of maragogi,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.010379799999999&lon=-35.2208051&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 218 for location of ponta do sol,cv 
     http://api.openweathermap.org/data/2.5/weather?lat=17.2004826&lon=-25.0925624&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 219 for location of marienburg,sr 
     http://api.openweathermap.org/data/2.5/weather?lat=5.8467655&lon=-55.0507157&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 220 for location of buchanan,lr 
     http://api.openweathermap.org/data/2.5/weather?lat=5.887246999999999&lon=-10.0303723&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 221 for location of hobyo,so 
     http://api.openweathermap.org/data/2.5/weather?lat=5.3515922&lon=48.5249751&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 222 for location of ketchikan,us 
     http://api.openweathermap.org/data/2.5/weather?lat=55.34222219999999&lon=-131.6461112&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 223 for location of east london,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.0291582&lon=27.8545867&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 224 for location of kalanguy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=51.01920459999999&lon=116.5108072&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 225 for location of yaan,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=29.980537&lon=103.013261&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 226 for location of college,us 
     http://api.openweathermap.org/data/2.5/weather?lat=41.5077578&lon=-71.3300034&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 227 for location of esperance,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.8608027&lon=121.8896205&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 228 for location of pangnirtung,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=66.1465578&lon=-65.7012182&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 229 for location of mar del plata,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-38.0054771&lon=-57.5426106&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 230 for location of georgetown,sh 
     http://api.openweathermap.org/data/2.5/weather?lat=-7.926222999999999&lon=-14.4112011&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 231 for location of chuy,uy 
     http://api.openweathermap.org/data/2.5/weather?lat=-33.692754&lon=-53.4552817&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 232 for location of descalvado,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-21.9159262&lon=-47.6202824&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 233 for location of manjakandriana,mg 
     http://api.openweathermap.org/data/2.5/weather?lat=-18.9105687&lon=47.8081645&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 234 for location of lorengau,pg 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.0349854&lon=147.279039&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 235 for location of hovd,mn 
     http://api.openweathermap.org/data/2.5/weather?lat=47.1129654&lon=92.31107519999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 236 for location of zhucheng,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=35.995654&lon=119.410103&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 237 for location of marcona,pe 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.3439659&lon=-75.0844757&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 238 for location of vanimo,pg 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.6896767&lon=141.2998457&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 239 for location of port hardy,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=50.7123867&lon=-127.460393&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 240 for location of saskylakh,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=71.954308&lon=114.1198349&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 241 for location of calabar,ng 
     http://api.openweathermap.org/data/2.5/weather?lat=4.9757165&lon=8.3417006&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 242 for location of half moon bay,us 
     http://api.openweathermap.org/data/2.5/weather?lat=37.4635519&lon=-122.4285862&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 243 for location of markova,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=56.1081477&lon=66.5604504&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 244 for location of port lincoln,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-34.7301943&lon=135.8504838&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 245 for location of broome,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-17.9614336&lon=122.235852&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 246 for location of okhotsk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=59.35845999999999&lon=143.2034909&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 247 for location of riyadh,sa 
     http://api.openweathermap.org/data/2.5/weather?lat=24.7135517&lon=46.6752957&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 248 for location of ekhabi,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=53.50858299999999&lon=142.96743&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 249 for location of ilulissat,gl 
     http://api.openweathermap.org/data/2.5/weather?lat=69.2198118&lon=-51.0986031&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 250 for location of solnechnyy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=50.726608&lon=136.644272&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 251 for location of tyshkivka,ua 
     http://api.openweathermap.org/data/2.5/weather?lat=48.4978938&lon=30.9365392&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 252 for location of mandera,ke 
     http://api.openweathermap.org/data/2.5/weather?lat=3.3873803&lon=40.6458786&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 253 for location of dingle,ie 
     http://api.openweathermap.org/data/2.5/weather?lat=52.14093889999999&lon=-10.2640135&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 254 for location of walvis bay,na 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.9389587&lon=14.5247463&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 255 for location of greensboro,us 
     http://api.openweathermap.org/data/2.5/weather?lat=36.0726354&lon=-79.7919754&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 256 for location of mabaruma,gy 
     http://api.openweathermap.org/data/2.5/weather?lat=8.2041293&lon=-59.7775773&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 257 for location of shimoda,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=34.6795334&lon=138.945316&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 258 for location of jerez,es 
     http://api.openweathermap.org/data/2.5/weather?lat=36.6850064&lon=-6.126074399999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 259 for location of saint george,bm 
     http://api.openweathermap.org/data/2.5/weather?lat=32.3819877&lon=-64.6769793&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 260 for location of sungai besar,my 
     http://api.openweathermap.org/data/2.5/weather?lat=3.675398&lon=100.9857899&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 261 for location of fare,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=39.967072&lon=-75.171281&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 262 for location of katsiveli,ua 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3934152&lon=33.9715074&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 263 for location of ban bung,th 
     http://api.openweathermap.org/data/2.5/weather?lat=13.2878094&lon=101.1051259&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 264 for location of victoria,sc 
     http://api.openweathermap.org/data/2.5/weather?lat=-4.619143&lon=55.4513149&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 265 for location of toledo,co 
     http://api.openweathermap.org/data/2.5/weather?lat=7.307025&lon=-72.48044399999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 266 for location of sabha,ly 
     http://api.openweathermap.org/data/2.5/weather?lat=27.0087129&lon=14.4490398&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 267 for location of turukhansk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=65.79585999999999&lon=87.962418&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 268 for location of kupang,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-10.1771997&lon=123.6070329&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 269 for location of guacara,ve 
     http://api.openweathermap.org/data/2.5/weather?lat=10.2646995&lon=-67.8927472&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 270 for location of bengkulu,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-3.5778471&lon=102.3463875&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 271 for location of domoni,km 
     http://api.openweathermap.org/data/2.5/weather?lat=-12.2632051&lon=44.5290018&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 272 for location of mattru,sl 
     http://api.openweathermap.org/data/2.5/weather?lat=7.6042266&lon=-12.1718486&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 273 for location of chicama,pe 
     http://api.openweathermap.org/data/2.5/weather?lat=-7.847994799999999&lon=-79.1407421&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 274 for location of honiara,sb 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.4456381&lon=159.9728999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 275 for location of botwood,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=49.1422983&lon=-55.3440853&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 276 for location of metro,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-5.117839399999999&lon=105.3072646&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 277 for location of marawi,sd 
     http://api.openweathermap.org/data/2.5/weather?lat=18.523319&lon=31.82962&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 278 for location of tahta,eg 
     http://api.openweathermap.org/data/2.5/weather?lat=26.7647964&lon=31.4982868&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 279 for location of haines junction,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=60.7544541&lon=-137.5117819&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 280 for location of lukulu,zm 
     http://api.openweathermap.org/data/2.5/weather?lat=-14.4076036&lon=23.2587992&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 281 for location of kalmunai,lk 
     http://api.openweathermap.org/data/2.5/weather?lat=7.414383099999999&lon=81.8306334&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 282 for location of vicuna,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-30.0319&lon=-70.7081&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    Missing values
    The valid url # 283 for location of lebu,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-37.6097143&lon=-73.6483294&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 284 for location of naruja,ge 
     http://api.openweathermap.org/data/2.5/weather?lat=41.9087741&lon=41.958701&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 285 for location of burica,pa 
     http://api.openweathermap.org/data/2.5/weather?lat=8.9933743&lon=-79.5388265&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 286 for location of ostrovnoy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=45.8124109&lon=135.2848966&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 287 for location of te anau,nz 
     http://api.openweathermap.org/data/2.5/weather?lat=-45.4144515&lon=167.718053&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 288 for location of kuche,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=41.717906&lon=82.96201599999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 289 for location of othaya,ke 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.5517506999999999&lon=36.9447027&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 290 for location of nyurba,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=63.2803099&lon=118.3618985&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 291 for location of seydi,tm 
     http://api.openweathermap.org/data/2.5/weather?lat=39.4286365&lon=62.86175960000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 292 for location of duncan,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=48.7786908&lon=-123.7079417&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 293 for location of sobolevo,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=54.300693&lon=155.956757&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 294 for location of lujan,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-34.5633312&lon=-59.1208805&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 295 for location of muros,es 
     http://api.openweathermap.org/data/2.5/weather?lat=42.8073676&lon=-9.0460525&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 296 for location of asau,tv 
     http://api.openweathermap.org/data/2.5/weather?lat=-7.488197&lon=178.6807179&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 297 for location of gerash,ir 
     http://api.openweathermap.org/data/2.5/weather?lat=27.6903817&lon=54.1501922&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 298 for location of cambridge,us 
     http://api.openweathermap.org/data/2.5/weather?lat=42.3736158&lon=-71.10973349999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 299 for location of nguiu,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-11.7608881&lon=130.6330634&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 300 for location of rockhampton,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-23.3790772&lon=150.510016&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 301 for location of pisco,pe 
     http://api.openweathermap.org/data/2.5/weather?lat=-13.7134562&lon=-76.1841701&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 302 for location of berlevag,no 
     http://api.openweathermap.org/data/2.5/weather?lat=70.7198284&lon=29.0300862&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 303 for location of bageshwar,in 
     http://api.openweathermap.org/data/2.5/weather?lat=29.8403606&lon=79.769426&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 304 for location of chaihe,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=47.562627&lon=121.315016&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 305 for location of husavik,is 
     http://api.openweathermap.org/data/2.5/weather?lat=66.0449706&lon=-17.3383442&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 306 for location of luwuk,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.938828&lon=122.792801&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 307 for location of pacific grove,us 
     http://api.openweathermap.org/data/2.5/weather?lat=36.6177374&lon=-121.9166215&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 308 for location of the valley,ai 
     http://api.openweathermap.org/data/2.5/weather?lat=18.2148129&lon=-63.0574406&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 309 for location of wheeling,us 
     http://api.openweathermap.org/data/2.5/weather?lat=40.0639616&lon=-80.7209149&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 310 for location of encruzilhada,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.5306298&lon=-40.91280940000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 311 for location of morro bay,us 
     http://api.openweathermap.org/data/2.5/weather?lat=35.3659445&lon=-120.8499924&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 312 for location of rupert,us 
     http://api.openweathermap.org/data/2.5/weather?lat=42.6190756&lon=-113.6772348&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 313 for location of alta floresta,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.8764576&lon=-56.08550899999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 314 for location of hamilton,bm 
     http://api.openweathermap.org/data/2.5/weather?lat=32.2945837&lon=-64.7858887&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 315 for location of murray bridge,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-35.1311491&lon=139.2650902&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 316 for location of humaita,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-7.5169578&lon=-63.0298013&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 317 for location of nuevo progreso,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=26.0498321&lon=-97.9511137&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 318 for location of raudeberg,no 
     http://api.openweathermap.org/data/2.5/weather?lat=61.9829132&lon=5.1351057&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 319 for location of manado,id 
     http://api.openweathermap.org/data/2.5/weather?lat=1.4748305&lon=124.8420794&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 320 for location of rantepao,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.9703732&lon=119.8757349&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 321 for location of korsakov,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=46.6353796&lon=142.7841876&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 322 for location of ranong,th 
     http://api.openweathermap.org/data/2.5/weather?lat=9.9528702&lon=98.60846409999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 323 for location of aksha,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=50.2850778&lon=113.2766861&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 324 for location of cabedelo,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-6.966667&lon=-34.833333&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 325 for location of saint-joseph,re 
     http://api.openweathermap.org/data/2.5/weather?lat=-21.3246183&lon=55.64675829999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 326 for location of sicamous,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=50.8378243&lon=-118.9768156&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 327 for location of bereda,so 
     http://api.openweathermap.org/data/2.5/weather?lat=37.7538318&lon=-122.4206972&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 328 for location of colombia,cu 
     http://api.openweathermap.org/data/2.5/weather?lat=20.9874938&lon=-77.4185584&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 329 for location of balaipungut,id 
     http://api.openweathermap.org/data/2.5/weather?lat=1.0710103&lon=101.2920619&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 330 for location of general roca,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-39.032803&lon=-67.5892227&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 331 for location of turbat,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=26.0080546&lon=63.03830589999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 332 for location of kaitangata,nz 
     http://api.openweathermap.org/data/2.5/weather?lat=-46.28334&lon=169.8470967&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 333 for location of cap-aux-meules,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=47.3777379&lon=-61.8713553&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 334 for location of gunjur,gm 
     http://api.openweathermap.org/data/2.5/weather?lat=13.1806725&lon=-16.7559004&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 335 for location of cherskiy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=68.742677&lon=161.3507839&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 336 for location of yumen,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=40.29184300000001&lon=97.04567800000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 337 for location of san jeronimo,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=20.4061494&lon=-103.9854708&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 338 for location of san quintin,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=30.56087669999999&lon=-115.9379302&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 339 for location of hasilpur,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=29.69025499999999&lon=72.53822930000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 340 for location of la ronge,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=55.10823&lon=-105.285989&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 341 for location of kongolo,cd 
     http://api.openweathermap.org/data/2.5/weather?lat=-5.387502&lon=26.9911288&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 342 for location of san ramon,bo 
     http://api.openweathermap.org/data/2.5/weather?lat=37.7799273&lon=-121.9780153&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 343 for location of trinidad,cu 
     http://api.openweathermap.org/data/2.5/weather?lat=21.7960343&lon=-79.98081429999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 344 for location of amderma,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=69.751221&lon=61.6636961&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 345 for location of mirnyy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=62.5313374&lon=113.9773882&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 346 for location of boyabat,tr 
     http://api.openweathermap.org/data/2.5/weather?lat=41.46610500000001&lon=34.7711201&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 347 for location of saveh,ir 
     http://api.openweathermap.org/data/2.5/weather?lat=35.0236107&lon=50.3585065&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 348 for location of geraldton,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-28.7773715&lon=114.6149715&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 349 for location of makakilo city,us 
     http://api.openweathermap.org/data/2.5/weather?lat=21.3469444&lon=-158.0858333&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 350 for location of kungurtug,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=50.595182&lon=97.519958&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 351 for location of grand gaube,mu 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.014212&lon=57.6694082&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 352 for location of derzhavinsk,kz 
     http://api.openweathermap.org/data/2.5/weather?lat=51.098127&lon=66.3165471&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 353 for location of teguldet,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=57.304527&lon=88.17174899999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 354 for location of hunza,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=36.316666&lon=74.64998630000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 355 for location of vikindu,tz 
     http://api.openweathermap.org/data/2.5/weather?lat=-6.9739803&lon=39.2881866&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 356 for location of tautira,pf 
     http://api.openweathermap.org/data/2.5/weather?lat=-17.74932&lon=-149.160155&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 357 for location of saint-francois,gp 
     http://api.openweathermap.org/data/2.5/weather?lat=16.2542635&lon=-61.283115&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 358 for location of sokolo,ml 
     http://api.openweathermap.org/data/2.5/weather?lat=14.7384717&lon=-6.118242899999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 359 for location of rincon,an 
     http://api.openweathermap.org/data/2.5/weather?lat=33.7415031&lon=-117.840052&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 360 for location of baft,ir 
     http://api.openweathermap.org/data/2.5/weather?lat=29.233038&lon=56.60089720000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 361 for location of black river,jm 
     http://api.openweathermap.org/data/2.5/weather?lat=18.0335359&lon=-77.85673799999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 362 for location of hami,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=42.81842&lon=93.51514999999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 363 for location of mayo,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=63.59426199999999&lon=-135.8964919&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 364 for location of toba,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=34.481435&lon=136.8433615&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 365 for location of mount isa,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.7255748&lon=139.4927085&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 366 for location of mogadishu,so 
     http://api.openweathermap.org/data/2.5/weather?lat=2.0469343&lon=45.3181623&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 367 for location of alappuzha,in 
     http://api.openweathermap.org/data/2.5/weather?lat=9.498066699999999&lon=76.3388484&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 368 for location of jati,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=24.3552401&lon=68.26685379999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 369 for location of tall kayf,iq 
     http://api.openweathermap.org/data/2.5/weather?lat=36.4907739&lon=43.1199722&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 370 for location of nouakchott,mr 
     http://api.openweathermap.org/data/2.5/weather?lat=18.0735299&lon=-15.9582372&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 371 for location of guerrero negro,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=27.9591758&lon=-114.056646&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 372 for location of cadiz,es 
     http://api.openweathermap.org/data/2.5/weather?lat=36.5270612&lon=-6.2885962&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 373 for location of itarema,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.9209642&lon=-39.91673979999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 374 for location of winnemucca,us 
     http://api.openweathermap.org/data/2.5/weather?lat=40.9729584&lon=-117.7356849&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 375 for location of kiruna,se 
     http://api.openweathermap.org/data/2.5/weather?lat=67.8557995&lon=20.225282&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 376 for location of sala consilina,it 
     http://api.openweathermap.org/data/2.5/weather?lat=40.4019157&lon=15.5908015&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 377 for location of rosarito,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=32.3661011&lon=-117.0617553&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 378 for location of smiltene,lv 
     http://api.openweathermap.org/data/2.5/weather?lat=57.42306300000001&lon=25.900378&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 379 for location of usinsk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=65.9991695&lon=57.5243292&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 380 for location of kenai,us 
     http://api.openweathermap.org/data/2.5/weather?lat=60.55444439999999&lon=-151.2583333&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 381 for location of tabas,ir 
     http://api.openweathermap.org/data/2.5/weather?lat=33.6033455&lon=56.9323531&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 382 for location of krasnovishersk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=60.4050484&lon=57.0720287&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 383 for location of andilamena,mg 
     http://api.openweathermap.org/data/2.5/weather?lat=-17.0127475&lon=48.57126299999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 384 for location of pangkalanbuun,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-2.688962000000001&lon=111.622398&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 385 for location of talesh,ir 
     http://api.openweathermap.org/data/2.5/weather?lat=37.8016324&lon=48.907262&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 386 for location of mayskiy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=43.63639149999999&lon=44.0628764&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 387 for location of san vicente,ph 
     http://api.openweathermap.org/data/2.5/weather?lat=10.5126542&lon=119.3645562&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 388 for location of kemijarvi,fi 
     http://api.openweathermap.org/data/2.5/weather?lat=66.7136282&lon=27.4292063&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 389 for location of mbandaka,cd 
     http://api.openweathermap.org/data/2.5/weather?lat=0.0265717&lon=18.2970692&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 390 for location of marica,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.9160994&lon=-42.819192&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 391 for location of tvoroyri,fo 
     http://api.openweathermap.org/data/2.5/weather?lat=61.5557494&lon=-6.811948&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 392 for location of bataipora,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.2951897&lon=-53.2715408&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 393 for location of itoman,jp 
     http://api.openweathermap.org/data/2.5/weather?lat=26.1235841&lon=127.6658145&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 394 for location of ulaangom,mn 
     http://api.openweathermap.org/data/2.5/weather?lat=49.9903359&lon=92.0557583&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 395 for location of nalut,ly 
     http://api.openweathermap.org/data/2.5/weather?lat=31.8742348&lon=10.9750484&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 396 for location of goderich,sl 
     http://api.openweathermap.org/data/2.5/weather?lat=8.427560999999999&lon=-13.285784&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 397 for location of seoul,kr 
     http://api.openweathermap.org/data/2.5/weather?lat=37.566535&lon=126.9779692&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 398 for location of kokkola,fi 
     http://api.openweathermap.org/data/2.5/weather?lat=63.8415002&lon=23.1250337&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 399 for location of talnakh,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=69.5&lon=88.39999999999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 400 for location of macaboboni,ph 
     http://api.openweathermap.org/data/2.5/weather?lat=16.1952956&lon=119.7802409&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 401 for location of wadena,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=51.94450699999999&lon=-103.80147&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 402 for location of buqayq,sa 
     http://api.openweathermap.org/data/2.5/weather?lat=25.9168154&lon=49.67072049999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 403 for location of la palma,pa 
     http://api.openweathermap.org/data/2.5/weather?lat=40.6035139&lon=-75.4790678&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 404 for location of coihaique,cl 
     http://api.openweathermap.org/data/2.5/weather?lat=-45.5712254&lon=-72.068265&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 405 for location of pedasi,pa 
     http://api.openweathermap.org/data/2.5/weather?lat=7.5202138&lon=-80.0758425&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 406 for location of prieska,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-29.7069446&lon=22.739048&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 407 for location of ormara,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=25.2665929&lon=64.6095785&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 408 for location of sao joao da barra,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-21.6368446&lon=-41.0484428&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 409 for location of igrim,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=63.19083319999999&lon=64.4183685&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 410 for location of bentiu,sd 
     http://api.openweathermap.org/data/2.5/weather?lat=9.231487&lon=29.8005027&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 411 for location of bambanglipuro,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-7.9481229&lon=110.3130087&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 412 for location of turan,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=52.1421176&lon=93.92106509999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 413 for location of sao joao dos patos,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-6.4937893&lon=-43.7039903&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 414 for location of barcelos,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.2674076&lon=-63.2032151&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 415 for location of tumannyy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=68.878911&lon=35.6675264&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 416 for location of fortuna,us 
     http://api.openweathermap.org/data/2.5/weather?lat=40.5981867&lon=-124.1572756&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 417 for location of mount gambier,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-37.8284212&lon=140.7803529&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 418 for location of gat,ly 
     http://api.openweathermap.org/data/2.5/weather?lat=24.509445&lon=118.1089531&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 419 for location of tilichiki,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=60.43333299999999&lon=166.0486109&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 420 for location of dolinsk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=47.3350064&lon=142.7899519&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 421 for location of kabalo,cd 
     http://api.openweathermap.org/data/2.5/weather?lat=-6.0329665&lon=26.9263671&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 422 for location of padang,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-0.9470831999999999&lon=100.417181&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 423 for location of batemans bay,au 
     http://api.openweathermap.org/data/2.5/weather?lat=-35.7143871&lon=150.1794707&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 424 for location of peniche,pt 
     http://api.openweathermap.org/data/2.5/weather?lat=39.3603291&lon=-9.387622&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 425 for location of porbandar,in 
     http://api.openweathermap.org/data/2.5/weather?lat=21.6417069&lon=69.6292654&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 426 for location of baherden,tm 
     http://api.openweathermap.org/data/2.5/weather?lat=38.4361809&lon=57.42878990000001&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 427 for location of miles city,us 
     http://api.openweathermap.org/data/2.5/weather?lat=46.4083362&lon=-105.8405582&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 428 for location of waingapu,id 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.738685799999999&lon=120.182022&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 429 for location of maimon,do 
     http://api.openweathermap.org/data/2.5/weather?lat=18.9066115&lon=-70.2735719&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 430 for location of las conchas,hn 
     http://api.openweathermap.org/data/2.5/weather?lat=13.3238027&lon=-87.3971964&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 431 for location of sao filipe,cv 
     http://api.openweathermap.org/data/2.5/weather?lat=14.8951679&lon=-24.4945636&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 432 for location of bikaner,in 
     http://api.openweathermap.org/data/2.5/weather?lat=28.0229348&lon=73.3119159&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 433 for location of liwale,tz 
     http://api.openweathermap.org/data/2.5/weather?lat=-9.8012675&lon=37.9201751&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 434 for location of andenes,no 
     http://api.openweathermap.org/data/2.5/weather?lat=69.31607989999999&lon=16.1202285&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 435 for location of linchuan,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=27.934572&lon=116.312166&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 436 for location of mayumba,ga 
     http://api.openweathermap.org/data/2.5/weather?lat=-3.4426092&lon=10.6562606&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 437 for location of salaverry,pe 
     http://api.openweathermap.org/data/2.5/weather?lat=-8.2141205&lon=-78.97689989999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 438 for location of ituporanga,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-27.4156778&lon=-49.603384&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 439 for location of altay,cn 
     http://api.openweathermap.org/data/2.5/weather?lat=47.844924&lon=88.14125299999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 440 for location of acari,pe 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.4384565&lon=-74.6180833&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 441 for location of scarborough,gb 
     http://api.openweathermap.org/data/2.5/weather?lat=54.283113&lon=-0.399752&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 442 for location of shahdadkot,pk 
     http://api.openweathermap.org/data/2.5/weather?lat=27.848312&lon=67.91063179999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 443 for location of sidney,us 
     http://api.openweathermap.org/data/2.5/weather?lat=41.1448219&lon=-102.9774497&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 444 for location of salihorsk,by 
     http://api.openweathermap.org/data/2.5/weather?lat=52.7899466&lon=27.5359617&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 445 for location of mormugao,in 
     http://api.openweathermap.org/data/2.5/weather?lat=15.3874352&lon=73.8154394&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 446 for location of quarai,br 
     http://api.openweathermap.org/data/2.5/weather?lat=-30.3845133&lon=-56.4488086&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 447 for location of ponta delgada,pt 
     http://api.openweathermap.org/data/2.5/weather?lat=37.7428301&lon=-25.6805868&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 448 for location of umm lajj,sa 
     http://api.openweathermap.org/data/2.5/weather?lat=25.026409&lon=37.27076&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 449 for location of panchagarh,bd 
     http://api.openweathermap.org/data/2.5/weather?lat=26.2708705&lon=88.59517509999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 450 for location of miramar,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=22.3384943&lon=-97.87006389999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 451 for location of mahajanga,mg 
     http://api.openweathermap.org/data/2.5/weather?lat=-15.6921494&lon=46.3336857&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 452 for location of luba,gq 
     http://api.openweathermap.org/data/2.5/weather?lat=3.4590145&lon=8.552874599999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 453 for location of libertador general san martin,ar 
     http://api.openweathermap.org/data/2.5/weather?lat=-23.8153322&lon=-64.7928261&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 454 for location of sandnessjoen,no 
     http://api.openweathermap.org/data/2.5/weather?lat=66.0215534&lon=12.6314628&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 455 for location of palaia fokaia,gr 
     http://api.openweathermap.org/data/2.5/weather?lat=37.7178168&lon=23.9464496&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    time delay
    The valid url # 456 for location of plastun,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=44.7548106&lon=136.3089946&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 457 for location of fort nelson,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=58.8050174&lon=-122.697236&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 458 for location of petropavlovsk-kamchatskiy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=53.0409109&lon=158.677726&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 459 for location of beisfjord,no 
     http://api.openweathermap.org/data/2.5/weather?lat=68.376177&lon=17.5960147&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 460 for location of yarmouth,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=43.8374576&lon=-66.11738199999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 461 for location of hurricane,us 
     http://api.openweathermap.org/data/2.5/weather?lat=37.1752607&lon=-113.2899484&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 462 for location of new ulm,us 
     http://api.openweathermap.org/data/2.5/weather?lat=44.3144394&lon=-94.45930179999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 463 for location of karauzyak,uz 
     http://api.openweathermap.org/data/2.5/weather?lat=43.0174717&lon=60.011507&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 464 for location of bogo,cm 
     http://api.openweathermap.org/data/2.5/weather?lat=10.7330518&lon=14.6004911&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 465 for location of bensonville,lr 
     http://api.openweathermap.org/data/2.5/weather?lat=6.446975999999999&lon=-10.6182477&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 466 for location of lucea,jm 
     http://api.openweathermap.org/data/2.5/weather?lat=18.4504186&lon=-78.17639369999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 467 for location of sibolga,id 
     http://api.openweathermap.org/data/2.5/weather?lat=1.7368371&lon=98.78511209999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 468 for location of poum,nc 
     http://api.openweathermap.org/data/2.5/weather?lat=-20.2349574&lon=164.0329499&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 469 for location of santiago,ph 
     http://api.openweathermap.org/data/2.5/weather?lat=16.7149832&lon=121.5537152&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 470 for location of vao,nc 
     http://api.openweathermap.org/data/2.5/weather?lat=-22.6658429&lon=167.4960078&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 471 for location of verkhnevilyuysk,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=63.44358839999999&lon=120.3197132&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 472 for location of shubarkuduk,kz 
     http://api.openweathermap.org/data/2.5/weather?lat=49.14301649999999&lon=56.4816745&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 473 for location of gubkinskiy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=64.4444789&lon=76.4742687&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 474 for location of terrace,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=34.035425&lon=-117.306961&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 475 for location of tsihombe,mg 
     http://api.openweathermap.org/data/2.5/weather?lat=-25.3168473&lon=45.48630929999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 476 for location of bathsheba,bb 
     http://api.openweathermap.org/data/2.5/weather?lat=13.2101681&lon=-59.5253545&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 477 for location of kamina,cd 
     http://api.openweathermap.org/data/2.5/weather?lat=-8.7368981&lon=24.9872821&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 478 for location of hiranagar,in 
     http://api.openweathermap.org/data/2.5/weather?lat=32.4556366&lon=75.27276549999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 479 for location of yanam,in 
     http://api.openweathermap.org/data/2.5/weather?lat=16.7271912&lon=82.21757749999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 480 for location of acapulco,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=16.8531086&lon=-99.8236533&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 481 for location of loandjili,cg 
     http://api.openweathermap.org/data/2.5/weather?lat=-4.76732&lon=11.8627984&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 482 for location of buala,sb 
     http://api.openweathermap.org/data/2.5/weather?lat=-8.1662459&lon=159.6189829&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 483 for location of la macarena,co 
     http://api.openweathermap.org/data/2.5/weather?lat=2.181718&lon=-73.78645&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 484 for location of chernyshevskiy,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=63.0250384&lon=112.4902494&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 485 for location of okha,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=53.577557&lon=142.9424741&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 486 for location of thinadhoo,mv 
     http://api.openweathermap.org/data/2.5/weather?lat=0.531061&lon=72.99772519999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 487 for location of boissevain,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=49.2304365&lon=-100.0595039&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 488 for location of camacha,pt 
     http://api.openweathermap.org/data/2.5/weather?lat=32.679852&lon=-16.8502879&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 489 for location of mpulungu,zm 
     http://api.openweathermap.org/data/2.5/weather?lat=-8.772507&lon=31.1166193&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 490 for location of sioux lookout,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=50.0978321&lon=-91.922038&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 491 for location of khani,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=56.933333&lon=119.965&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 492 for location of luau,ao 
     http://api.openweathermap.org/data/2.5/weather?lat=-10.7072554&lon=22.22946&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 493 for location of sorvag,fo 
     http://api.openweathermap.org/data/2.5/weather?lat=62.07129279999999&lon=-7.3058656&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 494 for location of hay river,ca 
     http://api.openweathermap.org/data/2.5/weather?lat=60.816218&lon=-115.7853652&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 495 for location of margate,za 
     http://api.openweathermap.org/data/2.5/weather?lat=-30.8458684&lon=30.37237409999999&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 496 for location of malinovoye ozero,ru 
     http://api.openweathermap.org/data/2.5/weather?lat=51.6781161&lon=79.7893754&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 497 for location of mandalgovi,mn 
     http://api.openweathermap.org/data/2.5/weather?lat=45.7631589&lon=106.2650297&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 498 for location of bahia honda,cu 
     http://api.openweathermap.org/data/2.5/weather?lat=22.9081486&lon=-83.1702597&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 499 for location of salalah,om 
     http://api.openweathermap.org/data/2.5/weather?lat=17.0506675&lon=54.1065864&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4
    The valid url # 500 for location of puerto escondido,mx 
     http://api.openweathermap.org/data/2.5/weather?lat=15.8719795&lon=-97.0767365&units=imperial&APPID=2bf97998be001d3babddbe80bb73edb4





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
      <th>Cities</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Temperature(F)</th>
      <th>Humidity(%)</th>
      <th>Cloudiness(%)</th>
      <th>Wind Speed(mph)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>mataura,pf</td>
      <td>-23.347063</td>
      <td>-149.485044</td>
      <td>71.75</td>
      <td>100</td>
      <td>0</td>
      <td>7.96</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ushuaia,ar</td>
      <td>-54.801912</td>
      <td>-68.302951</td>
      <td>33.80</td>
      <td>86</td>
      <td>90</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>2</th>
      <td>kirakira,sb</td>
      <td>-10.448715</td>
      <td>161.896413</td>
      <td>82.19</td>
      <td>100</td>
      <td>56</td>
      <td>19.37</td>
    </tr>
    <tr>
      <th>3</th>
      <td>boyuibe,bo</td>
      <td>-20.441300</td>
      <td>-63.279822</td>
      <td>82.10</td>
      <td>40</td>
      <td>88</td>
      <td>20.83</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tuktoyaktuk,ca</td>
      <td>69.445358</td>
      <td>-133.034181</td>
      <td>59.00</td>
      <td>58</td>
      <td>75</td>
      <td>11.41</td>
    </tr>
    <tr>
      <th>5</th>
      <td>sinnamary,gf</td>
      <td>5.374671</td>
      <td>-52.954599</td>
      <td>81.20</td>
      <td>94</td>
      <td>0</td>
      <td>10.76</td>
    </tr>
    <tr>
      <th>6</th>
      <td>manaure,co</td>
      <td>11.772778</td>
      <td>-72.444227</td>
      <td>82.73</td>
      <td>100</td>
      <td>44</td>
      <td>11.99</td>
    </tr>
    <tr>
      <th>7</th>
      <td>kattivakkam,in</td>
      <td>12.968213</td>
      <td>80.259943</td>
      <td>82.40</td>
      <td>88</td>
      <td>75</td>
      <td>3.36</td>
    </tr>
    <tr>
      <th>8</th>
      <td>vestmanna,fo</td>
      <td>62.163170</td>
      <td>-7.165286</td>
      <td>44.60</td>
      <td>93</td>
      <td>92</td>
      <td>29.97</td>
    </tr>
    <tr>
      <th>9</th>
      <td>hithadhoo,mv</td>
      <td>-0.606057</td>
      <td>73.089225</td>
      <td>81.02</td>
      <td>100</td>
      <td>56</td>
      <td>13.22</td>
    </tr>
    <tr>
      <th>10</th>
      <td>qaanaaq,gl</td>
      <td>77.467043</td>
      <td>-69.228483</td>
      <td>13.70</td>
      <td>100</td>
      <td>0</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>11</th>
      <td>port elizabeth,za</td>
      <td>-33.713925</td>
      <td>25.520736</td>
      <td>57.20</td>
      <td>71</td>
      <td>0</td>
      <td>11.41</td>
    </tr>
    <tr>
      <th>12</th>
      <td>busselton,au</td>
      <td>-33.655493</td>
      <td>115.350019</td>
      <td>62.39</td>
      <td>99</td>
      <td>12</td>
      <td>7.29</td>
    </tr>
    <tr>
      <th>13</th>
      <td>hermanus,za</td>
      <td>-34.409200</td>
      <td>19.250444</td>
      <td>36.20</td>
      <td>97</td>
      <td>12</td>
      <td>2.48</td>
    </tr>
    <tr>
      <th>14</th>
      <td>tocopilla,cl</td>
      <td>-22.085798</td>
      <td>-70.193006</td>
      <td>50.87</td>
      <td>100</td>
      <td>0</td>
      <td>6.40</td>
    </tr>
    <tr>
      <th>15</th>
      <td>barentsburg,sj</td>
      <td>78.064847</td>
      <td>14.233460</td>
      <td>39.20</td>
      <td>69</td>
      <td>20</td>
      <td>17.22</td>
    </tr>
    <tr>
      <th>16</th>
      <td>rikitea,pf</td>
      <td>-23.119901</td>
      <td>-134.970265</td>
      <td>70.67</td>
      <td>100</td>
      <td>80</td>
      <td>9.98</td>
    </tr>
    <tr>
      <th>17</th>
      <td>bundaberg,au</td>
      <td>-24.866974</td>
      <td>152.350971</td>
      <td>68.51</td>
      <td>100</td>
      <td>92</td>
      <td>18.03</td>
    </tr>
    <tr>
      <th>18</th>
      <td>longyearbyen,sj</td>
      <td>78.223172</td>
      <td>15.626723</td>
      <td>39.20</td>
      <td>69</td>
      <td>20</td>
      <td>17.22</td>
    </tr>
    <tr>
      <th>19</th>
      <td>ribeira grande,pt</td>
      <td>37.821037</td>
      <td>-25.514814</td>
      <td>71.60</td>
      <td>78</td>
      <td>75</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>20</th>
      <td>corum,tr</td>
      <td>40.549926</td>
      <td>34.953724</td>
      <td>62.60</td>
      <td>63</td>
      <td>0</td>
      <td>6.93</td>
    </tr>
    <tr>
      <th>21</th>
      <td>alofi,nu</td>
      <td>-19.055371</td>
      <td>-169.917871</td>
      <td>75.20</td>
      <td>88</td>
      <td>75</td>
      <td>13.87</td>
    </tr>
    <tr>
      <th>22</th>
      <td>cape town,za</td>
      <td>-33.924869</td>
      <td>18.424055</td>
      <td>51.80</td>
      <td>87</td>
      <td>40</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>23</th>
      <td>kudahuvadhoo,mv</td>
      <td>2.670704</td>
      <td>72.891423</td>
      <td>82.10</td>
      <td>100</td>
      <td>92</td>
      <td>14.12</td>
    </tr>
    <tr>
      <th>24</th>
      <td>bowen,au</td>
      <td>-20.001480</td>
      <td>148.226218</td>
      <td>75.80</td>
      <td>94</td>
      <td>48</td>
      <td>4.72</td>
    </tr>
    <tr>
      <th>25</th>
      <td>brigham city,us</td>
      <td>41.510213</td>
      <td>-112.015501</td>
      <td>82.40</td>
      <td>24</td>
      <td>1</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>26</th>
      <td>port alfred,za</td>
      <td>-33.586407</td>
      <td>26.885145</td>
      <td>60.14</td>
      <td>90</td>
      <td>76</td>
      <td>13.22</td>
    </tr>
    <tr>
      <th>27</th>
      <td>ukiah,us</td>
      <td>39.150171</td>
      <td>-123.207783</td>
      <td>77.00</td>
      <td>57</td>
      <td>1</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>28</th>
      <td>atuona,pf</td>
      <td>-9.803280</td>
      <td>-139.042574</td>
      <td>78.23</td>
      <td>100</td>
      <td>20</td>
      <td>13.11</td>
    </tr>
    <tr>
      <th>29</th>
      <td>belaya gora,ru</td>
      <td>68.549671</td>
      <td>146.232876</td>
      <td>36.11</td>
      <td>84</td>
      <td>64</td>
      <td>9.42</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>470</th>
      <td>verkhnevilyuysk,ru</td>
      <td>63.443588</td>
      <td>120.319713</td>
      <td>51.32</td>
      <td>83</td>
      <td>20</td>
      <td>5.17</td>
    </tr>
    <tr>
      <th>471</th>
      <td>shubarkuduk,kz</td>
      <td>49.143016</td>
      <td>56.481674</td>
      <td>53.84</td>
      <td>52</td>
      <td>0</td>
      <td>8.86</td>
    </tr>
    <tr>
      <th>472</th>
      <td>gubkinskiy,ru</td>
      <td>64.444479</td>
      <td>76.474269</td>
      <td>35.30</td>
      <td>100</td>
      <td>24</td>
      <td>4.72</td>
    </tr>
    <tr>
      <th>473</th>
      <td>terrace,ca</td>
      <td>34.035425</td>
      <td>-117.306961</td>
      <td>80.60</td>
      <td>44</td>
      <td>1</td>
      <td>24.16</td>
    </tr>
    <tr>
      <th>474</th>
      <td>tsihombe,mg</td>
      <td>-25.316847</td>
      <td>45.486309</td>
      <td>55.01</td>
      <td>66</td>
      <td>0</td>
      <td>3.04</td>
    </tr>
    <tr>
      <th>475</th>
      <td>bathsheba,bb</td>
      <td>13.210168</td>
      <td>-59.525354</td>
      <td>80.60</td>
      <td>94</td>
      <td>75</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>476</th>
      <td>kamina,cd</td>
      <td>-8.736898</td>
      <td>24.987282</td>
      <td>60.32</td>
      <td>89</td>
      <td>0</td>
      <td>3.38</td>
    </tr>
    <tr>
      <th>477</th>
      <td>hiranagar,in</td>
      <td>32.455637</td>
      <td>75.272765</td>
      <td>83.36</td>
      <td>49</td>
      <td>0</td>
      <td>4.94</td>
    </tr>
    <tr>
      <th>478</th>
      <td>yanam,in</td>
      <td>16.727191</td>
      <td>82.217577</td>
      <td>78.68</td>
      <td>98</td>
      <td>64</td>
      <td>3.27</td>
    </tr>
    <tr>
      <th>479</th>
      <td>acapulco,mx</td>
      <td>16.853109</td>
      <td>-99.823653</td>
      <td>75.20</td>
      <td>94</td>
      <td>90</td>
      <td>10.29</td>
    </tr>
    <tr>
      <th>480</th>
      <td>loandjili,cg</td>
      <td>-4.767320</td>
      <td>11.862798</td>
      <td>77.00</td>
      <td>83</td>
      <td>75</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>481</th>
      <td>buala,sb</td>
      <td>-8.166246</td>
      <td>159.618983</td>
      <td>85.16</td>
      <td>82</td>
      <td>80</td>
      <td>9.42</td>
    </tr>
    <tr>
      <th>482</th>
      <td>la macarena,co</td>
      <td>2.181718</td>
      <td>-73.786450</td>
      <td>71.48</td>
      <td>99</td>
      <td>92</td>
      <td>1.81</td>
    </tr>
    <tr>
      <th>483</th>
      <td>chernyshevskiy,ru</td>
      <td>63.025038</td>
      <td>112.490249</td>
      <td>48.62</td>
      <td>77</td>
      <td>8</td>
      <td>7.96</td>
    </tr>
    <tr>
      <th>484</th>
      <td>okha,ru</td>
      <td>53.577557</td>
      <td>142.942474</td>
      <td>58.16</td>
      <td>78</td>
      <td>0</td>
      <td>4.83</td>
    </tr>
    <tr>
      <th>485</th>
      <td>thinadhoo,mv</td>
      <td>0.531061</td>
      <td>72.997725</td>
      <td>81.92</td>
      <td>100</td>
      <td>68</td>
      <td>12.77</td>
    </tr>
    <tr>
      <th>486</th>
      <td>boissevain,ca</td>
      <td>49.230437</td>
      <td>-100.059504</td>
      <td>59.00</td>
      <td>62</td>
      <td>75</td>
      <td>10.29</td>
    </tr>
    <tr>
      <th>487</th>
      <td>camacha,pt</td>
      <td>32.679852</td>
      <td>-16.850288</td>
      <td>71.60</td>
      <td>73</td>
      <td>40</td>
      <td>16.11</td>
    </tr>
    <tr>
      <th>488</th>
      <td>mpulungu,zm</td>
      <td>-8.772507</td>
      <td>31.116619</td>
      <td>56.00</td>
      <td>50</td>
      <td>8</td>
      <td>9.19</td>
    </tr>
    <tr>
      <th>489</th>
      <td>sioux lookout,ca</td>
      <td>50.097832</td>
      <td>-91.922038</td>
      <td>62.60</td>
      <td>59</td>
      <td>90</td>
      <td>3.36</td>
    </tr>
    <tr>
      <th>490</th>
      <td>khani,ru</td>
      <td>56.933333</td>
      <td>119.965000</td>
      <td>52.22</td>
      <td>70</td>
      <td>0</td>
      <td>2.15</td>
    </tr>
    <tr>
      <th>491</th>
      <td>luau,ao</td>
      <td>-10.707255</td>
      <td>22.229460</td>
      <td>65.18</td>
      <td>33</td>
      <td>0</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>492</th>
      <td>sorvag,fo</td>
      <td>62.071293</td>
      <td>-7.305866</td>
      <td>44.60</td>
      <td>93</td>
      <td>88</td>
      <td>29.97</td>
    </tr>
    <tr>
      <th>493</th>
      <td>hay river,ca</td>
      <td>60.816218</td>
      <td>-115.785365</td>
      <td>48.20</td>
      <td>70</td>
      <td>20</td>
      <td>6.93</td>
    </tr>
    <tr>
      <th>494</th>
      <td>margate,za</td>
      <td>-30.845868</td>
      <td>30.372374</td>
      <td>66.53</td>
      <td>97</td>
      <td>92</td>
      <td>12.55</td>
    </tr>
    <tr>
      <th>495</th>
      <td>malinovoye ozero,ru</td>
      <td>51.678116</td>
      <td>79.789375</td>
      <td>48.62</td>
      <td>82</td>
      <td>0</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>496</th>
      <td>mandalgovi,mn</td>
      <td>45.763159</td>
      <td>106.265030</td>
      <td>66.35</td>
      <td>56</td>
      <td>8</td>
      <td>13.67</td>
    </tr>
    <tr>
      <th>497</th>
      <td>bahia honda,cu</td>
      <td>22.908149</td>
      <td>-83.170260</td>
      <td>78.23</td>
      <td>91</td>
      <td>0</td>
      <td>2.59</td>
    </tr>
    <tr>
      <th>498</th>
      <td>salalah,om</td>
      <td>17.050667</td>
      <td>54.106586</td>
      <td>78.80</td>
      <td>83</td>
      <td>20</td>
      <td>9.19</td>
    </tr>
    <tr>
      <th>499</th>
      <td>puerto escondido,mx</td>
      <td>15.871980</td>
      <td>-97.076736</td>
      <td>80.21</td>
      <td>100</td>
      <td>88</td>
      <td>11.21</td>
    </tr>
  </tbody>
</table>
<p>500 rows × 7 columns</p>
</div>




```python
city_df[['City','Country']] = city_df['Cities'].str.split(',', expand=True)
```


```python
#printing the dataframe
city_df = city_df.drop('Cities', 1)

city_df["City"]=city_df["City"].str.capitalize()

city_df["Country"]=city_df["Country"].str.upper()

city_df = city_df[['City', 'Country', 'Latitude','Longitude','Temperature(F)','Humidity(%)','Cloudiness(%)','Wind Speed(mph)']]

city_df
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
      <th>City</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Temperature(F)</th>
      <th>Humidity(%)</th>
      <th>Cloudiness(%)</th>
      <th>Wind Speed(mph)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Mataura</td>
      <td>PF</td>
      <td>-23.347063</td>
      <td>-149.485044</td>
      <td>71.75</td>
      <td>100</td>
      <td>0</td>
      <td>7.96</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Ushuaia</td>
      <td>AR</td>
      <td>-54.801912</td>
      <td>-68.302951</td>
      <td>33.80</td>
      <td>86</td>
      <td>90</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Kirakira</td>
      <td>SB</td>
      <td>-10.448715</td>
      <td>161.896413</td>
      <td>82.19</td>
      <td>100</td>
      <td>56</td>
      <td>19.37</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Boyuibe</td>
      <td>BO</td>
      <td>-20.441300</td>
      <td>-63.279822</td>
      <td>82.10</td>
      <td>40</td>
      <td>88</td>
      <td>20.83</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Tuktoyaktuk</td>
      <td>CA</td>
      <td>69.445358</td>
      <td>-133.034181</td>
      <td>59.00</td>
      <td>58</td>
      <td>75</td>
      <td>11.41</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Sinnamary</td>
      <td>GF</td>
      <td>5.374671</td>
      <td>-52.954599</td>
      <td>81.20</td>
      <td>94</td>
      <td>0</td>
      <td>10.76</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Manaure</td>
      <td>CO</td>
      <td>11.772778</td>
      <td>-72.444227</td>
      <td>82.73</td>
      <td>100</td>
      <td>44</td>
      <td>11.99</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Kattivakkam</td>
      <td>IN</td>
      <td>12.968213</td>
      <td>80.259943</td>
      <td>82.40</td>
      <td>88</td>
      <td>75</td>
      <td>3.36</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Vestmanna</td>
      <td>FO</td>
      <td>62.163170</td>
      <td>-7.165286</td>
      <td>44.60</td>
      <td>93</td>
      <td>92</td>
      <td>29.97</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Hithadhoo</td>
      <td>MV</td>
      <td>-0.606057</td>
      <td>73.089225</td>
      <td>81.02</td>
      <td>100</td>
      <td>56</td>
      <td>13.22</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Qaanaaq</td>
      <td>GL</td>
      <td>77.467043</td>
      <td>-69.228483</td>
      <td>13.70</td>
      <td>100</td>
      <td>0</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Port elizabeth</td>
      <td>ZA</td>
      <td>-33.713925</td>
      <td>25.520736</td>
      <td>57.20</td>
      <td>71</td>
      <td>0</td>
      <td>11.41</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Busselton</td>
      <td>AU</td>
      <td>-33.655493</td>
      <td>115.350019</td>
      <td>62.39</td>
      <td>99</td>
      <td>12</td>
      <td>7.29</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Hermanus</td>
      <td>ZA</td>
      <td>-34.409200</td>
      <td>19.250444</td>
      <td>36.20</td>
      <td>97</td>
      <td>12</td>
      <td>2.48</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Tocopilla</td>
      <td>CL</td>
      <td>-22.085798</td>
      <td>-70.193006</td>
      <td>50.87</td>
      <td>100</td>
      <td>0</td>
      <td>6.40</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Barentsburg</td>
      <td>SJ</td>
      <td>78.064847</td>
      <td>14.233460</td>
      <td>39.20</td>
      <td>69</td>
      <td>20</td>
      <td>17.22</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Rikitea</td>
      <td>PF</td>
      <td>-23.119901</td>
      <td>-134.970265</td>
      <td>70.67</td>
      <td>100</td>
      <td>80</td>
      <td>9.98</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Bundaberg</td>
      <td>AU</td>
      <td>-24.866974</td>
      <td>152.350971</td>
      <td>68.51</td>
      <td>100</td>
      <td>92</td>
      <td>18.03</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Longyearbyen</td>
      <td>SJ</td>
      <td>78.223172</td>
      <td>15.626723</td>
      <td>39.20</td>
      <td>69</td>
      <td>20</td>
      <td>17.22</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Ribeira grande</td>
      <td>PT</td>
      <td>37.821037</td>
      <td>-25.514814</td>
      <td>71.60</td>
      <td>78</td>
      <td>75</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Corum</td>
      <td>TR</td>
      <td>40.549926</td>
      <td>34.953724</td>
      <td>62.60</td>
      <td>63</td>
      <td>0</td>
      <td>6.93</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Alofi</td>
      <td>NU</td>
      <td>-19.055371</td>
      <td>-169.917871</td>
      <td>75.20</td>
      <td>88</td>
      <td>75</td>
      <td>13.87</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Cape town</td>
      <td>ZA</td>
      <td>-33.924869</td>
      <td>18.424055</td>
      <td>51.80</td>
      <td>87</td>
      <td>40</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Kudahuvadhoo</td>
      <td>MV</td>
      <td>2.670704</td>
      <td>72.891423</td>
      <td>82.10</td>
      <td>100</td>
      <td>92</td>
      <td>14.12</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Bowen</td>
      <td>AU</td>
      <td>-20.001480</td>
      <td>148.226218</td>
      <td>75.80</td>
      <td>94</td>
      <td>48</td>
      <td>4.72</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Brigham city</td>
      <td>US</td>
      <td>41.510213</td>
      <td>-112.015501</td>
      <td>82.40</td>
      <td>24</td>
      <td>1</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Port alfred</td>
      <td>ZA</td>
      <td>-33.586407</td>
      <td>26.885145</td>
      <td>60.14</td>
      <td>90</td>
      <td>76</td>
      <td>13.22</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Ukiah</td>
      <td>US</td>
      <td>39.150171</td>
      <td>-123.207783</td>
      <td>77.00</td>
      <td>57</td>
      <td>1</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Atuona</td>
      <td>PF</td>
      <td>-9.803280</td>
      <td>-139.042574</td>
      <td>78.23</td>
      <td>100</td>
      <td>20</td>
      <td>13.11</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Belaya gora</td>
      <td>RU</td>
      <td>68.549671</td>
      <td>146.232876</td>
      <td>36.11</td>
      <td>84</td>
      <td>64</td>
      <td>9.42</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>470</th>
      <td>Verkhnevilyuysk</td>
      <td>RU</td>
      <td>63.443588</td>
      <td>120.319713</td>
      <td>51.32</td>
      <td>83</td>
      <td>20</td>
      <td>5.17</td>
    </tr>
    <tr>
      <th>471</th>
      <td>Shubarkuduk</td>
      <td>KZ</td>
      <td>49.143016</td>
      <td>56.481674</td>
      <td>53.84</td>
      <td>52</td>
      <td>0</td>
      <td>8.86</td>
    </tr>
    <tr>
      <th>472</th>
      <td>Gubkinskiy</td>
      <td>RU</td>
      <td>64.444479</td>
      <td>76.474269</td>
      <td>35.30</td>
      <td>100</td>
      <td>24</td>
      <td>4.72</td>
    </tr>
    <tr>
      <th>473</th>
      <td>Terrace</td>
      <td>CA</td>
      <td>34.035425</td>
      <td>-117.306961</td>
      <td>80.60</td>
      <td>44</td>
      <td>1</td>
      <td>24.16</td>
    </tr>
    <tr>
      <th>474</th>
      <td>Tsihombe</td>
      <td>MG</td>
      <td>-25.316847</td>
      <td>45.486309</td>
      <td>55.01</td>
      <td>66</td>
      <td>0</td>
      <td>3.04</td>
    </tr>
    <tr>
      <th>475</th>
      <td>Bathsheba</td>
      <td>BB</td>
      <td>13.210168</td>
      <td>-59.525354</td>
      <td>80.60</td>
      <td>94</td>
      <td>75</td>
      <td>5.82</td>
    </tr>
    <tr>
      <th>476</th>
      <td>Kamina</td>
      <td>CD</td>
      <td>-8.736898</td>
      <td>24.987282</td>
      <td>60.32</td>
      <td>89</td>
      <td>0</td>
      <td>3.38</td>
    </tr>
    <tr>
      <th>477</th>
      <td>Hiranagar</td>
      <td>IN</td>
      <td>32.455637</td>
      <td>75.272765</td>
      <td>83.36</td>
      <td>49</td>
      <td>0</td>
      <td>4.94</td>
    </tr>
    <tr>
      <th>478</th>
      <td>Yanam</td>
      <td>IN</td>
      <td>16.727191</td>
      <td>82.217577</td>
      <td>78.68</td>
      <td>98</td>
      <td>64</td>
      <td>3.27</td>
    </tr>
    <tr>
      <th>479</th>
      <td>Acapulco</td>
      <td>MX</td>
      <td>16.853109</td>
      <td>-99.823653</td>
      <td>75.20</td>
      <td>94</td>
      <td>90</td>
      <td>10.29</td>
    </tr>
    <tr>
      <th>480</th>
      <td>Loandjili</td>
      <td>CG</td>
      <td>-4.767320</td>
      <td>11.862798</td>
      <td>77.00</td>
      <td>83</td>
      <td>75</td>
      <td>4.70</td>
    </tr>
    <tr>
      <th>481</th>
      <td>Buala</td>
      <td>SB</td>
      <td>-8.166246</td>
      <td>159.618983</td>
      <td>85.16</td>
      <td>82</td>
      <td>80</td>
      <td>9.42</td>
    </tr>
    <tr>
      <th>482</th>
      <td>La macarena</td>
      <td>CO</td>
      <td>2.181718</td>
      <td>-73.786450</td>
      <td>71.48</td>
      <td>99</td>
      <td>92</td>
      <td>1.81</td>
    </tr>
    <tr>
      <th>483</th>
      <td>Chernyshevskiy</td>
      <td>RU</td>
      <td>63.025038</td>
      <td>112.490249</td>
      <td>48.62</td>
      <td>77</td>
      <td>8</td>
      <td>7.96</td>
    </tr>
    <tr>
      <th>484</th>
      <td>Okha</td>
      <td>RU</td>
      <td>53.577557</td>
      <td>142.942474</td>
      <td>58.16</td>
      <td>78</td>
      <td>0</td>
      <td>4.83</td>
    </tr>
    <tr>
      <th>485</th>
      <td>Thinadhoo</td>
      <td>MV</td>
      <td>0.531061</td>
      <td>72.997725</td>
      <td>81.92</td>
      <td>100</td>
      <td>68</td>
      <td>12.77</td>
    </tr>
    <tr>
      <th>486</th>
      <td>Boissevain</td>
      <td>CA</td>
      <td>49.230437</td>
      <td>-100.059504</td>
      <td>59.00</td>
      <td>62</td>
      <td>75</td>
      <td>10.29</td>
    </tr>
    <tr>
      <th>487</th>
      <td>Camacha</td>
      <td>PT</td>
      <td>32.679852</td>
      <td>-16.850288</td>
      <td>71.60</td>
      <td>73</td>
      <td>40</td>
      <td>16.11</td>
    </tr>
    <tr>
      <th>488</th>
      <td>Mpulungu</td>
      <td>ZM</td>
      <td>-8.772507</td>
      <td>31.116619</td>
      <td>56.00</td>
      <td>50</td>
      <td>8</td>
      <td>9.19</td>
    </tr>
    <tr>
      <th>489</th>
      <td>Sioux lookout</td>
      <td>CA</td>
      <td>50.097832</td>
      <td>-91.922038</td>
      <td>62.60</td>
      <td>59</td>
      <td>90</td>
      <td>3.36</td>
    </tr>
    <tr>
      <th>490</th>
      <td>Khani</td>
      <td>RU</td>
      <td>56.933333</td>
      <td>119.965000</td>
      <td>52.22</td>
      <td>70</td>
      <td>0</td>
      <td>2.15</td>
    </tr>
    <tr>
      <th>491</th>
      <td>Luau</td>
      <td>AO</td>
      <td>-10.707255</td>
      <td>22.229460</td>
      <td>65.18</td>
      <td>33</td>
      <td>0</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>492</th>
      <td>Sorvag</td>
      <td>FO</td>
      <td>62.071293</td>
      <td>-7.305866</td>
      <td>44.60</td>
      <td>93</td>
      <td>88</td>
      <td>29.97</td>
    </tr>
    <tr>
      <th>493</th>
      <td>Hay river</td>
      <td>CA</td>
      <td>60.816218</td>
      <td>-115.785365</td>
      <td>48.20</td>
      <td>70</td>
      <td>20</td>
      <td>6.93</td>
    </tr>
    <tr>
      <th>494</th>
      <td>Margate</td>
      <td>ZA</td>
      <td>-30.845868</td>
      <td>30.372374</td>
      <td>66.53</td>
      <td>97</td>
      <td>92</td>
      <td>12.55</td>
    </tr>
    <tr>
      <th>495</th>
      <td>Malinovoye ozero</td>
      <td>RU</td>
      <td>51.678116</td>
      <td>79.789375</td>
      <td>48.62</td>
      <td>82</td>
      <td>0</td>
      <td>4.61</td>
    </tr>
    <tr>
      <th>496</th>
      <td>Mandalgovi</td>
      <td>MN</td>
      <td>45.763159</td>
      <td>106.265030</td>
      <td>66.35</td>
      <td>56</td>
      <td>8</td>
      <td>13.67</td>
    </tr>
    <tr>
      <th>497</th>
      <td>Bahia honda</td>
      <td>CU</td>
      <td>22.908149</td>
      <td>-83.170260</td>
      <td>78.23</td>
      <td>91</td>
      <td>0</td>
      <td>2.59</td>
    </tr>
    <tr>
      <th>498</th>
      <td>Salalah</td>
      <td>OM</td>
      <td>17.050667</td>
      <td>54.106586</td>
      <td>78.80</td>
      <td>83</td>
      <td>20</td>
      <td>9.19</td>
    </tr>
    <tr>
      <th>499</th>
      <td>Puerto escondido</td>
      <td>MX</td>
      <td>15.871980</td>
      <td>-97.076736</td>
      <td>80.21</td>
      <td>100</td>
      <td>88</td>
      <td>11.21</td>
    </tr>
  </tbody>
</table>
<p>500 rows × 8 columns</p>
</div>




```python
#write the output in csv

city_df.to_csv("output_city.csv",index=False)

#geth the x-axis

x=city_df["Latitude"]
yt=city_df["Temperature(F)"]
yh=city_df["Humidity(%)"]
yc=city_df["Cloudiness(%)"]
ys=city_df["Wind Speed(mph)"]
```

## Build a series of scatter plots to showcase the following relationships:

* Temperature (F) vs. Latitude
* Humidity (%) vs. Latitude
* Cloudiness (%) vs. Latitude
* Wind Speed (mph) vs. Latitude


```python
#Temperature (F) vs. Latitude scatter plot

plt.scatter(x,yt,marker="o",facecolors="blue", edgecolors="black",s=100, alpha=0.75)

plt.title('City Latitude vs Max Temperature', fontsize=15)
plt.xlabel('Latitude', fontsize=9)
plt.ylabel('Temperature', fontsize=9)
plt.grid()
plt.savefig('tempvsLat.png')
plt.show()
```


![png](output_8_0.png)



```python
#Humidity(%) vs. Latitude scatter plot

plt.scatter(x,yh,marker="o",facecolors="blue", edgecolors="black",s=150, alpha=0.75)

plt.title('City Latitude vs Humidity(%)', fontsize=15)
plt.xlabel('Latitude', fontsize=9)
plt.ylabel('Humidity(%)', fontsize=9)
plt.grid()
plt.savefig('HumidvsLat.png')
plt.show()
```


![png](output_9_0.png)



```python
#Cloudiness(%) vs. Latitude scatter plot

plt.scatter(x,yc,marker="o",facecolors="blue", edgecolors="black",s=150, alpha=0.75)

plt.title('City Latitude vs Cloudiness(%)', fontsize=15)
plt.xlabel('Latitude', fontsize=9)
plt.ylabel('Cloudiness(%)', fontsize=9)
plt.grid()
plt.savefig('CloudvsLat.png')
plt.show()
```


![png](output_10_0.png)



```python
#Wind Speed(mph) vs. Latitude scatter plot


plt.scatter(x,ys,marker="o",facecolors="blue", edgecolors="black",s=150,alpha=0.75)
plt.title('City Latitude vs Wind Speed(mph)', fontsize=15)
plt.xlabel('Latitude', fontsize=9)
plt.ylabel('Wind Speed(mph)', fontsize=9)
plt.grid()
plt.savefig('WindvsLat.png')
plt.show()

var2=datetime.datetime.now()

result=var2-var1
print("Total Duration to run this Program : %s " %(result))
```


![png](output_11_0.png)


    Total Duration to run this Program : 0:14:53.756118 

