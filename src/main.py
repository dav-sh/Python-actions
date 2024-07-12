from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:1234@localhost/book_ms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

'''
                 MODELS
'''

'''
AUTHOR
'''
class Author(db.Model):

    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    book = db.relationship('Book', back_populates = 'author')
    
    def __repr__(self):
        return f'<author {self.name}>'

'''
GENRE
'''
class Genre(db.Model):

    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    book = db.relationship('Book', back_populates = 'genre')
    
    def __repr__(self):
        return f'<genre {self.name}>'



'''
BOOK
'''
class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    author_id = db.Column(db.Integer, ForeignKey("author.id"))
    author = db.relationship('Author', back_populates = 'book')
    genre_id = db.Column(db.Integer, ForeignKey("genre.id"))
    genre = db.relationship('Genre', back_populates = 'book')


    def __repr__(self):
        return f' <id {self.isbn} title {self.title} author {self.author}>'
    



'''
                ENDPOINTS
'''

@app.route("/", methods = ['GET'])
def main():
    return "test",200

'''
AUTHOR
'''

# GET LIST
@app.route("/author", methods = ['GET'])
def getAuthors():
    authors = Author.query.all()
    authors_list=[]
    for au in authors:
        per_data = {
            "id": au.id,
            "name": au.name
        }
        authors_list.append(per_data)
    return jsonify(authors_list),200


#GET BY ID
@app.route("/author/<id>", methods = ['GET'])
def getAuthorById(id):

    author = Author.query.get(id)
    if author != None:
        per_data = {
            "id": author.id,
            "name": author.name
        }
        return jsonify(per_data),200
    return jsonify({"error": "Author not found"}),404


# CREATE
@app.route('/author', methods = ['POST'])
def createAuthor():
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({"error": "Name field is required"}), 400

    name = data["name"]
    person = Author(name=name)

    db.session.add(person)
    db.session.commit()
    return jsonify({"message": "Author created successfully"}),201



# DELETE BY ID
@app.route("/author/<id>", methods = ['DELETE'])
def deleteAuthorById(id):
    author = Author.query.get(id)
    if author:
            db.session.delete(author)
            db.session.commit()
            return jsonify({"message": "Author deleted successfully"}), 200
    else:
        return jsonify({"error": "author not found"}), 404


# UPDATE
@app.route("/author/<id>", methods=['PUT'])
def updateAuthorById(id):
    data = request.get_json()
    author = Author.query.get(id)

    if author:
        if 'name' not in data:
            return jsonify({"error": "Name field is required"}), 422
        else:
            author.name = data['name']
            return jsonify({"message": "Author updated successfully"}),200
    else:
        return jsonify({"error": "Author not found"}), 404

'''
BOOK
'''
# GET
@app.route('/book', methods=['GET'])
def getBook():
    books = Book.query.all()
    books_list = []
    for book in books:
        book_data = {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author.name
        }
        books_list.append(book_data)
    return jsonify(books_list), 200


# GET BY ID
@app.route('/book/<id>', methods=['GET'])
def getBookByID(id):
    # isbn = id
    # book = Book.query(Book).filter(Book.isbn == id).first()
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book_data = []
    print(book)
    
    data = {
        "isbn": book.isbn,
        "title": book.title,
        "price": book.price,
        "quantity" : book.quantity,
        "author":{
            "id": book.author.id,
            "name": book.author.name
        },
        # "author_id": book.author.id,
        # "author_name" : book.author.name, 
        "genre":{
            "id": book.genre.id,
            "name": book.genre.name
        }

    }
    
    book_data.append(data)
    return jsonify(book_data), 200

# INSERT
@app.route('/book', methods=['POST'])
def insertBook():
    data = request.get_json()

    if 'title' not in data or 'author' not in data or 'price' not in data or 'genre' not in data:
        return jsonify({"error": "Lack of information"}), 422
    
    # Data to Book Object
    title = data["title"]
    price = data["price"]
    quantity = data["quantity"]
    author = data["author"]["id"]
    genre = data["genre"]["id"]
    book = Book(title = title, price = price, quantity = quantity, author_id = author, genre_id = genre)

    # Save in db
    db.session.add(book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully'}), 201


# UPDATE BY ID  
@app.route('/book/<id>', methods = ['PUT'])
def updateBookById(id):
    data = request.get_json() # dictionary -> Json
    book = Book.query.filter(Book.isbn == id).first() #Book model -> python object
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    # Data to Book Object
    print(book)
    book.title = data["title"]
    book.price = data["price"]
    book.quantity = data["quantity"]
    book.author_id = data["author"]["id"]
    book.genre_id = data["genre"]["id"]


    # book = Book(title = title, price = price, quantity = quantity, author = author_id, genre = genre_id)
    
    # Save in db
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

# DELETE
@app.route('/book/<id>', methods = ['DELETE'])
def deleteBookById(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Book.query.where(Book.isbn == id).delete()
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': f'Book {book.isbn} deleted successfully'}), 200



'''
GENRE
'''
# GET LIST
@app.route('/genre', methods=['GET'])
def getGenre():
    data = Genre.query.all()
    print(data)
    genres_data = []
    for d in data:
        tmp = {
            "id": d.id,
            "name": d.name
        }
        genres_data.append(tmp)
    return jsonify(genres_data),200

# GET BY ID
@app.route('/genre/<id>', methods=['GET'])
def getGenreByID(id):
    genre = Genre.query.get(id)

    if not genre:
        jsonify({'error': 'Genre not found'}), 404
    data = {
        "id": genre.id,
        "name": genre.name
    }
    return jsonify(data),200

# CREATE
@app.route('/genre', methods=['POST'])
def insertGenre():
    data = request.get_json()
    if not 'name' in data:
        return jsonify({'error': 'Name field is required'}), 422
    name = data['name']
    genre = Genre(name=name)
    db.session.add(genre)
    db.session.commit()
    return jsonify({'message': 'Genre added successfully'}),201


# UPDATE BY ID
@app.route('/genre/<id>', methods=['PUT'])
def updateGenreById(id):
    data = request.get_json()
    genre = Genre.query.get(id)
    if not genre:
        return jsonify({'error': 'Genre not found'}), 404
    if not 'name' in data:
        return jsonify({'error': 'Name field is required'}), 422
    genre.name = data['name']
    if genre.name == "":
        return jsonify({'error': 'Name cannot be empty'}), 422

    db.session.add(genre)
    db.session.commit()
    return jsonify({'message': 'Genre updated successfully'}), 200


# DELETE
@app.route('/genre/<id>', methods=['DELETE'])
def deleteGenreById(id):
    genre = Genre.query.get(id)
    if not genre:
        return jsonify({'error': 'Genre not found'}), 404
    
    db.session.delete(genre)
    db.session.commit()
    return jsonify({'message': 'Genre deleted successfully'})



'''
        MAIN
'''

if __name__ == "__main__":
    app.run()