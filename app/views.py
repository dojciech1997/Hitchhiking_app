from flask import render_template, request, redirect, url_for
#from app import app, db
from db_file import db
from __init__ import app
#from app.models import Person, Tag
from models import Person, Tag
#from app.forms import TagForm
import logging

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['name']
    photo_url = request.form['photo_url']
    description = request.form['description']
    new_person = Person(name=name, photo_url=photo_url, description=description)
    tags = request.form.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        for tag_name in tags_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            new_person.tags.append(tag)
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_person/<int:person_id>', methods=['POST', 'DELETE'])
def delete_person(person_id):
    person = Person.query.get(person_id)
    if person:
        db.session.delete(person)
        db.session.commit()
    return redirect(url_for('library'))

@app.route('/edit_person_from_library/<int:person_id>', methods=['POST'])
def edit_person_from_library(person_id):
    person = Person.query.get_or_404(person_id)

    # Aktualizuj dane na podstawie formularza
    person.name = request.form['name']
    person.photo_url = request.form['photo_url']
    person.description = request.form['description']
    tags = request.form.get('tags')
    if tags:
        tags_list = [tag.strip() for tag in tags.split(',')]
        person.tags = []
        for tag_name in tags_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            person.tags.append(tag)
    db.session.commit()
    logging.debug(f'Updated person tags: {person.tags}')
    return redirect(url_for('library'))

@app.route('/search_person', methods=['POST'])
def search_person():
    search_id = request.form.get('search_id')
    search_name = request.form.get('search_name')
    search_tags = request.form.get('search_tags')

    people = []

    # if search_id:
    #     person = Person.query.get(search_id)
    #     if person:
    #         people.append(person)
    #         # return render_template('index.html', people=[person])
    if search_name:
        people.extend(Person.query.filter(Person.name.like(f"%{search_name}%")).all())
    if search_tags:
        tags_list = [tag.strip() for tag in search_tags.split(',')]
        for tag_name in tags_list:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag:
                people.extend(tag.people)
    # # Dodaj standardowe rekordy do listy
    # people.extend(Person.query.all())

    return render_template('index.html', people=people)


@app.route('/library')
def library():
    people = Person.query.all()
    return render_template('library.html', people=people)
