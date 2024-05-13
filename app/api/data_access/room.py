from app.dependencies import get_db


def insert_room(room, property_id):
    db = get_db()
    cursor = db.cursor()

    room_query = "INSERT INTO Room (idProperty, type, number) VALUES (%s, %s, %s)"
    room_values = (property_id, room.type, room.number)
    cursor.execute(room_query, room_values)

    cursor.close()
    db.commit()


def select_room_by_id(property_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Room WHERE idProperty = %s", (property_id,))
    rooms = cursor.fetchone()

    cursor.close()
    return rooms


def select_room_by_id_by_type(property_id, property_type):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Room WHERE type = %s AND idProperty = %s", (property_type, property_id,))
    rooms = cursor.fetchone()

    cursor.close()
    return rooms


def update_room_by_id_by_type(property_id, value_type, value_number):
    db = get_db()
    cursor = db.cursor()

    query = "UPDATE Room SET number = %s WHERE type = %s AND idProperty = %s"
    values = (value_number, value_type, property_id)
    cursor.execute(query, values)

    cursor.close()
    db.commit()


def del_room_by_id_by_type(property_id, room_type):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Room WHERE type = %s AND idProperty = %s", (room_type, property_id,))

    cursor.close()
    db.commit()


def del_room_by_id(property_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Room WHERE idProperty = %s", (property_id,))

    cursor.close()
    db.commit()
