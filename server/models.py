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
        names = [author.name for author in Author.query.all()]
        if not name:
            raise ValueError("Author must have a name")
        if name in names:
            raise ValueError("Author must have a unique name")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        digits = list(phone_number)
        if len(digits) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        for digit in digits:
            if digit not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                raise ValueError("Phone number can only contain integers")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

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
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, text):
        if len(text) > 250:
            raise ValueError("Post summary must be less than 250 characters long")
        return text

    @validates('category')
    def validate_category(self, key, category):
        categories = ['Fiction', 'Non-Fiction']
        if category not in categories:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won\'t Believe", "Secret", "Top", "Guess"]
        clickbaity = False
        for item in clickbait:
            if item in title:
                clickbaity = True
        if clickbaity == False:
            raise ValueError('Post title must contain one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
