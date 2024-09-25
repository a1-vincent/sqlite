import random
from faker import Faker
from flask import Flask, jsonify, request
import sqlite3


# object af Faker
app = Flask(__name__)
fake = Faker() # https://faker.readthedocs.io/en/stable/

# Funktion der returnerer en random dictionary med en user
def create_random_user():
    return {
        "id": random.randint(1, 1000),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
        "gender": random.choice(["Male", "Female"]),
        "email": fake.email(),
        "phonenumber": fake.phone_number(),
        "address": fake.address(),
        "nationality": fake.country(),
        "active": random.choice([True, False]),
        "github_username": fake.user_name()
    }

# List comprehension der genererer en liste med 10 random_user dictionaries
random_users = [create_random_user() for _ in range(10)]


def init_db():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS members (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              first_name TEXT,
              last_name TEXT,
              birth_date TEXT,
              gender TEXT,
              email TEXT,
              phonenumber TEXT,
              address TEXT,
              nationality TEXT,
              active BOOLEAN,
              github_username TEXT
              )
        """)

    conn.commit()
    conn.close()


def insert_users_into_db(users):
    conn = sqlite3.connect('members.db')
    c = conn.cursor()

    c.executemany("""INSERT INTO members 
                  (first_name, 
                  last_name, 
                  birth_date, 
                  gender, 
                  email, 
                  phonenumber, 
                  address, 
                  nationality, 
                  active, 
                  github_username) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   [(
                       user['first_name'], 
                       user['last_name'], 
                       user['birth_date'], 
                       user['gender'], 
                       user['email'], 
                       user['phonenumber'], 
                       user['address'], 
                       user['nationality'], 
                       user['active'], 
                       user['github_username']) for user in users])

    conn.close()

init_db()
insert_users_into_db(random_users)

@app.route('/api/members', methods=['GET'])
def get_members():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute('SELECT * FROM members')

    members = c.fetchall()
    members_list = []
    for row in members:
        members_list.append({
            'id': row[0],
            'first_name': row[1], 
            'last_name': row[2], 
            'birth_date': row[3], 
            'gender': row[4], 
            'email': row[5], 
            'phonenumber': row[6], 
            'address': row[7], 
            'nationality': row[8], 
            'active': row[9], 
            'github_username': row[10] 
        })

    conn.close()
    return jsonify(members_list), 200


@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute('SELECT * FROM members WHERE id = ?', (member_id,))

    member = c.fetchone()
    conn.close()

    if member is None:
        return jsonify({"error": "Member not found"}), 404
    
    member_data = {
         'id': member[0],
            'first_name': member[1], 
            'last_name': member[2], 
            'birth_date': member[3], 
            'gender': member[4], 
            'email': member[5], 
            'phonenumber': member[6], 
            'address': member[7], 
            'nationality': member[8], 
            'active': member[9], 
            'github_username': member[10]
    }

    return jsonify(member_data),200


if __name__ == '__main__':
    app.run(debug=True)