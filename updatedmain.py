import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random

def choose_rest(data:pd.DataFrame = pd.read_csv('update_data.csv'),
                day:str = None,
                time:int = None,
                lucky:bool = True,
                price_level:int = None, 
                rating:float = None,
                cuisine:str = None,
                type:str = None,
                food:str = None
               ) -> pd.DataFrame:
    '''
    This function selects a restaurant(s) based on the user inputs, displays a figure, and returns a dataframe with the restaurants most closely matching the inputs. Will be between 1 and 5 entries shown and plotted on the map.

    Inputs:
        data(pd.DataFrame): A dataframe containing restaurant data. 
            the dataframe read from the file 'update_data.csv' is the default value for this argument.
        day(str, optional): Day of the week. 
            Valid inputs include: ('mon','tues','wed','thurs','fri','sat','sun')
            Without a specified day of the week the subsequent code will be run on the entire data set and could
            result in a closed establishment.
        time(int, optional): Time of day. A valid input is an integer between 0-2400 in military time format. 
            Including a time without a day will have no impact on the results.
            ex. 2:30pm would be entered as 1430
        lucky(bool): Default set to True, no other specifications are used and a restaurant is selected at random.
            Must be set to False if optional arguments are desired.
        price_level(int, optional): Integer between 1-4 indicating the price level they are willing to spend.
        rating(float, optional): Float between 0-5 indicating the ideal reviews rating.
        cuisine(str, optional): Desired cuisine type. 
            Valid inputs include: ('American', 'French', 'Southern', 'British', 'Japanese',
                          'Greek', 'Chinese', 'Spanish', 'Italian', 'Thai', 'Mexican')
        type(str, optional): Desired atomosphere or trait. 
            Valid inputs include: ('Pubs', 'Bars', 'Delis', 'Store', 'Delivery', 'Fast Food', 'Cafes',
                          'Bakeries', 'Tapas/Small Plates', 'Diners', 'Halal')
        food(str, optional): Desired food. 
            Vaid inputs include: ('Barbeque', 'Seafood', 'Pizza', 'Chicken', 'Sandwiches', 'Sushi', 
                          'Breakfast, Brunch, Coffee', 'Salad', 'Burgers', 'Desserts', 'Wraps', 'Soup')
    '''
#first get subset of open restaurants
    if day is not None and time is not None:
        df = sub_open(data,day,time)
    else:
        df = data

#structure of  below conditional blocks: if the respective optional argument is provided, a subset with entries matching the specified value will be assigned to the variable df_(respective variable). If the argument is not provided, the variable will be assigned None for usage in the get_max function inputs.
    if cuisine is not None:
        df_cuisine = check_cuisine(cuisine, df)
        df_cuisine.reset_index(inplace = True, drop = True)
    else:
        df_cuisine = None
    if type is not None:
        df_type = check_type(type, df)
        df_type.reset_index(inplace = True, drop = True)
    else:
        df_type = None
    if price_level is not None:
        df_price = check_price(price_level, df)
        df_price.reset_index(inplace = True, drop = True)
    else:
        df_price = None
    if rating is not None:
        df_rate = check_rating(rating, df)
        df_rate.reset_index(inplace = True, drop = True)
    else:
        df_rate = None
    if food is not None:
        df_food = check_for_food(food,df)
        df_food.reset_index(inplace = True, drop = True)
    else:
        df_food = None
        
    dataframes = [df_cuisine, df_type, df_price, df_rate, df_food]
#following conditional accounts for the case of the user wanting a totally random output(no optional arguments added) 
    if lucky == True: #if lucky is not set to False it chooses 1 random selection 
        if any(df is not None for df in dataframes): #if arguments are specified, but lucky = True, the code will continue to run after the printed statement.
            print('Arguments were specified, but random choice is provided (default lucky = True). If specifications are desired, set lucky = False')
        val = random.sample(range(0,len(df)),1) #choose a random index in the dataframe
        target = df[df.index.isin(val)]
#if the lucky argument is set to False and at least one optional argument is specified the get_max function is used to determine which entries satisfy the most conditions specified
    else: #lucky = False
        if any(df is not None for df in dataframes): #at least one of the dataframes had a valid input resulting in a subset of the restaurant data
            names = get_max(cuisine = df_cuisine, type = df_type, price = df_price, rating = df_rate, food = df_food)
        else: #no valid arguments while lucky = False, code breaks after the printed statement
            print('No valid arguments were provided, set lucky = True, or specify a valid argument for at least one of: price_level, cuisine, rating, type, food. Check README.md for valid arguments.')
            return
        if len(names) > 5:#if more than 5 resturants tie with the max number of matching qualifications, 5 are randomly chosen
            vals = random.sample(range(0, len(names)), 5) #5 random indecies chosen in the list of restaurants
            temp = []
            for item in vals:
                temp.append(names[item])
            names = temp
        target = df[df['Name'].isin(names)]

    make_viz(target) #function call to make the visualization with the 1-5 resturants selected
    if day is not None:
        return target[['Name','Address','Price Level','Rating','Total Ratings',
                       'Cuisine', 'Attributes', 'Foods',day+'_open',day+'_close']] #relevant information that may be desired is returned for the 1-5 resturants that are plotted as well
    else:
        return target[['Name','Address','Price Level','Rating','Total Ratings',
                       'Cuisine', 'Attributes', 'Foods']]

