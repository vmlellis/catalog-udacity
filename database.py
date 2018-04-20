from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem


#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


def getAllCategories():
    return session.query(Category).all()


def findCategory(**args):
    query = session.query(Category)
    if args is not None:
        query = query.filter_by(**args)
    return query.one()


def createCategory(**args):
    newCategory = Category(name=args['name'], user_id=args['user_id'])
    session.add(newCategory)
    session.commit()


def updateCategory(category, opts):
    if opts['name']:
        category.name = opts['name']
    session.add(category)
    session.commit()


def deleteCategory(category):
    session.delete(category)
    session.commit()


def getAllItems(**args):
    query = session.query(CategoryItem).order_by(CategoryItem.id.desc())
    if args is not None:
        for key, value in args.iteritems():
            if key == 'limit':
                query = query.limit(value)
            if key == 'category_id':
                query = query.filter_by(category_id=value)
    return query.all()


def findItem(**args):
    query = session.query(CategoryItem)
    if args is not None:
        query = query.filter_by(**args)
    return query.one()


def createItem(**args):
    newItem = CategoryItem(
        title=args['title'],
        description=args['description'],
        category_id=int(args['category_id']),
        user_id=int(args['user_id']))
    session.add(newItem)
    session.commit()


def updateItem(item, opts):
    if opts['title']:
        item.title = opts['title']
    if opts['description']:
        item.description = opts['description']
    if opts['category']:
        item.category_id = int(opts['category'])
    session.add(item)
    session.commit()


def deleteItem(item):
    session.delete(item)
    session.commit()


def findUser(**args):
    query = session.query(User)
    if args is not None:
        query = query.filter_by(args)
    return query.one()


def createUser(opts):
    newUser = User(
        name=opts['username'],
        email=opts['email'],
        picture=opts['picture'])
    session.add(newUser)
    session.commit()
    user = findUser(email=opts['email'])
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
