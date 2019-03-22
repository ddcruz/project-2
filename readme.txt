Data Sources:
RadientVis JS library, to generate the colors for the gradients
https://stackoverflow.com/questions/3080421/javascript-color-gradient

city data for density per mi squared
https://simplemaps.com/data/us-cities

the idea for the map
http://www.city-data.com/#data

leaflet inteative choropleth tutorial
https://leafletjs.com/examples/choropleth/

Overpass API:
https://lz4.overpass-api.de/api/interpreter

Census Data:
https://www.census.gov/developers/

What each team member contributed:
1. DJ: Store Data, review struggle with reverse Geocoding, worked with Eric on scatter plot and pie chart
2. Eric: Setup front end HTML framework, worked with DJ on scatter plot and pie chart
3. Michael: Census data per state with a BindOnPopup for the Leaflet circles, App routes for the city demographic data
4. Dexter: Interactive choropleth map using leaflet and a custom control to respond to mouse events over each state. 
Leaftlet circles to display each city using the density of each city as the radius. 
SQLite db to store the data and power the API routes
Heroku to host the app


Lesson’s learned / difficulties overcome:
1. Difficulty with API calls for Geocoding
2. Resizing the pie chart to interact with each state
3. Problem Michael and Dexter had with dealing with multiple promises for the detailed pop up
4. Dexter: getting the circle radius to reflect properly
5. Performing the square km to square mi conversion in the proper place in the code.


Technologies Used:
1. HTML / CSS
2. JS
3. Python / Flask
4. Jupyter Notebook
5. D3
6. Plotly
7. Leaftlet
8. sqlite
9. Heroku