def add_to_dict(input:pd.DataFrame, count:dict) -> dict:
    '''
    Helper function used to update the count dictionary for each variable that has a non null dataframe.
    
    Inputs:
        input(pd.DataFrame): The dataframe of selected restaurants.
        count(dict): Contains the restaurants and the number of times they match a criteria.

    Returns:
        dict: Updated restaurants and the number of times they match a criteria.
    '''
    var = input
    i = 0
    while i < len(var): #loops through all the entries in the dataframe input into this function to add a tally to the count dictionary, since the restaurant was present in a subset for a matching trait
        if var['Name'][i] in count: #if the name of the restaurant is already a key in the count dictionary, then the value += 1
            count[var['Name'][i]] += 1
            i += 1
        else: #if the name of the restaurant is not already a key in the count dictionary, a new key is added and the value = 1
            count[var['Name'][i]] = 1
            i+=1
    return count

def get_max(price:pd.DataFrame = None, 
            rating:pd.DataFrame = None, 
            cuisine:pd.DataFrame = None,
            type:pd.DataFrame = None,
            food:pd.DataFrame = None
           ) -> list[str]:
    '''
    Helper function used to determine the restaurants with the max value of matches in the matching qualifications dictionary.
    
    Inputs:
        price(pd.DataFrame, optional): The dataframe of selected restaurants for price arg.
        rating(pd.DataFrame, optional): The dataframe of selected restaurants for rating arg.
        cuisine(pd.DataFrame, optional): The dataframe of selected restaurants for cuisine arg.
        type(pd.DataFrame, optional): The dataframe of selected restaurants for type arg.
        food(pd.DataFrame, optional): The dataframe of selected restaurants for food arg.
 
    Returns:
        list[str]: A list of restaurant names that have the max number of criteria met.
    '''
    count = {}
#structure of following conditionals: if a dataframe that is not None is passed into the function (entries matching desired qualification for the argument), the block for the respective argument will be entered and the function add_to_dict is run for that dataframe to add a tally to the count dictionary for each of those entries.
    if cuisine is not None:
        count = add_to_dict(cuisine, count)
    if type is not None:
        count = add_to_dict(type, count)
    if price is not None:
        count = add_to_dict(price, count)
    if rating is not None:
        count = add_to_dict(rating, count)
    if food is not None:
        count = add_to_dict(food, count)

#following loop is to find the max value in the dict (represents the max number of criteria met)
    num = 0
    for key in count:
        if count[key] > num:
            num = count[key]
#following loop determines if each key has the max value and if it does, that key is added to a list containing the names of the ideal restaurants which is returned by the function.
    temp = []
    for key in count:
        if count[key] == num:
            temp.append(key)
    return temp

def sub_open(data:pd.DataFrame, dow:str, time:int) -> pd.DataFrame:
    '''
    Subsets the full dataframe to only include the restaurants that open for the day and time specified. This subset is used for rest of the searching.
    
    Inputs:
        dow(str): Day of the week. 
            Valid inputs include: ('mon','tues','wed','thurs','fri','sat','sun')
        time(int): Time of day. A valid input is an integer between 0-2400 in military time format.
            ex. 2:30pm would be entered as 1430
        data(pd.DataFrame): The dataframe of restaurants.

    Returns:
        pd.DataFrame: Subset including only the open restaurants.
    '''
    i = 0
    ind = []
    while i < len(data):
        if pd.notna(data[dow+'_open'][i]): #if there is a not null entry for the opening time on the specified day
            open = int(data[dow+'_open'][i]) #the open and close times are established as int variables
            close = int(data[dow+'_close'][i])
            if time in range(open, close+1): #determine if the specified time is in the range of open and close times
                ind.append(i) #if the restaurant is open, the i value(the index of the entry) is added to a list
        i += 1
    open_data = data[data.index.isin(ind)] #full dataset is subset to only include the entries where the index is in the list of the indecies of the open restaurants
    open_data.reset_index(inplace = True, drop = True) #index reset to prevent later problems with indexing
    return open_data

def checker(column:str, type:str, data:pd.DataFrame) -> pd.DataFrame:
    '''
    Helper function to subset the the open restaurants data to include entires matching the desired qualification. Used in the check_type, check_cuisine, and check_food functions.
    
    Inputs:
        column(str): The variable in the dataframe that is being searched for the desired input.
        type(str): Desired quality from the user that is being searched for in the column of interest.
        data(pd.DataFrame): The dataframe of restaurants.

    Returns:
        pd.DataFrame: Subset of the restaurants including the desired qualification in the column(variable) of interest.
    '''
    i=0
    ind = []
    while i < len(data): #loops through the set of data provided
        if type in data[column][i]: #if the specified attribute(type) is contained within the specified variable(column) for each row the index is added to a list
            ind.append(i)
        i+=1
    sub_df = data[data.index.isin(ind)] #subsets the data to include only the entries with indecies in the list created above
    return sub_df
    
