from flask import Blueprint, render_template
from flask import request, session

from models import User, db, Manager, Section,Product,Cart

authM = Blueprint('authM', __name__, template_folder='templates')


@authM.route('/manager')
def Home_Page():
    return render_template('manager/Manager_login.html')


@authM.route('/loginmanager', methods=["POST"])
def Manager_Login():
   
    password = request.form['password']
    email = request.form['email']
    objManager = Manager.query.filter_by(password=password, email=email).first()
    mid = session.get('mid')
    obj = Section.query.filter_by(manager_id=mid).all()

    if objManager:
        session['mid'] = objManager.mid
        return render_template('manager/Manager_dashboard.html',objSection = obj)
    else:
        return render_template('manager/Manager_login.html', k='Manager doesnt exist')


@authM.route('/createsection', methods=["POST", "GET"])
def Create_S():
    mid = session.get('mid')
    obj = Section.query.filter_by(manager_id=mid).all()
    
    return render_template('manager/Manager_dashboard.html',objSection = obj)

@authM.route('/create',methods=["POST","GET"])
def Create_Section():
    section = request.form['section']
    
    manager_id = session.get('mid')
    
    # obj = Section.query.get(manager_id)
    obj=Section.query.filter_by(manager_id=manager_id).all()
    objSection = Section.query.filter_by(section = section, manager_id=manager_id).first()
    
    #print(objSection)
    if objSection:
        session['sid'] = objSection.sid
        sid = session.get('sid')
        objP = Product.query.filter_by(manager_id = manager_id).all()
        return render_template('manager/Manager_product.html', k='Section Exists',obj=obj,objP = objP,l='No products were added')
    
    section = Section(section=section, manager_id=manager_id)
    db.session.add(section)
    db.session.commit()
    obj = Section.query.filter_by(manager_id = manager_id).all()
    objP = Product.query.filter_by(manager_id = manager_id).all()
    return render_template('manager/Manager_product.html', k='Section Created',obj=obj,objP = objP,l='No products were added')

@authM.route('/deletesection/<int:sid>',methods=["POST","GET"])
def Delete_Section(sid):
    print(sid)
    manager_id = session.get('mid')
    objSection = Section.query.get(sid)
    objProduct = Product.query.filter_by(sectionid = sid,manager_id = manager_id).all()
    objP = Product.query.filter_by(manager_id = manager_id).all()
    objCart = Cart.query.filter_by(product_id = 2).first()
    print(objProduct)
    if objSection:
        if objProduct:
            db.session.delete(objProduct)
            db.session.commit()
        db.session.delete(objSection)
        db.session.commit()
        obj=Section.query.filter_by(manager_id=manager_id).all()

        return render_template('manager/Manager_product.html', k='Section Exists',obj=obj,objP = objP,l='No products were added')
    obj=Section.query.filter_by(manager_id=manager_id).all()
    return render_template('manager/Manager_product.html', k='Section Exists',obj=obj,objP = objP,l='No products were added')


@authM.route('/editsection/<int:sid>',methods=["POST","GET"])
def Edit_Section(sid):
    manager_id = session.get('mid')
    objP = Product.query.filter_by(manager_id = manager_id).all()
    obj=Section.query.filter_by(manager_id=manager_id).all()
    objSection = Section.query.get(sid)
    if objSection:
        return render_template('manager/Section_edit.html',objSection=objSection)
    return render_template('manager/Manager_product.html', k='Section Exists',obj=obj,objP = objP,l='No products were added')

@authM.route('/edit/<int:sid>',methods=["POST","GET"])
def Edit(sid):
    manager_id =session.get('mid')
    objP = Product.query.filter_by(manager_id = manager_id).all()
    objSection = Section.query.get(sid)
    section = request.form['categoryName']
    objSection.section = section
    obj=Section.query.filter_by(manager_id=manager_id).all()
    db.session.commit()
    return render_template('manager/Manager_product.html', k='Section Exists',obj=obj,objP = objP,l='No products were added')


#Product Controller
@authM.route('/createproduct/<int:sid>')
def Create_Product(sid):
    obj = Section.query.get(sid)
    manager_id = session.get('mid')
    return render_template('manager/Create_product.html',obj = obj)

@authM.route('/createp/<int:sid>',methods=["POST","GET"])
def Create(sid):
    manager_id = session.get('mid')
    product = request.form['name']
    unit = request.form['unit']
    price = request.form['price']
    quantity = request.form['quantity']

    objP = Product.query.filter_by(manager_id = manager_id).all()
    obj = Section.query.filter_by(manager_id = manager_id).all()
    objProduct = Product.query.filter_by(product = product, unit = unit, price = price, quantity = quantity,sectionid=sid).first()
    if objProduct:
        objP = Product.query.filter_by(manager_id = manager_id).all()
        return render_template('manager/Manager_product.html',obj = obj,objP = objP,l='No products added',k='product exists')
    prod = Product(product = product,unit =unit,price = price,quantity = quantity,sectionid =sid,manager_id = manager_id)
    db.session.add(prod)
    db.session.commit()
    
    objP = Product.query.filter_by(manager_id = manager_id).all()
    obj = Section.query.filter_by(manager_id = manager_id).all()

    return render_template('manager/Manager_product.html',obj=obj,objP = objP,l='No products added')

@authM.route('/deleteproduct/<int:pid>',methods=["POST","GET"])
def Delete(pid):
    
    manager_id = session.get('mid')
    sid = session.get('sid')
    objProduct = Product.query.get(pid)
    objP = Product.query.filter_by(manager_id = manager_id).all()
    obj=Section.query.filter_by(manager_id=manager_id).all()
    objCart = Cart.query.filter_by(product_id = pid).first()

    if objProduct:
        if objCart:
            db.session.delete(objCart)
            db.session.delete(objProduct)
            db.session.commit()
        db.session.delete(objProduct)
        db.session.commit()
        objP = Product.query.filter_by(manager_id = manager_id).all()
        return render_template('manager/Manager_product.html',objP = objP,obj=obj,l='No products addedd',k='Deleted successfully')
    return render_template('manager/Manager_product.html',objP = objP,obj=obj,l='No products addedd',k='Doesnt exist')

@authM.route('/editproduct/<int:pid>')
def Edit_Prod(pid):
    print("edit pid:",pid)
    try:
        objProduct = Product.query.filter_by(pid = pid).first()
    except Exception as e:
        print("There was an error: ", e)

    print(objProduct)
    return render_template("manager/Edit_products.html",objProduct=objProduct)
   

@authM.route('/editp/<int:pid>',methods=["POST","GET"])
def Edited(pid):
    manager_id = session.get('mid')
    product = request.form['name']
    unit = request.form['unit']
    price = request.form['price']
    quantity = request.form['quantity']

    objProduct = Product.query.filter_by(pid = pid).first()
    objProduct.product = product 
    objProduct.unit = unit  
    objProduct.price = price
    objProduct.quantity = quantity

    db.session.commit()

    objP = Product.query.filter_by(manager_id = manager_id).all()
    obj = Section.query.filter_by(manager_id = manager_id).all() 

    return render_template('manager/Manager_product.html',objP = objP,obj=obj,l='No products addedd',k='Edited successfully')

@authM.route('/logout')
def Logout():
    session['mid'] = None
    return render_template('user/Start.html')