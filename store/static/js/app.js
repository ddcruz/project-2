var map = L.map('map').setView([37.8, -96], 4);
var circlesGroup = L.featureGroup();

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
    '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  id: 'mapbox.light'
}).addTo(map);


// control that shows state info on hover
var info = L.control();

info.onAdd = function (map) {
  this._div = L.DomUtil.create('div', 'info');
  this.update();
  return this._div;
};

info.update = function (props) {
  this._div.innerHTML = '<h4>US Population Density</h4>' +  (props ?
    '<b>' + props.name + '</b><br />' + props.density + ' people / mi<sup>2</sup>'
    : 'Hover over a state');
};

info.addTo(map);


// get color depending on population density value
function getColor(d) {
  return d > 1000 ? '#800026' :
      d > 500  ? '#BD0026' :
      d > 200  ? '#E31A1C' :
      d > 100  ? '#FC4E2A' :
      d > 50   ? '#FD8D3C' :
      d > 20   ? '#FEB24C' :
      d > 10   ? '#FED976' :
            '#FFEDA0';
}

function style(feature) {
  return {
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.7,
    fillColor: getColor(feature.properties.density)
  };
}

function highlightFeature(e) {
  // console.log('mouseover: highlightFeature')
  var layer = e.target;

  layer.setStyle({
    weight: 5,
    color: '#666',
    dashArray: '',
    fillOpacity: 0.7
  });

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
    layer.bringToFront();
  }

  info.update(layer.feature.properties);
}

var geojson;

function resetHighlight(e) {
  // console.log('mouseout: resetHighlight')
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    if (e.originalEvent.shiftKey === false) {
      map.fitBounds(e.target.getBounds());
      updateCityDropDown(e.sourceTarget.feature.properties.state_abbr)
    }

  if (e.originalEvent.shiftKey === true) {
    drawCircles(e.sourceTarget.feature.properties.state_abbr)  
  }

  buildPie(e.sourceTarget.feature.properties.state_abbr)
}

function onEachFeature(feature, layer) {
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: zoomToFeature,
  });
}

geojson = L.geoJson(statesData, {
  style: style,
  onEachFeature: onEachFeature
}).addTo(map);

map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');


var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

  var div = L.DomUtil.create('div', 'info legend'),
    grades = [0, 10, 20, 50, 100, 200, 500, 1000],
    labels = [],
    from, to;

  for (var i = 0; i < grades.length; i++) {
    from = grades[i];
    to = grades[i + 1];

    labels.push(
      '<i style="background:' + getColor(from + 1) + '"></i> ' +
      from + (to ? '&ndash;' + to : '+'));
  }

  div.innerHTML = labels.join('<br>');
  return div;
};

legend.addTo(map);


function drawCircles(state_abbr) {
  
  //remove any previously added circles
  circlesGroup.clearLayers()

  /* data route */
  var url = `/api/city_data/${state_abbr}`;
  d3.json(url).then(function(cities) {

    // Loop through the cities data and create a circle for each store, 
    // and use the density for the radius
    for (var i = 0; i < cities.length; i++) {
      var city = cities[i];
      L.circle(city.location, {
        fillOpacity: 1
        , color: 'white'
        , fillColor: getColor(city.density)
        , radius: city.density
      })
      .bindPopup(city.city + ", " + city.state_abbr +  ":   " + city.density + " people per square km")
      .addTo(circlesGroup);
    }
    map.addLayer(circlesGroup)
  });
}

function updateCityDropDown(state_abbr) {
  //update the state label
  d3.select('#stateDropDownLabel').select('h5').text(`Select a city in ${state_abbr} from the list below:`)
  d3.select('#stateDropDownLabel').select('h4').text(`${state_abbr}`)

  // Grab a reference to the dropdown select element
  var selector = d3.select("#cityselector");

  //clear any previous dropdown values
  selector.selectAll('option').remove()
  
  // Use the list of sample names to populate the select options
  d3.json(`api/city_list/${state_abbr}`).then((cities) => {
    cities.forEach((city) => {
      selector
        .append("option")
        .text(city.city)
        .property("value", city.city);
    });

    // Use the first city from the list to build the initial plots
    optionChanged(cities[0].city); 
  });
   buildCharts(state_abbr);
   buildPie(state_abbr)
}

function buildCharts(state_abbr) {
  var state_abbr = d3.select('#stateDropDownLabel').select('h4').text()

  var url = `/api/plot/${state_abbr}`

  d3.json(url).then(data=> {
    // console.log(data)
    var trace1 = {
      'x': data.med_age,
      'y': data.med_income,
      'text': data.cities,
      'mode': 'markers',
      'marker': {
        // size: data.med_age,
        // color: 'blue'
      }
    };
    var layout1 = {
        title: {
          text:`${state_abbr} Median Age vs Median Income`,
          font: {
            size: 24
          }
        },
        height: 700,
        width: 1100,
        xaxis: {
          title: {
            text: 'Median Age (Years)'
          }
        },
        yaxis: {
          title: {
            text: 'Median Household Income (US Dollars)'
          }
        }
      }
      Plotly.newPlot("chart2", [trace1], layout1)
  });
};

function buildPie(state_abbr) {
  // var state_abbr = d3.select('#stateDropDownLabel').select('h4').text()
  console.log(state_abbr)
  var url = `/api/pie/${state_abbr}`

  d3.json(url).then(data=> {
    // console.log(data)
    var trace1 = {
      values: data.population,
      labels: data.cities,
      type: 'pie'
    };
    var layout1 = {
        title: {
          text:`${state_abbr} Top 10 Population`,
          font: {
            size: 14
          }
        },
        height: 400,
        width: 400,
      }
      Plotly.newPlot("chart1", [trace1], layout1)
  });
};




function showCityInfo(city) {
  // select state
  var state_abbr = d3.select('#stateDropDownLabel').select('h4').text()

  var url = `/api/demographics/${state_abbr}/${city}`

  var select_city = d3.select("#city-data")

  select_city.html("")

  d3.json(url).then(data=> {
    // console.log(data)
    var sortedData = {
        city: data.city,
        state: data.state,
        population: data.population, 
        median_age: data.median_age,
        avgerage_household_size: data.avgerage_household_size,
        median_income: data.median_income,
        household_income: data.household_income,
        per_capita_income: data.per_capita_income
      }
    
    // reformat keys: replace "_" with " " + capitalize first letter of each word
    function formatText(string) {
      var correctText = string.replace(/_/g,' ').split(' ').map(x=> x.charAt(0).toUpperCase() + x.slice(1)).join(' ')
      return correctText
    }


    Object.entries(sortedData).forEach(([key, value])=> {
      var p = select_city.append("p")
      p.text(`${formatText(key)}: ${value}`)
    })
  })

}

function optionChanged(city) {
  // buildCharts(city); 
  showCityInfo(city); 
}


function init() {
  updateCityDropDown('TX')
}

init()