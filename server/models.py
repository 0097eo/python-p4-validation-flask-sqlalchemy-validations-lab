from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name cannot be empty')
        author_name = db.session.query(Author.id).filter_by(name=name).first()
        if author_name is not None:
            raise ValueError('Name already exists')
        return name

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number should be 10 digits long')
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def validate_content(self, key, title):
        if not title:
            raise ValueError('Title cannot be empty')
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError('Title must contain at least one of the following keywords: Won\'t Believe, Secret, Top, Guess')
        return title
    

    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category must be either Fiction or Non-Fiction')
        return category
    
    @validates('content', 'summary')
    def validate_length(self, key, string):
        if (key == 'content'):
            if len(string) < 250:
                raise ValueError('Content must be at least 250 characters long')
        if (key == 'summary'):
            if len(string) > 250:
                raise ValueError('Summary cannot be more than 250 characters long')
        return string



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
