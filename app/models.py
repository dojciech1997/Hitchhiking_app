from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    tags = db.relationship('Tag', secondary='person_tag', backref='people')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'

person_tag = db.Table(
    'person_tag',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
