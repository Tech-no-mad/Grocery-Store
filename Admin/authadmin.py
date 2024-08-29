from flask import Blueprint, render_template
from flask import request
from flask import session

from models import Admin, db, Manager, User,Section,Product

authA = Blueprint('authA', __name__, template_folder='templates')


@authA.route('/admin')
def Home_Page():
    return render_template('admin/Admin_login.html')


@authA.route('/adminlogin', methods=['POST'])
def Admin_Login():
    adminname = request.form['adminname']
    password = request.form['password']
    email = request.form['email']
    check = request.form['check']
    # objAdmin=Admin.query.filter_by(name = adminname,password = password,email=email).first()
    objAdmin = Admin.query.filter_by(name=adminname, password=password, email=email).first()
    if objAdmin:
        session['aid'] = objAdmin.aid
        if check == ('Manager' or 'manager'):
            return render_template('admin/Admin_Dashboard.html')
        return render_template('admin/Admin_user.html')
    else:
        return render_template('admin/Admin_login.html')


@authA.route('/createmanager', methods=["POST", "GET"])
def Create_Manager():
    if session['aid'] is None:
        return render_template('user/User_login.html')

    return render_template('admin/create_manager.html')


@authA.route('/created', methods=["POST", "GET"])
def Created():
    manager = request.form['manager']
    password = request.form['password']
    email = request.form['email']
    admin_id = session.get('aid')
    objManager = Manager.query.filter_by(manager=manager, password=password, email=email, admin_id=admin_id).first()

    if objManager:
        return render_template('admin/Admin_Dashboard.html', k='Manager Exists')
    else:
        manager = Manager(manager=manager, password=password, email=email, admin_id=admin_id)
        db.session.add(manager)
        db.session.commit()
        return render_template('admin/Admin_Dashboard.html', k='Manager Created')


@authA.route('/editmanager', methods=["POST", "GET"])
def Edit_Manager():
    if session['aid'] is None:
        return render_template('user/User_login.html')
    objManager = Manager.query.with_entities(Manager.mid, Manager.manager, Manager.password,Manager.email).all()
    return render_template('admin/edit_manager.html', objManager=objManager)


@authA.route('/editedid', methods=["POST", "GET"])
def Edit_by_Id():
    if session['aid'] is None:
        return render_template('user/User_login.html')
    mid = request.form['edited_manager']
    objManager = Manager.query.get(mid)

    return render_template('admin/edit_manager_id.html', objManager=objManager)


@authA.route('/edited/<int:mid>', methods=["POST", "GET"])
def Edited(mid):
    manager = request.form['manager']
    password = request.form['password']
    email = request.form['email']
    print('manager', manager, 'email', email)
    objManager = Manager.query.get_or_404(mid)
    print(objManager)
    objManager.manager = manager
    objManager.password = password
    objManager.email = email
    db.session.commit()

    return render_template('admin/Admin_Dashboard.html', k='Manager Edited')


@authA.route('/deletemanager', methods=["POST", "GET"])
def Delete_Manager():
    if session['aid'] is None:
        return render_template('user/User_login.html')
    objManager = Manager.query.with_entities(Manager.mid, Manager.manager, Manager.email).all()
    return render_template('admin/delete_manager.html', objManager=objManager)


@authA.route('/deleted', methods=["POST", "GET"])
def Deleted():
    managerid = request.form['deleted_manager']
    print("manager id",managerid)
    objManager = Manager.query.filter_by(mid=managerid).first()
    objSection = Section.query.filter_by(manager_id = managerid).all()
    objProduct = Product.query.filter_by(manager_id = managerid).all()

    print("objManager",objManager)
    if objManager:
        if objSection:
            if objProduct:
                for o in objProduct:
                    db.session.delete(o)
                
                    db.session.commit()
                
            
            for o in objSection:        
                db.session.delete(o)

            db.session.commit()
        db.session.delete(objManager)
        db.session.commit()
        return render_template('admin/Admin_Dashboard.html', k='Manager Deleted')
    else:
        return render_template('admin/Admin_Dashboard.html', k='Manager Exists')


# User Edit,Delete and Create


@authA.route('/editUser', methods=["POST", "GET"])
def Edit_User():
    if session['aid'] is None:
        return render_template('user/User_login.html')
    objUser = User.query.with_entities(User.uid, User.user, User.password,User.email).all()
    return render_template('admin/edit_User.html', objUser=objUser)


@authA.route('/editedidUser', methods=["POST", "GET"])
def Edit_by_UId():
    if session['aid'] is None:
        return render_template('user/User_login.html')
    uid = request.form['edited_User']
    objUser = User.query.get(uid)

    return render_template('admin/edit_User_id.html', objUser=objUser)


@authA.route('/editedUser/<int:uid>', methods=["POST", "GET"])
def Edited_User(uid):
    user = request.form['User']
    password = request.form['password']
    email = request.form['email']
    print('User', user, 'email', email)
    objUser = User.query.get_or_404(uid)
    print(objUser)
    objUser.user = user
    objUser.password = password
    objUser.email = email
    db.session.commit()

    return render_template('admin/Admin_user.html', k='User Edited')


@authA.route('/deleteUser', methods=["POST", "GET"])
def Delete_User():
    if session['aid'] is None:
        return render_template('user/User_login.html')
    objUser = User.query.with_entities(User.uid, User.user, User.email).all()
    return render_template('admin/delete_User.html', objUser=objUser)


@authA.route('/deletedUser', methods=["POST", "GET"])
def Deleted_User():
    Userid = request.form['deleted_User']
    objUser = User.query.get(Userid)
    if objUser:
        db.session.delete(objUser)
        db.session.commit()
        return render_template('admin/Admin_user.html', k='User Deleted')
    else:
        return render_template('admin/Admin_user.html', k='User Exists')


@authA.route('/logout')
def Logout():
    session['aid'] = None
    return render_template('user/Start.html')
