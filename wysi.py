# This file contains the WSGI configuration required to serve up your
# web application at http://DhruvinSoni.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError


# +++++++++++ HELLO WORLD +++++++++++
# A little pure-wsgi hello world we've cooked up, just
# to prove everything works.  You should delete this
# code to get your own working.


HELLO_WORLD = """
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8' />
    <title>Significant Earthquakes in 2015</title>
    <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
	<script src='https://api.tiles.mapbox.com/mapbox-gl-js/v0.53.0/mapbox-gl.js'></script>
<link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.53.0/mapbox-gl.css' rel='stylesheet' />
	<script src="https://d3js.org/d3.v3.min.js"></script>
	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <style>
        body { margin:0; padding:0; }
        #map { position:absolute; top:0; bottom:0; width:100%; }
    </style>
</head>
<body>

<style>
.map-overlay {
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
    position: absolute;
    width: 25%;
    top: 0;
    left: 0;
    padding: 10px;
}

.map-overlay .map-overlay-inner {
    background-color: #fff;
    box-shadow:0 1px 2px rgba(0, 0, 0, 0.20);
    border-radius: 3px;
    padding: 10px;
    margin-bottom: 10px;
}

.map-overlay h2 {
    line-height: 24px;
    display: block;
    margin: 0 0 10px;
}

.map-overlay .legend .bar {
    height: 10px;
    width: 100%;
    background: linear-gradient(to right, #FCA107, #7F3121);
}

.map-overlay input {
    background-color: transparent;
    display: inline-block;
    width: 100%;
    position: relative;
    margin: 0;
    cursor: ew-resize;
}
</style>
<div id='map'></div>

<div class='map-overlay top'>

<button type="button" class="btn btn-sm btn-default" onclick="document.location='index.html'">< Go Back to Home</button>
    <div class='map-overlay-inner'>
        <h5>Significant earthquakes in 2015</h5>
        Month of 2015:<label id='month'></label>
        <input id='slider' type='range' min='0' max='11' step='1' value='0' />
		<br>
		<a href="https://docs.mapbox.com/mapbox-gl-js/assets/significant-earthquakes-2015.geojson">data</a>
    </div>
    <div class='map-overlay-inner'>
        <div id='legend' class='legend'>
            <div class='bar'></div>
            <div>Magnitude (m)</div>
        </div>
    </div>
</div>

<script src='//d3js.org/d3.v3.min.js' charset='utf-8'></script>
<script>
mapboxgl.accessToken = 'pk.eyJ1IjoiZGhydXZpbnNvbmkiLCJhIjoiY2pzMDlzaDBpMWNrMjQ1bHh5aXk3OGF6biJ9.LhQnGJHeEzcvOUwRlEypLg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [31.4606, 20.7927],
    zoom: 0.5
});

var months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
];

function filterBy(month) {

    var filters = ['==', 'month', month];
    map.setFilter('earthquake-circles', filters);
    map.setFilter('earthquake-labels', filters);

    // Set the label to the month
    document.getElementById('month').textContent = months[month];
}

map.on('load', function() {

    // Data courtesy of http://earthquake.usgs.gov/
    // Query for significant earthquakes in 2015 URL request looked like this:
    // http://earthquake.usgs.gov/fdsnws/event/1/query
    //    ?format=geojson
    //    &starttime=2015-01-01
    //    &endtime=2015-12-31
    //    &minmagnitude=6'
    //
    // Here we're using d3 to help us make the ajax request but you can use
    // Any request method (library or otherwise) you wish.
    //d3.json('data/significant-earthquakes-2015.geojson', function(err, data) {
    d3.json('https://docs.mapbox.com/mapbox-gl-js/assets/significant-earthquakes-2015.geojson', function(err, data) {
        if (err) throw err;

        // Create a month property value based on time
        // used to filter against.
        data.features = data.features.map(function(d) {
            d.properties.month = new Date(d.properties.time).getMonth();
            return d;
        });

        map.addSource('earthquakes', {
            'type': 'geojson',
            data: data
        });

        map.addLayer({
            'id': 'earthquake-circles',
            'type': 'circle',
            'source': 'earthquakes',
            'paint': {
                'circle-color': [
                    'interpolate',
                    ['linear'],
                    ['get', 'mag'],
                    6, '#FCA107',
                    8, '#7F3121'
                ],
                'circle-opacity': 0.75,
                'circle-radius': [
                    'interpolate',
                    ['linear'],
                    ['get', 'mag'],
                    6, 20,
                    8, 40
                ]
            }
        });

        map.addLayer({
            'id': 'earthquake-labels',
            'type': 'symbol',
            'source': 'earthquakes',
            'layout': {
                'text-field': ['concat', ['to-string', ['get', 'mag']], 'm'],
                'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
                'text-size': 12
            },
            'paint': {
                'text-color': 'rgba(0,0,0,0.5)'
            }
        });

        // Set filter to first month of the year
        // 0 = January
        filterBy(0);

        document.getElementById('slider').addEventListener('input', function(e) {
            var month = parseInt(e.target.value, 10);
            filterBy(month);
        });
    });
});
</script>

</body>
</html>"""

def application(environ, start_response):
    if environ.get('PATH_INFO') == '/':
        status = '200 OK'
        content = HELLO_WORLD
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
    start_response(status, response_headers)
    yield content.encode('utf8')


# Below are templates for Django and Flask.  You should update the file
# appropriately for the web framework you're using, and then
# click the 'Reload /yourdomain.com/' button on the 'Web' tab to make your site
# live.

# +++++++++++ VIRTUALENV +++++++++++
# If you want to use a virtualenv, set its path on the web app setup tab.
# Then come back here and import your application object as per the
# instructions below


# +++++++++++ CUSTOM WSGI +++++++++++
# If you have a WSGI file that you want to serve using PythonAnywhere, perhaps
# in your home directory under version control, then use something like this:
#
#import sys
#
#path = '/home/DhruvinSoni/path/to/my/app
#if path not in sys.path:
#    sys.path.append(path)
#
#from my_wsgi_file import application  # noqa


# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
#import os
#import sys
#
## assuming your django settings file is at '/home/DhruvinSoni/mysite/mysite/settings.py'
## and your manage.py is is at '/home/DhruvinSoni/mysite/manage.py'
#path = '/home/DhruvinSoni/mysite'
#if path not in sys.path:
#    sys.path.append(path)
#
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
#
## then:
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()



# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
#
#import sys
#
## The "/home/DhruvinSoni" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/DhruvinSoni/myproject"
#path = '/home/DhruvinSoni/path/to/flask_app_directory'
#if path not in sys.path:
#    sys.path.append(path)
#
#from main_flask_app_file import app as application  # noqa
#
# NB -- many Flask guides suggest you use a file called run.py; that's
# not necessary on PythonAnywhere.  And you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.
