from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
import datetime
import sqlite3
import sys

from sqlalchemy.orm.mapper import validates

Base = declarative_base()


class Person(Base):
    __tablename__ = 'Persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String, nullable=False)
    loans = relationship('Loan')

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value
        return value


class Book(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    lent = Column(Boolean, default=False)


class Loan(Base):
    __tablename__ = "Loans"
    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer, ForeignKey('Persons.id'))
    book_id = Column(Integer, ForeignKey('Books.id'))
    book = relationship("Book", backref=backref("Books", uselist=False))


def add_person(name, email):
    p = Person()
    p.name = name
    p.email = email
    session.add(p)
    session.commit()


def add_book(author, title, year):
    b = Book()
    b.author = author
    b.title = title
    b.year = year
    session.add(b)
    session.commit()


def lend_book(borrower_id, book_id):
    if session.query(Book).get(book_id).lent:
        print("This book is already lent")
        return
    session.query(Book).get(book_id).lent = True
    l = Loan()
    l.book_id = book_id
    l.borrower_id = borrower_id
    session.add(l)
    session.commit()


def return_book(b_id):
    if not session.query(Book).get(b_id).lent:
        print("This book is not lent")
        return
    session.query(Book).get(b_id).lent = False
    session.query(Loan).filter_by(book_id=b_id).delete()
    session.commit()


engine = create_engine('sqlite:///test.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)

session = Session()
# session.query(Loan).delete()
# session.close()
