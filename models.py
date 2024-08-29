from flask_sqlalchemy import SQLAlchemy as sa

db = sa()


# USER CLASS
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=True)


# ADMIN CLASS
class Admin(db.Model):
    __tablename__ = 'admin'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    managers = db.relationship('Manager', backref='admin')


# STORE MANAGER CLASS
class Manager(db.Model):
    __tablename__ = 'manager'
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.aid'), nullable=False)
    sections = db.relationship('Section', backref='manager')
    products = db.relationship('Product', backref='manager')
    cart_manager =  db.relationship('Cart', backref='manager')


# SECTION/CATEGORY CLASS
class Section(db.Model):
    __tablename__ = 'section'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    section = db.Column(db.String, unique=True, nullable=False)
    products = db.relationship('Product', backref='section')
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.mid'), nullable=False)
    cart_section =  db.relationship('Cart', backref='section')

# PRODUCT CLASS
class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.String, nullable=False)
    unit    = db.Column(db.String,nullable=False)
    price   = db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    sectionid = db.Column(db.Integer, db.ForeignKey('section.sid'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.mid'), nullable=False)    
    cart_products = db.relationship('Cart', backref='product_1',lazy=True)

#CART CLASS 
class Cart(db.Model):
    __tablename__= 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    max_quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    section_id = db.Column(db.Integer,  db.ForeignKey('section.sid'),nullable=False)
    product_id = db.Column(db.Integer,  db.ForeignKey('product.pid'),nullable=False)
    manager_id = db.Column(db.Integer,  db.ForeignKey('manager.mid'),nullable=False)

    