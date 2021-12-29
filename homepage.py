import csv
import os
from datetime import datetime
from flask_mysqldb import MySQL
from flask import Flask,render_template,url_for,redirect,flash,request,session ,jsonify

from forms import dailyreport, monthlyreport, employeereport, nextreport, finalreport, addremovereport, removereport, \
    addfoodreport, loginreport

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'employee'
app.config['MYSQL_CURSORCLASS'] ='DictCursor'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cursor1 = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    curr=mysql.connection.cursor()
    curse=mysql.connection.cursor()
    cur.execute('select sum(a.rate*b.quantity) as Amount from employee.food_table a JOIN employee.ordering b where b.food_name=a.f_name and month(b.ordered_date) = MONTH(now())')
    cursor1.execute('select count(id) as count from employee.employee_detail')
    cur1.execute('select count(id) as new from employee.employee_detail where month(doj)=month(now())')
    curr.execute('select count(a.type) as count from employee.food_table a JOIN employee.ordering b ON b.food_name=a.f_name where a.type="Veg" and date(b.ordered_date)=date(now())')
    curse.execute('select count(a.type) as total from employee.food_table a JOIN employee.ordering b ON b.food_name=a.f_name where a.type="Non-veg" and date(b.ordered_date)=date(now())')
    user_detail=cur.fetchall()
    user=list(user_detail)
    for row in user:
        info=row['Amount']
    count=cursor1.fetchall()
    cnt=list(count)
    for col in cnt:
        emp=col['count']
    newcnt=cur1.fetchall()
    emp_cnt=list(newcnt)
    for i in emp_cnt:
        new=i['new']
    vcnt=curr.fetchall()
    vcount=list(vcnt)
    for c in vcount:
        veg_count=c['count']
    nvcnt=curse.fetchall()
    nvcount=list(nvcnt)
    for k in nvcount:
        nonveg=k['total']
    return render_template('index.html',info=info,emp=emp,new=new,veg_count=veg_count,nonveg=nonveg)

@app.route('/daily_report', methods=['GET', 'POST'])
def daily_report():
    form = dailyreport()
    cur = mysql.connection.cursor()
    curse = mysql.connection.cursor()
    if form.validate_on_submit():
        date1=str(form.date1.data)
        cur.execute('select count(emp_id) as TOTAL from employee.ordering where ordered_date='+"'"+date1+"'")
        curse.execute('select food_name,quantity from employee.ordering where ordered_date=' + "'" + date1 + "'")
        user_detail = cur.fetchall()
        count = 0
        list2 = []
        for row in curse:
            list2.append(row)
        result_list = [[(v) for k,v in d.items()] for d in list2]
        var1=str(result_list).replace('[','').replace(']','')
        var2=str(var1).replace("'",'')
        print(var2)
        session['var2']=var2
        #print("Ordered foods are: ",result_list)
        for col in user_detail:
            count += 1
        col=str(col)
        session['col']=col
        #print("Total employee count: ",col[10])
        mysql.connection.commit()
        return redirect(url_for('order'))
    return render_template('daily_report.html',form=form)

@app.route('/order', methods=['GET', 'POST'])
def order():
    var2=session['var2']
    col=session['col']
    return render_template('order.html',var2=session['var2'],col=session['col'])

@app.route('/monthly_report', methods=['GET', 'POST'])
def monthly_report():
    form = monthlyreport()
    cur = mysql.connection.cursor()
    if form.validate_on_submit():
        start_date=str(form.start_date.data)
        end_date=str(form.end_date.data)
        try:
            cur.execute('select a.emp_name,sum(a.quantity*b.subsidy) as Deductions from employee.ordering a JOIN employee.food_table b ON a.food_name=b.f_name where a.ordered_date between '+ "'"+start_date+"'" 'and'+ "'"+end_date+"'" 'GROUP BY a.emp_name')
            user1=cur.fetchall()
            file1=list(user1)
            with open("report.csv","w") as final:
                w = csv.DictWriter(final, file1[0].keys(), delimiter='|')
                w.writerow(dict((fn, fn) for fn in file1[0].keys()))
                w.writerows(file1)
                paths=os.path.abspath(os.getcwd())
                session['paths']=paths
        except:
            print("Not found")
        mysql.connection.commit()
        return redirect(url_for('report'))
    return render_template('monthly_report.html',form=form)

@app.route('/report', methods=['GET', 'POST'])
def report():
    paths=session['paths']
    return render_template('report.html',paths=session['paths'])

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    form = employeereport()
    cur = mysql.connection.cursor()
    if form.validate_on_submit():
        empid=str(form.empid.data)
        session['empid']=empid
        check=False
        cur.execute('select name from employee.employee_detail where id='+"'"+empid+"'")
        for row in cur:
            check=True
            name1=cur.fetchone()
            name=name1['name']
            session['name']=name
            #print("Your name is: ",name.title())
        return redirect(url_for('next_page'))
    return render_template('employee.html',form=form)

