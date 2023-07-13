import requests
import mysql.connector
import time
import xml.etree.ElementTree as ET

MESASURE_INTERVAL = 5*60  # 5 minutes
RETRYING_INTERVAL = 60  # 1 minute

# wait for mysql to start properly
time.sleep(15)


def create_table():
    try:
        mydb = mysql.connector.connect(
            host="mysql",
            user="root",
            password="passwd",
            database="bikeKia"
        )
    except:
        return ("Error: Could not connect to the database.")
    else:
        cursor = mydb.cursor()
        # set the time zone to europe/paris
        cursor.execute("SET GLOBAL time_zone = 'Europe/Paris';")
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS bike_data (
                id INTEGER AUTO_INCREMENT,
                bike_id INTEGER,
                bikeType INTEGER,
                active INTEGER,
                boardcomputer VARCHAR(255),
                station_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            )
            """
        cursor.execute(create_table_query)
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS station_data (
                id INTEGER,
                name VARCHAR(255),
                lng VARCHAR(255),
                lat VARCHAR(255),
                PRIMARY KEY (id)
            )
            """
        cursor.execute(create_table_query)
        mydb.commit()
        mydb.close()
        return


def fetch_data():
    # Fetch the resource
    try:
        response = requests.get(
            "http://iframe.nextbike.net/maps/nextbike-live.xml?city=538")
        xml_data = response.text
        root = ET.fromstring(xml_data)
    except:
        return ("Error: Could not fetch data.")
    else:
        try:
            # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host="mysql",
                user="root",
                password="passwd",
                database="bikeKia"
            )
        except:
            return ("Error: Could not connect to the database.")
        else:
            # Create a cursor object to execute SQL queries
            cursor = mydb.cursor()

            data_bikes = []

            # Parse the XML
            city_element = root.find('country/city')
            places = city_element.findall('place')
            for place in places:
                # Store the station data in the database
                station_name = place.get('name')
                lng = place.get('lng')
                lat = place.get('lat')
                station_id = place.get('uid')
                insert_query = f"""
                    INSERT INTO station_data (id, name, lng, lat)
                    VALUES ('{station_id}', '{station_name}', '{lng}', '{lat}')
                    ON DUPLICATE KEY UPDATE
                    id = '{station_id}'
                    """
                cursor.execute(insert_query)
                if int(place.get('bikes')) >= 1:
                    bikes = place.findall('bike')
                    for bike in bikes:
                        data_bikes.append({
                            'bike_id': int(bike.get('number')),
                            'bike_type': int(bike.get('bike_type')),
                            'active': int(bike.get('active')),
                            'boardcomputer': bike.get('boardcomputer'),
                            'station_id': int(station_id),
                        })

            # Store the data in the database
            for bike in data_bikes:
                insert_query = f"""
                    INSERT INTO bike_data (bike_id, bikeType, active, boardcomputer, station_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    bike['bike_id'],
                    bike['bike_type'],
                    bike['active'],
                    bike['boardcomputer'],
                    bike['station_id'],
                ))

            # Commit the changes and close the connection
            try:
                mydb.commit()
                mydb.close()
            except:
                return ("Error: Could not commit changes to the database.")
            else:
                return


if __name__ == "__main__":
    ret = create_table()
    if ret is not None:
        print(ret + f" Retrying in {RETRYING_INTERVAL} seconds...")
        time.sleep(RETRYING_INTERVAL)

    while True:
        ret = fetch_data()
        if ret is None:
            print(
                f"Data fetched successfully. Waiting {MESASURE_INTERVAL} minutes...")
            time.sleep(MESASURE_INTERVAL*60)
        else:
            print(ret + f" Retrying in {RETRYING_INTERVAL} seconds...")
            time.sleep(RETRYING_INTERVAL)
