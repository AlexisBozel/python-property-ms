from app.dependencies import get_db
import datetime


def select_advert(advert_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Advert WHERE idAdvert= %s", (advert_id,))
    advert = cursor.fetchone()

    cursor.close()
    return advert


def select_advert_with_filter(partial_query):
    db = get_db()
    cursor = db.cursor()
    query = (("SELECT DISTINCT Property.* FROM Advert, Property, Pricing, Room WHERE Advert.idProperty = "
              "Property.idProperty"
              " AND Property.idPricing = Pricing.idPricing AND Room.idProperty = Property.idProperty AND ")
             + partial_query)
    print(query)
    cursor.execute(query)
    properties_data = cursor.fetchall()
    cursor.close()
    db.commit()
    return properties_data


def select_adverts_by_property_owner(owner_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Advert a, Property p WHERE a.idProperty = p.idProperty "
                   "AND idOwner = %s", (owner_id,))

    advert_data = cursor.fetchall()

    cursor.close()
    db.commit()

    return advert_data


def select_adverts():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Advert")

    advert_data = cursor.fetchall()

    cursor.close()
    db.commit()

    return advert_data


def insert_advert(advert):
    db = get_db()
    cursor = db.cursor()

    date = get_date_now()

    advert_query = ("INSERT INTO Advert (idProperty, title, description, dtCreation, dtModification, dtAvailability) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
    advert_values = (advert.idProperty, advert.title, advert.description, date, date, advert.dtAvailability)
    cursor.execute(advert_query, advert_values)
    advert_id = int(cursor.lastrowid)

    cursor.close()
    db.commit()
    return advert_id


def update_advert(advert_id, key, value):
    db = get_db()
    cursor = db.cursor()
    date = get_date_now()

    query = "UPDATE Advert SET " + key + " = %s, dtModification = %s WHERE idAdvert = %s"
    values = (value, date, advert_id)
    cursor.execute(query, values)

    cursor.close()
    db.commit()


def delete_advert(advert_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Advert WHERE idAdvert = %s", (advert_id,))

    cursor.close()
    db.commit()


def get_date_now():
    date = datetime.datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')
