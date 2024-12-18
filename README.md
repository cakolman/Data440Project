# Restaurant Picker for the Indecisive

1. If the data (csv located in this respository) is downloaded to the same place as the function is being run from, the function will have no trouble reading that data in since it is hard coded in the fuction as if the csv is in the same place. If the csv is located elsewhere, just make sure to specify data = the path to your file in choose_rest()
2. choose_rest() with no arguments specified, generating a random result is the default when running the main py
3. from main import choose_rest
4. To run the function, specify any number of the optional arguments, or none at all for a random result. If an open restaurant is desired, make sure to input both day and time otherwise the code will run on the full dataset and could result in a closed restaurant being returned.

## The Function: choose_rest()
Selects either 1 random restaurant if the lucky argument (explained below) is left as the default True, or selects at most 5 restaurants that most closely match the criteria inputted. These choices are displayed on a map and in a dataframe including some additional useful information about the establishments.

Inputs:
- data(pd.DataFrame): A dataframe containing restaurant data. The dataframe read from the file 'update_data.csv' is the default value for this argument, so it is not necessary to specify one’s own data.
- day(str, optional): Day of the week. Valid inputs include: ('mon','tues','wed','thurs','fri','sat','sun'). Without a specified day of the week the subsequent code will be run on the entire data set and could result in a closed establishment.
- time(int, optional): Time of day. A valid input is an integer between 0-2400 in military time format. ex. 2:30pm would be entered as 1430. Including a time without a day will have no impact on the results.
- lucky(bool): Default set to True, no other specifications are used and a restaurant is selected at random. Must be set to False if optional arguments are desired.
- price_level(int, optional): Integer between 1-4 indicating the price level they are willing to spend.
- rating(float, optional): Float between 0-5 indicating the ideal reviews rating.
- cuisine(str, optional): Desired cuisine type. Valid inputs include: ('American', 'French', 'Southern', 'British', 'Japanese', 'Greek', 'Chinese', 'Spanish', 'Italian', 'Thai', 'Mexican')
- type(str, optional): Desired atmosphere or trait. Valid inputs include: ('Pubs', 'Bars', 'Delis', 'Store', 'Delivery', 'Fast Food', 'Cafes','Bakeries', 'Tapas/Small Plates', 'Diners', 'Halal’)
- food(str, optional): Desired food. Valid inputs include: ('Barbeque', 'Seafood', 'Pizza', 'Chicken', 'Sandwiches', 'Sushi', 'Breakfast, Brunch, Coffee', 'Salad', 'Burgers', 'Desserts', 'Wraps', 'Soup')

First the choose_rest() function uses the sub_open() function with the inputs: data,day,time to find a subset of the open restaurants. If day and time are not specified, or if only one or the other are specified, the sub_open() function will not get run and the subsequent code will run on the whole dataset.

- sub_open() takes the inputs: data, day, and time(same as above). This function works by checking if the time input is within the open and close hours for the desired day. It then creates a subset with all the rows where this condition is met.

Five variables are specified at this stage of the function: df_cuisine, df_type, df_price, df_rate}, and df_food. If the respective argument was specified, the function to check for it (explained below) is used and the variable is set to the subsetted dataframe. If an argument is not specified, the variable is set to None. The result will be some combination of dataframes and Nones depending on the arguments specified.

- check_price() takes the inputs: price_level and data. It checks the ‘Price Level’ column for entries where the price is less than or equal to the price_level input and returns a subset of the data where that condition is met.
- check_rating() takes the inputs: rating and data. It checks the ‘Rating’ column for the entries where the rating is greater than or equal to the rating input and returns a subset of the data where that condition is met.
- checker() takes the inputs: column(variable), type(input attribute), and data. This is a helper function for the following check functions. It finds the rows where the desired input is included in the search column. The data is then subset to only include these rows.
- check_cuisine() takes the inputs: type(input attribute) and data and uses checker() with the column argument specified as ‘Cuisine’ to return a subset of the data that matches the desired attribute.
- check_type() takes the inputs: type(input attribute) and data and uses checker() with the column argument specified as ‘Attributes’ to return a subset of the data that matches the desired attribute.
- check_for_food() takes the inputs: type(input attribute) and data and uses checker() with the column argument specified as ‘Foods’ to return a subset of the data that matches the desired attribute.

Before anything else occurs, the choose_rest() function checks if lucky = True. If this condition is satisfied, a random number is picked and the variable target (this is the final chosen entries) is set to a subset of the data at the index of that random number.

If lucky = False and at least one of [df_cusine, df_type, df_price, df_rate, df_food] is not None, the get_max() function is used with the inputs: df-cuisine, df-type, df-price, df-rate, df-food and this provides a list of the restaurants that satisfied the most conditions.

- get_max() takes in all of the dataframe and none objects as arguments and returns a list of strings which are the restaurant names. For each of the respective arguments, if it is not None, the function add-to-dict() is used. A dictionary is returned from that function and gets added to with each argument that is not None. After the dictionary is filled (add-to-dict() on each of the arguments that are not None), the next step in the function is determining the max value that exists within the dictionary. A list is then created and returned with each key that has that max value in it.
- add_to_dict() takes in one of [df_cuisine, df_type, df_price, df_rate, df_food], for which argument it is run on and also takes in a dictionary. This function iterates through the passed in dataframe and determines if that ‘Name’ already exists as a key in the dictionary. If it does, the value += 1. If not, the key is added with the value 1. This dictionary is a count of the times a restaurant is recognized in one of the dataframes passed into the get-max() function which represents everytime it satisfies a condition.

If the length of the returned list is longer than 5, 5 random values are chosen and a new list is created to only include the names at the indices of those random values in the initial list.

Now that the list of names is 5 or shorter, the target variable is assigned a subset of the data where the ‘Name’ is in the list of names. This dataframe target is then used in the make-viz() function and target[['Name','Address','Price Level','Rating','Total Ratings', 'Cuisine', 'Attributes', 'Foods',day+'_open',day+'_close']] is returned as useful information.

- make-viz() This function generates and displays a figure with the selected restaurant(s). The only argument that this function takes is data(dataframe). The map is created with the specifications: (width = 800, height = 400, margin = {'r':0, 't': 0, 'l': 0, 'b': 0}, and showledgend = False). Additional settings include: customdata = data['Address'], hovertext displays text = ['Name'] and customdata, marker settings: size = 14, color = purple, opacity = 1, symbol = circle, mapbox style = carto-positron, and the map is centered at {'lat': 37.2707, 'lon': -76.7075} with zoom=12. The coordinates for the center are the middle of Williamsburg, VA. If one wanted to redo this project with data for a different city, these coordinates would need to be changed accordingly.
