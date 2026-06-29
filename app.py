from flask import Flask,request,render_template,redirect
import sqlite3
import os
app=Flask(__name__)
con = sqlite3.connect("proj.db")
cursor = con.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT NOT NULL,
    amount INTEGER NOT NULL,
    category TEXT NOT NULL,
    expense_date DATE NOT NULL
)
""")
con.commit()
con.close()
@app.route("/",methods=["POST","GET"])
def data():
    total=0
    tran=0
    da=[]
    con=sqlite3.connect('proj.db')
    cursor=con.cursor()
    if request.method=='POST':
        ename=request.form.get('ename')
        amount=request.form.get('amount')
        category=request.form.get('category')
        date=request.form.get('date')
        cursor.execute("insert into expenses(expense_name, amount, category, expense_date) values(?,?,?,?)",(ename,amount,category,date))
    con.commit()
    cursor.execute('select * from expenses')
    data=cursor.fetchall()
    for i in data:
            expense={
                'id':i[0],
                'ename':i[1],
                'amount':i[2],
                'category':i[3],
                'date':i[4]
        }
            da.append(expense)
    con.close()
    for i in da:
        total+=int(i["amount"])
    tran=len(da)
    return render_template('proj.html',da=da,total=total,tran=tran)
@app.route("/delete/<int:id>")
def delete(id):
    con = sqlite3.connect("proj.db")
    cursor = con.cursor()
    cursor.execute('delete from expenses where id=?',(id,))
    con.commit()
    con.close()
    return redirect("/")
@app.route("/update/<int:id>",methods=['POST',"GET"])
def update(id):
    con = sqlite3.connect("proj.db")
    cursor = con.cursor()
    if request.method=='POST':
        col=request.form.get('col')
        new=request.form.get('new')
        col1=f"update expenses set {col}=? where id=?"
        cursor.execute(col1,(new,id))
        con.commit()
        con.close()
        return redirect("/")
    return render_template('update.html',id=id)
@app.route("/search",methods=["GET","POST"])
def search():
      da=[]
      total=0
      tran=0
      con = sqlite3.connect("proj.db")
      cursor = con.cursor()
      if request.method=="POST":
           ser=request.form.get('ser')
           cursor.execute("Select * from expenses where expense_name like ?",("%"+ser+"%",))
           data=cursor.fetchall()
           for i in data:
                expense={
                'id':i[0],
                'ename':i[1],
                'amount':i[2],
                'category':i[3],
                'date':i[4]
        }
                da.append(expense)
           for i in da:
                total+=int(i['amount'])
           tran=len(da)
      con.close()
      return render_template('proj.html',da=da,total=total,tran=tran)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )




