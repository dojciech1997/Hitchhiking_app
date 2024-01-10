from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Person, Tag
import psycopg2
#from app.forms import TagForm
import logging

def get_db_connection():
    return psycopg2.connect(
        host='database',
        user='wojtek',
        password='password',
        database='devops_db',
        port=5432
    )

def get_tags_for_person(person_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT tag.name
                FROM tag
                JOIN person_tag ON tag.id = person_tag.tag_id
                WHERE person_tag.person_id = %s AND tag.name IS NOT NULL
            """, (person_id,))
            tags_data = cursor.fetchall()

    tags = [tag_data[0] for tag_data in tags_data]
    return tags

@app.route('/')
def index():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM person")
            people_data = cursor.fetchall()
    people = []
    for person_data in people_data:
        person = {
            'id': person_data[0],
            'name': person_data[1],
            'photo_url': person_data[2],
            'latitude': person_data[3],
            'longitude': person_data[4],
            'description': person_data[5],
            'tags': get_tags_for_person(person_data[0]),
        }
        people.append(person)
    return render_template('index.html')

@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['name']
    photo_url = request.form['photo_url']
    description = request.form['description']
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO person (name, photo_url, description) VALUES (%s, %s, %s) RETURNING id", (name, photo_url, description))
            new_person_id = cursor.fetchone()[0]
    tags = request.form.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        for tag_name in tags_list:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO tag (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = %s RETURNING id", (tag_name, tag_name))
                    tag_id = cursor.fetchone()[0]
                    # tag_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # if tag_id:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO person_tag (person_id, tag_id) VALUES (%s, %s)", (new_person_id, tag_id))

    # new_person = Person(name=name, photo_url=photo_url, description=description)
    # tags = request.form.get('tags')
    # if tags:
    #     tags_list = [tag.strip() for tag in tags.split(',')]
    #     for tag_name in tags_list:
    #         tag = Tag.query.filter_by(name=tag_name).first()
    #         if not tag:
    #             tag = Tag(name=tag_name)
    #             db.session.add(tag)
    #             db.session.commit()
    #         new_person.tags.append(tag)
    # db.session.add(new_person)
    # db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_person/<int:person_id>', methods=['POST', 'DELETE'])
def delete_person(person_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM person_tag WHERE person_id = %s", (person_id,))
            cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
    # person = Person.query.get(person_id)
    # if person:
    #     db.session.delete(person)
    #     db.session.commit()
    return redirect(url_for('library'))

@app.route('/edit_person_from_library/<int:person_id>', methods=['POST'])
def edit_person_from_library(person_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM person WHERE id = %s", (person_id,))
            person_data = cursor.fetchone()
    if person_data:
        name = request.form['name']
        photo_url = request.form['photo_url']
        description = request.form['description']

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE person SET name = %s, photo_url = %s, description = %s WHERE id = %s", (name, photo_url, description, person_id))

        tags = request.form.get('tags')
        if tags:
            tags_list = [tag.strip() for tag in tags.split(',')]
            for tag_name in tags_list:
                with get_db_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("INSERT INTO tag (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = %s RETURNING id", (tag_name, tag_name))
                        tag_id = cursor.fetchone()[0]
                        # tag_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

                # if tag_id:
                with get_db_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("INSERT INTO person_tag (person_id, tag_id) VALUES (%s, %s)", (person_id, tag_id))

    #logging.debug(f'Updated person tags: {tags}')


    # person = Person.query.get_or_404(person_id)
    #
    # person.name = request.form['name']
    # person.photo_url = request.form['photo_url']
    # person.description = request.form['description']
    # tags = request.form.get('tags')
    # if tags:
    #     tags_list = [tag.strip() for tag in tags.split(',')]
    #     person.tags = []
    #     for tag_name in tags_list:
    #         tag = Tag.query.filter_by(name=tag_name).first()
    #         if not tag:
    #             tag = Tag(name=tag_name)
    #             db.session.add(tag)
    #             db.session.commit()
    #         person.tags.append(tag)
    # db.session.commit()
    # logging.debug(f'Updated person tags: {person.tags}')
    return redirect(url_for('library'))

@app.route('/search_person', methods=['POST'])
def search_person():
    search_id = request.form.get('search_id')
    search_name = request.form.get('search_name')
    search_tags = request.form.get('search_tags')

    people = []
    if search_name:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM person WHERE name ILIKE %s", (f"%{search_name}%",))
                people_data = cursor.fetchall()

        for person_data in people_data:
            person = {
                'id': person_data[0],
                'name': person_data[1],
                'photo_url': person_data[2],
                'latitude': person_data[3],
                'longitude': person_data[4],
                'description': person_data[5],
                'tags': get_tags_for_person(person_data[0]),
            }
            people.append(person)
    if search_tags:
        tags_list = [tag.strip() for tag in search_tags.split(',')]
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT person.*
                FROM person
                JOIN person_tag ON person.id = person_tag.person_id
                JOIN tag ON person_tag.tag_id = tag.id
                WHERE tag.name IN %s
                """
                cursor.execute(query, (tuple(tags_list),))
                people_data = cursor.fetchall()
    # if search_tags:
    #     tags_list = [tag.strip() for tag in search_tags.split(',')]
    #     for tag_name in tags_list:
    #         with get_db_connection() as conn:
    #             with conn.cursor() as cursor:
    #                 cursor.execute("SELECT person.* FROM person JOIN person_tag ON person.id = person_tag.person_id "
    #                                "JOIN tag ON person_tag.tag_id = tag.id WHERE tag.name ILIKE %s",
    #                                (f"%{tag_name}%",))
    #                 people_data = cursor.fetchall()

        for person_data in people_data:
            person = {
                'id': person_data[0],
                'name': person_data[1],
                'photo_url': person_data[2],
                'latitude': person_data[3],
                'longitude': person_data[4],
                'description': person_data[5],
                'tags': get_tags_for_person(person_data[0]),
            }
            people.append(person)
    # # if search_id:
    # #     person = Person.query.get(search_id)
    # #     if person:
    # #         people.append(person)
    # #         # return render_template('index.html', people=[person])
    # if search_name:
    #     people.extend(Person.query.filter(Person.name.like(f"%{search_name}%")).all())
    # if search_tags:
    #     tags_list = [tag.strip() for tag in search_tags.split(',')]
    #     for tag_name in tags_list:
    #         tag = Tag.query.filter_by(name=tag_name).first()
    #         if tag:
    #             people.extend(tag.people)
    # # people.extend(Person.query.all())

    return render_template('index.html', people=people)


@app.route('/library')
def library():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM person")
            people_data = cursor.fetchall()

    people = []
    for person_data in people_data:
        person = {
            'id': person_data[0],
            'name': person_data[1],
            'photo_url': person_data[2],
            'latitude': person_data[3],
            'longitude': person_data[4],
            'description': person_data[5],
            'tags': get_tags_for_person(person_data[0]),
        }
        people.append(person)
    # people = Person.query.all()
    return render_template('library.html', people=people)
