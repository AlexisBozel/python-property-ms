from app.dependencies import get_db


def insert_pricing(pricing):
    db = get_db()
    cursor = db.cursor()

    pricing_query = "INSERT INTO Pricing (charge, price) VALUES (%s, %s)"
    pricing_values = (pricing.charge, pricing.price)
    cursor.execute(pricing_query, pricing_values)
    pricing_id = int(cursor.lastrowid)

    cursor.close()
    db.commit()
    return pricing_id


def select_pricing(id_pricing):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Pricing WHERE idPricing = %s", (id_pricing,))
    pricing = cursor.fetchone()

    cursor.close()
    return pricing


def update_pricing(pricing_id, key, value):
    db = get_db()
    cursor = db.cursor()

    query = "UPDATE Pricing SET " + key + " = %s WHERE idPricing = %s"
    values = (value, pricing_id)
    cursor.execute(query, values)

    cursor.close()
    db.commit()


def delete_pricing(pricing_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Pricing WHERE idPricing = %s", (pricing_id,))

    cursor.close()
    db.commit()
