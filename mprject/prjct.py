import shelve
from bottle import route, run, template, redirect
from bottle import static_file, request, post

@route('/')
def mainpage():
    return template('templates/mainp.html')

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



@route('/form/<form_name>')
def form_view(form_name):
    return template('templates/' + form_name)

@route('/statics/<filename>')
def server_static(filename):
    return static_file(filename, root='statics/')


@post('/form-submit')
def form_submit():
    f = request.forms.get('firstname', None)
    l = request.forms.get('lastname', None)
    c = request.forms.get('country', None)
    sh = shelve.open('db.db')
    u = request.forms.get('username', None)
    p = request.forms.get('password', None)
    z = request.forms.get('zipcod', None)
    r = request.forms.get('confpassword', None)
    m= request.forms.get('mobileno', None)
    e = request.forms.get('email', None)
    if (r==p):
        sh = shelve.open('db.db')
        sh[f + ' _' + l] = dict(firstname=f, lastname=l ,countrty=c,username=u,password=p,zipcod=z,mobileno=m,email=e)
        sh.close()
        return redirect("/successful")
    else:
        return template('Your Password is not Equal')

@post('/login')
def form_login():
    f = request.forms.get('username', None)
    l = request.forms.get('password', None)
    isuser=False
    sh = shelve.open('userinfo.db')
    for item in sh:
        if (item['username']==f and item['password']==l):
            isuser=True
            break
    sh.close()        
    if isuser:
            return redirect("/welcom") 
    else:
            return redirect("/")           
        





@route('/successful')
def successful():
    conn = shelve.open('db.db')
    data = conn.items()
    conn.close()
    return template('templates/table.html', data=data)
    

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
