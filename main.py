import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random

def choose_rest(data = pd.read_csv('data.csv'), **kwargs):
    price_level = kwargs.get('price_level', None) #int(between 1-4)
    rating = kwargs.get('rating', None) #float
    cuisine = kwargs.get('cuisine', None) #str
    type = kwargs.get('type', None) #str(atmosphere)
    food = kwargs.get('food',None) #str
    dist = kwargs.get('dist', None) #float(miles away)
    cur_lat = kwargs.get('cur_lat', None) #float
    cur_lng = kwargs.get('cur_lng', None) #float
    cur_time = kwargs.get('cur_time', None) #int
    
    data = data
    if cuisine:
        df_cuisine = check_cuisine(cuisine, data)
        df_cuisine.reset_index(inplace = True, drop = True)
    else:
        df_cuisine = None
    if type:
        df_type = check_type(type, data)
        df_type.reset_index(inplace = True, drop = True)
    else:
        df_type = None
    if price_level:
        df_price = check_price(price_level, data)
        df_price.reset_index(inplace = True, drop = True)
    else:
        df_price = None
    if rating:
        df_rate = check_rating(rating, data)
        df_rate.reset_index(inplace = True, drop = True)
    else:
        df_rate = None
    #if food:  
    #if dist:
    #check_open()
    names = get_max(cuisine = df_cuisine, type = df_type, price = df_price, rating = df_rate)
    length = len(names)
    val = random.randint(0,length)
    ind = names[val]
    target = data[data['name']==ind]
    make_viz(target)
    return

def get_max(**kwargs):
    price = kwargs.get('price', None) #pd.DataFrame
    rating = kwargs.get('rating', None) #pd.DataFrame
    cuisine = kwargs.get('cuisine', None) #pd.DataFrame
    type = kwargs.get('type', None) #pd.DataFrame
    count = {}
    if cuisine is not None:
        c = cuisine
        i=0
        while i < len(c):
            if c['name'][i] in count:
                count[c['name'][i]] += 1
                i+=1
            else:
                count[c['name'][i]] = 1
                i+=1
    if type is not None:
        t = type
        j=0
        while j < len(t):
            if t['name'][j] in count:
                count[t['name'][j]] += 1
                j+=1
            else:
                count[t['name'][j]] = 1
                j+=1
    if price is not None:
        p = price
        z=0
        while z < len(p):
            if p['name'][z] in count:
                count[p['name'][z]] += 1
                z+=1
            else:
                count[p['name'][z]] = 1
                z+=1
    if rating is not None:
        r = rating
        y=0
        while y < len(r):
            if r['name'][y] in count:
                count[r['name'][y]] += 1
                y+=1
            else:
                count[r['name'][y]] = 1
                y+=1
    num = 0
    for key in count:
        if count[key] > num:
            num = count[key]
    temp = []
    for key in count:
        if count[key] == num:
            temp.append(key)
    return temp

def check_type(type:str, data:pd.DataFrame)->pd.DataFrame:
    i=0
    ind = []
    while i < len(data):
        if type in data['type_place'][i]:
            ind.append(i)
        i+=1
    df = pd.DataFrame(columns=['name', 'vicinity', 'price_level_x', 'rating_x', 'types',
                        'user_ratings_total', 'lat', 'lng', 'categories', 'attributes', 'hours',
                        'url','cuisine','type_place','foods','types2'])
    for j in ind:
        df.loc[len(df)]=data.loc[j]
    return df

def check_cuisine(type:str, data:pd.DataFrame)->pd.DataFrame:
    i = 0
    ind = []
    while i < len(data):
        if type in data['categories'][i]:
            ind.append(i)
        i+=1
    df = pd.DataFrame(columns=['name', 'vicinity', 'price_level_x', 'rating_x', 'types',
                        'user_ratings_total', 'lat', 'lng', 'categories', 'attributes', 'hours',
                        'url','cuisine','type_place','foods','types2'])
    for j in ind:
        df.loc[len(df)]=data.loc[j]
    return df

def check_price(level:int, data:pd.DataFrame)->pd.DataFrame:
    target = data[data['price_level_x'] <= level]
    return target

def check_rating(level:int, data:pd.DataFrame)->pd.DataFrame:
    target = data[data['rating_x'] >= level]
    return target

def make_viz(data:pd.DataFrame):
    MAP_FORMAT = {'width': 800,
                 'height': 400,
                 'margin': {'r':0, 't': 0, 'l': 0, 'b': 0},
                 'showlegend': False,
                 'mapbox_style': 'open-street-map'
                 }
    fig = go.Figure(layout=MAP_FORMAT)
    
    points = go.Scattermapbox(lat=data['lat'],
                              lon=data['lng'],
                              text=data['name'],
                              mode='markers+text', 
                              marker=dict(
                                  size=14,
                                  color='blue',
                                  symbol='circle', 
                                  opacity=1
                                ),
                              textposition="top right"
                            )
    fig.add_trace(points)
    fig.update_mapboxes(center={'lat': 37.2707, 'lon': -76.7075},
                        zoom=12
                       )
    fig.show()
    return