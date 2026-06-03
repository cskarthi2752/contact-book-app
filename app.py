from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "contacts.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    rows = c.fetchall()
    conn.close()

    contacts = []
    for row in rows:
        contacts.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3]
        })

    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "INSERT INTO contacts (name,email,phone) VALUES (?,?,?)",
        (data["name"], data["email"], data["phone"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Contact added"}), 201

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        """
        UPDATE contacts
        SET name=?, email=?, phone=?
        WHERE id=?
        """,
        (data["name"], data["email"], data["phone"], id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Contact updated"})

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("DELETE FROM contacts WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Contact deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
