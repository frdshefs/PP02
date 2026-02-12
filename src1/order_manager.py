from database import get_connection

def load_orders(tree):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.Id, o.OrderNumber, c.FullName, v.Brand + ' ' + v.Model,
               o.ReceiveDate, o.Status, o.TotalCost
        FROM Orders o
        JOIN Clients c ON o.ClientId = c.Id
        JOIN Vehicles v ON o.VehicleId = v.Id
    """)
    for item in tree.get_children():
        tree.delete(item)
    for row in cursor.fetchall():
        tree.insert("", "end", values=[row.Id, row.OrderNumber, row.FullName, row[3], row.ReceiveDate, row.Status, row.TotalCost])
    conn.close()

def update_status(order_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Orders SET Status=? WHERE Id=?", (status, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Orders WHERE Id=?", (order_id,))
    conn.commit()
    conn.close()

def update_order(order_id, order_number, client_id, vehicle_id, receive_date, status, total_cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Orders
        SET OrderNumber=?, ClientId=?, VehicleId=?, ReceiveDate=?, Status=?, TotalCost=?
        WHERE Id=?
    """, (order_number, client_id, vehicle_id, receive_date, status, total_cost, order_id))
    conn.commit()
    conn.close()
