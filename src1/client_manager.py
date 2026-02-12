from database import get_connection

def load_clients(tree):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Id, FullName, Phone, Email FROM Clients")
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def add_client(fullname, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Clients (FullName, Phone, Email) VALUES (?, ?, ?)",
        (fullname, phone, email)
    )
    conn.commit()
    conn.close()

def update_client(client_id, fullname, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Clients SET FullName=?, Phone=?, Email=? WHERE Id=?",
        (fullname, phone, email, client_id)
    )
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clients WHERE Id=?", (client_id,))
    conn.commit()
    conn.close()
