from typing import Union

import mysql.connector  # type: ignore
from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

import datetime

app = FastAPI()

# MySQL database configuration
mysql_config = {
    'user': 'root',
    'password': 'passwd',
    'host': 'mysql',
    'database': 'bikeKia',
}

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def execute_mysql_query(query: str):
    """
    Executes a MySQL query and returns the result with column names.
    """
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    connection.close()

    # Convert the result to a list of dictionaries with keys as column names
    formatted_result = []
    for row in result:
        formatted_result.append(dict(zip(column_names, row)))

    return formatted_result


@app.get("/")
def check_runner_status():
    # Get the current time
    current_time = datetime.datetime.now()

    # Calculate the time 5 minutes ago
    five_minutes_ago = current_time - datetime.timedelta(minutes=5)

    # Construct the query to get the latest insert within the past 5 minutes
    query = f"SELECT * FROM bike_data JOIN station_data ON bike_data.station_id = station_data.id WHERE created_at >= '{five_minutes_ago}' ORDER BY created_at DESC LIMIT 1"

    # Execute the query and retrieve the result
    result = execute_mysql_query(query)

    # Check if there is a result within the past 5 minutes
    if result:
        return {"Runner Status": "On"}
    else:
        return {"Runner Status": "Off"}


@app.get("/get_all")
def read_item(q: Union[str, None] = None):
    query = "SELECT * FROM bike_data JOIN station_data ON bike_data.station_id = station_data.id"
    result = execute_mysql_query(query)
    return {"result": result}


@app.get("/get_bike_by_id/{bike_id}")
def read_item(bike_id: int, q: Union[str, None] = None):
    query = f"SELECT * FROM bike_data JOIN station_data ON bike_data.station_id = station_data.id WHERE bike_id = {bike_id}"
    result = execute_mysql_query(query)
    return {"bike_id": bike_id, "result": result}


@app.get("/get_bike_by_station/{station_id}")
def read_item(station_id: int, q: Union[str, None] = None):
    query = f"SELECT * FROM bike_data JOIN station_data ON bike_data.station_id = station_data.id WHERE station_id = {station_id}"
    result = execute_mysql_query(query)
    return {"station_id": station_id, "result": result}


@app.get("/get_bike_by_id_and_station/{bike_id}/{station_id}")
def read_item(bike_id: int, station_id: int, q: Union[str, None] = None):
    query = f"SELECT * FROM bike_data JOIN station_data ON bike_data.station_id = station_data.id WHERE bike_id = {bike_id} AND station_id = {station_id}"
    result = execute_mysql_query(query)
    return {"bike_id": bike_id, "result": result}


@app.get("/station_by_id/{station_id}")
def read_item(station_id: int, q: Union[str, None] = None):
    query = f"SELECT * FROM station_data WHERE id = {station_id}"
    result = execute_mysql_query(query)
    return {"bike_id": station_id, "result": result}


@app.get("/get_all_stations")
def read_item(q: Union[str, None] = None):
    query = f"SELECT * FROM station_data"
    result = execute_mysql_query(query)
    return {"q": q, "result": result}
