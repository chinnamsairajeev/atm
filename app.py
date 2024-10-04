from flask import Flask,redirect,url_for,request,render_template
app=Flask(_name_)
data={
    '343434':{'pinno':111,'balance':2020}
}
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/get_accounts')  
def get_account():
    data_list=[{'account_no':accno,'balance':details['balance'],'pinno':details['pinno'] }for accno,details in data.items()]
    return data_list
@app.route('/create',methods=['GET','POST'])   

def create():
    if request.method=='POST':
        print(request.form)
        account_no=request.form['accno']
        pin_no=int(request.form['pinno'])
        #balance=float(request.form.get('balance'),0)
        balance=0
        if account_no in data:
            return 'account alredy existed'
        data[account_no]={'pinno':pin_no,'balance':balance}       
        return data


    return render_template('create.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        accno=request.form['acn'] #121212
        pin=int(request.form['pin'])
        if accno in data:
            if data[accno]['pinno']==pin:#{'pin:pin,'balance':'balance}
                return redirect(url_for('userpanel',account_no=accno,pin_no=pin))
            else:
                return 'pin wrong'
        else:
            return 'no account exists'
    return render_template('login.html')   
@app.route('/userpanel/<account_no>/<pin_no>')
def userpanel(account_no,pin_no):
    return render_template('userpanel.html',account_no=account_no,pin_no=pin_no) 
@app.route('/balance/<an>/<pn>')    
def balance(an,pn):
    details=data[an]
    data_list=[{'account_no':an,'balance':details['balance']}]
    balance=data_list[0]['balance']
    return render_template('balance.html',balance=balance)
@app.route('/credit/<an>/<pn>',methods=['GET','POST'])
def credit(an,pn):
    if request.method=='POST':
        amount=int(request.form['amount'])
        details=data[an] #if account is 343434 then details {'pinno':111,'balance':2020}
        data_list=[{'account_no':an,'balance':details['balance']}] #creating a list with accno,balance from above details
        if data_list[0]['account_no']==an: #validate accountno
            orginal_amount=data_list[0]['balance']
            data[an]['balance']=orginal_amount+amount
            print(data_list)
            return redirect(url_for('balance',an=an,pn=pn))
    return render_template('credit.html',an=an,pn=pn)  

@app.route('/withdraw/<an>/<pn>',methods=['GET','POST'])  
def withdraw(an,pn):
    if request.method=='POST':
        amount1=int(request.form['amount1'])
        details=data[an]
        data_list=[{'account_no':an,'balance':details['balance']}]
        orginal_amount=data_list[0]['balance']#40000
        if orginal_amount>=amount1:
            data[an]['balance']=orginal_amount-amount1
            return redirect(url_for('balance',an=an,pn=pn))
        else:
            return 'insufficent balance'    
      
    return render_template('withdraw.html')              
app.run(debug=True)