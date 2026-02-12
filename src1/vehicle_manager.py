from database import get_connection

def load_vehicles(tree):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.Id, c.FullName, v.Brand, v.Model, v.VIN, v.LicensePlate, v.Year, v.Mileage
        FROM Vehicles v
        JOIN Clients c ON v.ClientId = c.Id
    """)
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def add_vehicle(client_id, brand, model, vin, plate, year, mileage):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Vehicles (ClientId, Brand, Model, VIN, LicensePlate, Year, Mileage)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (client_id, brand, model, vin, plate, year, mileage))
    conn.commit()
    conn.close()

def update_vehicle(vehicle_id, client_id, brand, model, vin, plate, year, mileage):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Vehicles SET ClientId=?, Brand=?, Model=?, VIN=?, LicensePlate=?, Year=?, Mileage=?
        WHERE Id=?
    """, (client_id, brand, model, vin, plate, year, mileage, vehicle_id))
    conn.commit()
    conn.close()

def delete_vehicle(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Vehicles WHERE Id=?", (vehicle_id,))
    conn.commit()
    conn.close()
