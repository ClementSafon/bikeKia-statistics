# BikeKIA - Statistics

## Description

This projet is a dockerized application that collecte data from a bike station and store it in a database. To access the data, a web API is available.

## The web API

The web API is available at the following address: http://server_name:8080
And the different endpoints are:

- / : return the status of the API
- /get_all : return the list of all the bikes positions collected
- /get_all_stations : return the list of all the stations
- /get_all_bikes_by_id/<bike_id> : return the list of all the positions of the bike with the id <bike_id>
- /get_bike_by_station/<station_id> : return the list of all the bikes seen at the station with the id <station_id>
- /get_bike_by_id_and_station/<bike_id>/<station_id> : return the list of all the positions of the bike with the id <bike_id> seen at the station with the id <station_id>

## Utilisation

You can host this service on a server and use it to collect data from a bike station. Then you can use a local app to display the data at your convenience.

## Tips

Don't forget to had some firewalls and reconfigure the CORS policy to secure your server.
