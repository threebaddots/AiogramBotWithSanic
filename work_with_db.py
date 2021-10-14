import sqlite3

sqlite_connection = sqlite3.connect('db.sqlite')


async def get_data_from_db(tid):
    cursor = sqlite_connection.cursor()
    result = cursor.execute(f"""SELECT * FROM Geolocations WHERE id = {int(tid)}""").fetchall()
    if result:
        return result[0]
    return None


async def push_data_to_db(tid, location):
    cursor = sqlite_connection.cursor()
    if await get_data_from_db(tid):
        cursor.execute(f"""UPDATE Geolocations 
        SET latitude = {location[0]},
        longitude = {location[1]}
        WHERE id = {tid}""")
    else:
        cursor.execute(f"""INSERT INTO Geolocations VALUES({int(tid)}, {float(location[0])}, {float(location[1])})""")
    sqlite_connection.commit()
    cursor.close()