def check_type(type:str, data:pd.DataFrame) -> pd.DataFrame:
    '''
    The optional argument for the type of restaurant is specified and the 'Attributes' column is searched for the desired trait.
    
    Inputs:
        type(str): Desired atomosphere or trait. 
            Valid inputs include: 'Pubs', 'Bars', 'Delis', 'Store', 'Delivery', 'Fast Food', 'Cafes',
                          'Bakeries', 'Tapas/Small Plates', 'Diners', 'Halal'
        data(pd.DataFrame): The dataframe of restaurants.
        
    Returns:
        pd.DataFrame: Subset of the restaurants including the desired type of restaurant.
    
    '''
    return checker('Attributes',type,data) #runs the checker function for desired input(type) in the 'Attributes' column with the given data

def check_cuisine(type:str, data:pd.DataFrame) -> pd.DataFrame:
    '''
    The optional argument for the cuisine is specified and the 'Cuisine' column is searched for the desired trait.
    
    Inputs:
        type(str): Desired cuisine type. 
            Valid inputs include: 'American', 'French', 'Southern', 'British', 'Japanese',
                          'Greek', 'Chinese', 'Spanish', 'Italian', 'Thai', 'Mexican'
        data(pd.DataFrame): The dataframe of restaurants.

    Returns:
        pd.DataFrame: Subset of the restaurants including the desired cuisine.
    '''
    return checker('Cuisine',type,data) #runs the checker function for desired input(type) in the 'Cuisine' column with the given data

def check_for_food(item:str, data:pd.DataFrame) -> pd.DataFrame:
    '''
    The optional argument a food is specified and the 'Foods' column is searched for the desired trait.
    
    Inputs:
        type(str): Desired food. 
            Vaid inputs include: 'Barbeque', 'Seafood', 'Pizza', 'Chicken', 'Sandwiches',
                         'Sushi', 'Breakfast, Brunch, Coffee', 'Salad', 'Burgers',
                         'Desserts', 'Wraps', 'Soup'
        data(pd.DataFrame): The dataframe of restaurants.

    Returns:
        pd.DataFrame: Subset of the restaurants including the desired food item.
    '''
    return checker('Foods',item,data) #runs the checker function for desired input(type) in the 'Foods' column with the given data

def check_price(level:int, data:pd.DataFrame) -> pd.DataFrame:
    '''
    The optional argument for the price level is specified and the 'Price Level' column is searched for the desired trait.
    
    Inputs:
        level(int): Integer between 1-4 indicating the price level they are willing to spend.
        data(pd.DataFrame): The dataframe of restaurants.
        
    Returns:
        pd.DataFrame: Subset of the restaurants with desired price level and below.
    '''
    return data[data['Price Level'] <= level] #subsets the given data to include only entries where the price level is less than or equal to the input

def check_rating(level:float, data:pd.DataFrame) -> pd.DataFrame:
    '''
    The optional argument for the desired rating is specified and the 'Rating' column is searched for the desired trait.
    
    Inputs:
        level(float): Float between 0-5 indicating the ideal reviews rating.
        data(pd.DataFrame): The dataframe of restaurants.
        
    Returns:
        pd.DataFrame: Subset of the restaurants with desired rating and above.
    '''
    return data[data['Rating'] >= level] #subsets the given data to include only entries where the rating is greater than or equal to the input

def make_viz(data:pd.DataFrame) -> None:
    '''
    This function generates and displays a figure with the selected restaurant(s), but does not return any value.
    '''
    #format specifications
    MAP_FORMAT = {'width': 800, 
                 'height': 400,
                 'margin': {'r':0, 't': 0, 'l': 0, 'b': 0},
                 'showlegend': False
                 }
    fig = go.Figure(layout=MAP_FORMAT) #creates fig with format specifications
    
    points = go.Scattermapbox(lat=data['lat'], #latitude = appropriate column
                              lon=data['lng'], #longitude = appropriate column
                              text=data['Name'], #main text is the name of the restaurant
                              customdata = data['Address'], #add address as custom data to use in the hovertext
                              mode='markers', #show only the markers and not text because the text overlapped some of the points when shown and made the map look more clunky- made the choice to take them out because the name is included in the hovertext so one can still identify the points by hovering over them
                              marker=dict( #settings for the points
                                  size=14,
                                  color='purple',
                                  symbol='circle', 
                                  opacity=1
                                )
                            )
    fig.add_trace(points) #add the points to the map
    fig.update_traces(hovertemplate="%{text}<br>%{customdata}") #add the hovertext data

    fig.update_layout(mapbox_style="carto-positron") #update the map style

    fig.update_mapboxes(center={'lat': 37.2707, 'lon': -76.7075},zoom=12) #center the map on williamsburg and set an appropriate zoom level
    fig.show()
    return
    
if __name__ == '__main__': #run the main program-> runs the choose_rest function
    choose_rest()