# Restaurant Picker for the Indecisive

## The Function: choose_rest()
1. If the data (csv located in this respository) is downloaded to the same place as the function is being run from, the function will have no trouble reading that data in since it is hard coded in at the moment.
2.  Takes optional arguments for ‘cuisine’, ‘type’, ‘price_level’, and ‘rating’

- ‘price_level’ needs to be an integer from 1-4 representing the level you are okay with paying, 4 being the highest and 1 being the lowest.
- ‘rating’ is a float from 0-5 for the average customer rating desired and above, 0 being the lowest and 5 being the highest
- ‘type’ is a string representing the atmosphere or other key attributes- Valid options include: ‘Bars’, ’Pubs’, ’Delis’, ’Fast Food’, ’Bakeries’, ’Cafes’, ’Tapas/Small Plates’, ’Diners’, ’Halal’
- ‘cuisine’ is a string for the desired cuisine type- Valid options include: ‘American’, ’French’, ’Southern’, ’British’, ’Japanese’, ’Greek’, ’Chinese’, ’Spanish’, ’Italian’, ’Thai’, ’Mexican’
