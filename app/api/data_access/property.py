from app.dependencies import get_db


def select_property(property_id):
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
