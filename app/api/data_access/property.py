from app.dependencies import get_db


def select_property_by_id(property_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Property WHERE idProperty = %s", (property_id,))

    property_data = cursor.fetchone()

    cursor.close()
    db.commit()

    return property_data


def select_properties():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Property")

    properties_data = cursor.fetchall()

    cursor.close()
    db.commit()

    return properties_data


def insert_property(property_base, pricing_id):
    db = get_db()
    cursor = db.cursor()

    query = ("INSERT INTO Property (idOwner, address, surface, terrace, internet, idPricing)"
             "VALUES (%s, %s, %s, %s, %s, %s)")
    values = (
        property_base.idOwner, property_base.address, property_base.surface, property_base.terrace,
        property_base.internet, pricing_id)

    cursor.execute(query, values)

    property_id = cursor.lastrowid
    cursor.close()
    db.commit()
    return property_id


def update_property_by_id(property_id, key, value):
    db = get_db()
    cursor = db.cursor()

    query = "UPDATE Property SET " + key + " = %s WHERE idProperty = %s"
    values = (value, property_id)
    cursor.execute(query, values)

    cursor.close()
    db.commit()


def del_property_by_id(property_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Property WHERE idProperty = %s", (property_id,))

    cursor.close()
    db.commit()