@app.route('/next_page', methods=['GET', 'POST'])
def next_page():
    form = nextreport()
    cur = mysql.connection.cursor()
    cursor=mysql.connection.cursor()
    cur.execute('select f_id,f_name from employee.food_table')
    x=cur.fetchall()
    detail=list(x)
    """for row in abc:
        food_id=row['id']
        f_name=row['food_name']
        print(food_id,f_name)"""
    if form.validate_on_submit():
        item=str(form.item.data)
        quantity=str(form.quantity.data)
        session['quantity']=quantity
        cursor.execute('select f_name from employee.food_table where f_id=' + "'" + item + "'")
        f_name1=cursor.fetchall()
        f_name=list(f_name1)
        print(f_name)
        session['f_name']=f_name
        for row in f_name:
            food=row['f_name']
            print(food)
            session['food']=food
        return redirect(url_for('final'))
    return render_template('next_page.html',form=form,empid=session['empid'],name=session['name'],detail=detail)

@app.route('/final', methods=['GET', 'POST'])
def final():
    form=finalreport()
    cur=mysql.connection.cursor()
    ordered_date=datetime.now()
    formatted_date = ordered_date.strftime('%Y-%m-%d')
    print(formatted_date)
    empid=session['empid']
    name=session['name']
    f_name=session['f_name']
    food=session['food']
    quantity=session['quantity']
    if form.validate_on_submit():
        cur.execute("insert into employee.ordering (emp_id,emp_name,ordered_date,food_name,quantity) values("+"'"+empid+"'"','+"'"+name+"'"','+"'"+formatted_date+"'"',' +"'"+food+"'" ',' +"'"+quantity+"'" ")")
        mysql.connection.commit()
    mysql.connection.commit()
    return render_template('final.html',form=form,empid=session['empid'],name=session['name'],f_name=session['f_name'],quantity=session['quantity'])

@app.route('/addremove', methods=['GET', 'POST'])
def addremove():
    form=addremovereport()
    form1=removereport()
    cursor1=mysql.connection.cursor()
    if form.validate_on_submit():
        id=str(form.id.data)
        name=str(form.name.data)
        email=str(form.email.data)
        address=str(form.address.data)
        date_of_joining=str(form.date_of_joining.data)
        experience=str(form.experience.data)
        cursor1.execute('insert into employee.employee_detail(id,name,email,address,doj,experience) values(%s,%s,%s,%s,%s,%s)',(id,name,email,address,date_of_joining,experience,))
        mysql.connection.commit()
    if form1.validate_on_submit():
        id1=str(form1.id1.data)
        cursor1.execute('delete from employee.employee_detail where id='+"'"+id1+"'")
        mysql.connection.commit()
    return render_template('addremove.html',form=form,form1=form1)

@app.route('/foodreport', methods=['GET', 'POST'])
def foodreport():
    form=addfoodreport()
    cursor=mysql.connection.cursor()
    if form.validate_on_submit():
        food_id=str(form.food_id.data)
        food_name=str(form.food_name.data)
        food_type=str(form.food_type.data)
        rate=str(form.rate.data)
        subsidy=str(form.subsidy.data)
        cursor.execute('insert into employee.food_table(f_id,f_name,type,rate,subsidy) values (%s,%s,%s,%s,%s)',(food_id,food_name,food_type,rate,subsidy,))
        mysql.connection.commit()
    return render_template('foodreport.html',form=form)

@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    form=loginreport()
    if form.validate_on_submit():
        username=str(form.username.data)
        password=str(form.password.data)
        role=str(form.role.data)
        if(username=='admin' and password=='admin@12345' and role=='1'):
            return redirect(url_for('addremove'))
        elif(username=='clientadmin' and password=='admin@4532' and role=='2'):
            return redirect(url_for('foodreport'))
        else:
            flash(f'Invalid Username or password or role')
    return render_template('loginpage.html',form=form)

@app.route('/empreport', methods=['GET', 'POST'])
def empreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from employee.employee_detail')
    e_report=cursor.fetchall()
    emp_report=list(e_report)
    return render_template('empreport.html',emp_report=emp_report)

@app.route('/viewreport', methods=['GET', 'POST'])
def viewreport():
    cursor=mysql.connection.cursor()
    cursor.execute('select emp_name,food_name,quantity from employee.ordering where date(ordered_date) = date(now())')
    view_detail=cursor.fetchall()
    view=list(view_detail)
    return render_template('viewreport.html',view=view)

if __name__ =="__main__":
    app.run(debug =True)