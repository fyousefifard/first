#!../bin/python
from core   import db
from bottle import route, run, template, redirect,response
from bottle import static_file, request, post,get

@route('/')
def mainpage():
    title = 'home page'
    base = ''
    return template('templates/mainp.html', title=title, base=base)

    

@route('/hello/<esm>')
def greet(esm='Stranger'):
    f = open('data.txt', 'a')
    f.write('name: {}\n'.format(esm))
    f.close()
    return template('Hello <strong>{{e}}</strong>, how are you?', e=esm)
@route('/hello/')
def hello():
    k='Fatima'
    return template('Hello world Python<b> {{p}}</b>',p=k)

@route('/read_database/<_pass>')
def read(_pass):
    data = "Wrong Pass"
    if _pass == '12345':
        f = open('data.txt', 'r')
        data = f.read()
        f.close()
    
    
    return template(" content of file data.txt equal : </br>{{data}}", data=data)


@route('/statics/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='statics/css')

@route('/statics/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='statics/js')



"""@route('/form/<form_name>')
def form_view(form_name):
    return template('templates/' + form_name)"""
@get('/form/<form_name>')
def form_view(form_name):
    data={}
    return template('templates/' + form_name,data=data)

@route('/statics/<filename>')
def server_static(filename):
    return static_file(filename, root='statics/')



@post('/form-submit')
def form_submit():
    f = request.forms.get('firstname', None)
    l = request.forms.get('lastname', None)
    c = request.forms.get('country', None)
    
    u = request.forms.get('username', None)
    p = request.forms.get('password', None)
    z = request.forms.get('zipcod', None)
    r = request.forms.get('confpassword', None)
    m= request.forms.get('mobileno', None)
    e = request.forms.get('email', None)
    if (r==p):
	account_info=dict(
        firstname=request.forms.get('firstname', None),
        lastname= request.forms.get('lastname', None),
	country = request.forms.get('country', None),
    	username = request.forms.get('username', None),
    	password = request.forms.get('password', None),
    	zipcode = request.forms.get('zipcod', None),
    	mobile_number= request.forms.get('mobileno', None),
    	email = request.forms.get('email', None)
    	)
	db.Usertbl.insert_one(account_info)
        return redirect("/")
    else:
	data={}
	data['error']='error,Your Password is not Equal'
        return template('templates/register.html')

@post('/login')
def form_login():
    f = request.forms.get('username', None)
    l = request.forms.get('password', None)
    """isuser=False"""
    isuser=db.Usertbl.find({'username':f,'password':l})
    print(isuser)
    if isuser:
	    response.set_cookie('user_id',str(isuser['_id']))
            return redirect("/") 
    else:
            return redirect("templates/login.html")           
        





@route('/successful')
def successful():
    data = list(db.Usertbl.find().limit(20))
    
    return template('templates/table.html', data=data)
    

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
