from flask import Blueprint, render_template
from flask import request,session

from models import User, db,Product,Section,Cart
import copy

authU = Blueprint('authU', __name__, template_folder='templates')

@authU.route('/')
def Start():
    return render_template('user/Start.html')

@authU.route('/user')
def Home_Page():
    obj=Section.query.all()
    objP = Product.query.all()
    return render_template('user/User_login.html',obj = obj,objP = objP)


@authU.route('/search',methods=["POST","GET"])
def Search():
    uid = session.get('uid')
    if uid == None:
        return render_template('user/User_login.html')
    s = request.form['section_search']
    if s == 'All':
        obj=Section.query.all()
        objP = Product.query.all()
        return render_template('user/User_dashboard.html',obj = obj,objP = objP)
    obj = Section.query.all()
    objS = Section.query.get(s)
    section = objS.section
    objP = Product.query.filter_by(sectionid = s).all()
    return render_template('user/Section_search.html',obj = obj,objP = objP,section = section,s=s)

@authU.route('/loginpage', methods=["POST"])
def User_Login():
    
    username = request.form['username']
    password = request.form['password']
    objUser = User.query.filter_by(user=username, password=password).first()
    obj=Section.query.all()
    objP = Product.query.all()

    if objUser:
        session['uid'] = objUser.uid
        return render_template('user/User_dashboard.html', k='User Exists',obj=obj, objP=objP)
    else:
        return render_template('user/User_login.html', k='User doesnst exist',obj=obj, objP=objP)


@authU.route('/openregister')
def Open_Reg():
    return render_template('user/User_Register.html')


@authU.route('/registerpage', methods=["POST", "GET"])
def User_Reg():
    uid = session.get('uid')
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    objUser = User.query.filter_by(uid =uid ,user = username,password=password,email=email).first()
    if objUser:
        return render_template('user/User_register.html',k='Please try different credintials')
    user = User(user=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return render_template('user/User_login.html', k='User Created Successfully')


@authU.route('/userdashboard', methods=["GET", "POST"])
def User_dashboard():
    obj=Section.query.all()
    objP = Product.query.all()
    return render_template('user/User_dashboard.html',obj=obj, objP=objP)

@authU.route('/cart/<pid>/<sid>',methods=["POST","GET"])
def Add_Cart(pid,sid):
    user_id = session.get('uid')
    product_id = pid
    objproduct = Product.query.filter_by(pid = product_id).first()
    sect = Section.query.filter_by(sid = sid).first()
    mid = sect.manager_id
    product = objproduct.product
    max_quantity = objproduct.quantity
    price = objproduct.price
    objCart = Cart.query.filter_by(user_id = user_id,product_id = pid).first()
    obj=Section.query.all()
    objP = Product.query.all()

    if objCart:
          session['id'] = objCart.id
          return render_template('user/User_dashboard.html',obj=obj,objP = objP, k='Product in Cart')
    cart = Cart(user_id = user_id,product = product,max_quantity = max_quantity,quantity=0,price = price,product_id = product_id,section_id = sid,manager_id =mid)
    db.session.add(cart)
    db.session.commit()
    return render_template('user/User_dashboard.html',obj=obj,objP = objP, k='Product added to Cart')
@authU.route('/display')
def Cart_display():
    uid = session.get('uid')
    print(uid)
    if uid == None:
        return render_template('user/User_login.html')
    objCart = Cart.query.filter_by(user_id = uid).all()
    obj=Section.query.all()
    objP = Product.query.all()
    objProduct = Product.query.filter_by()
    print(objCart)
    if objCart:
        return render_template('user/Cart.html',objCart = objCart)
    return render_template('user/User_dashboard.html',obj = obj,objP = objP)

@authU.route('/delete/<int:id>',methods=["POST","GET"])
def Cart_delete(id):
    uid = session.get('uid')
    print(uid)
    if uid == None:
        return render_template('user/User_login.html')
    objcart = Cart.query.filter_by(id = id).first()
    objCart = Cart.query.filter_by(user_id = uid).all()
    if objcart:
        db.session.delete(objcart)
        db.session.commit()
        return render_template('user/Cart.html',objCart = objCart)
    return render_template('user/Cart.html',objCart = objCart)

@authU.route('/delete')
def Remove_All():
    uid = session.get('uid')
    print(uid)
    if uid == None:
        return render_template('user/User_login.html')
    objcart = Cart.query.filter_by(user_id = uid).all()
    objCart = Cart.query.filter_by(user_id = uid).all()
    obj=Section.query.all()
    objP = Product.query.all()
    if objcart:
        db.session.delete(objcart)
        db.session.commit()
        return render_template('user/User_dashboard.html',obj = obj,objP = objP)
    return render_template('user/Cart.html',objCart = objCart)

@authU.route('/billing',methods=["POST","GET"])
def Billing():
    uid = session.get('uid')
    print(uid)
    if uid == None:
        return render_template('user/User_login.html')
    
    user = User.query.filter_by(uid =uid).first()
    i=0
    objCart = Cart.query.filter_by(user_id = uid).all()
   
    for item in objCart:
        s = "quantity"+str(i)   
        k = int(request.form[s])     
        objProduct = Product.query.filter_by(pid = item.product_id).first()
        item.quantity = k
        db.session.commit()
        k = objProduct.quantity - item.quantity
        objProduct.quantity = k
        item.max_quantity = objProduct.quantity 
        db.session.commit()
        i+=1

    objCart= Cart.query.filter_by(user_id=uid).all()
   
    if len(objCart)>1 :
        objCart1 = copy.copy(objCart)        
        for o in objCart:
            db.session.delete(o)
        
        db.session.commit()  
        return render_template('user/Thank_you.html',objCart1 = objCart1,user=user)
    else:
        o = Cart.query.filter_by(user_id=uid).first()
        db.session.delete(o)
        db.session.commit()      
        return render_template('user/Thank_you.html',objCart1 = objCart,user=user)


@authU.route('/logout')
def Logout():
    session['uid'] = None
    return render_template('user/Start.html')