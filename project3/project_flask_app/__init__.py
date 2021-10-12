import os
from flask import Flask, render_template,url_for, flash, redirect, request
from forms import RegistrationForm
from mangodb import get_result,insertCollection,dropCollection

#def create_app():
app = Flask(__name__)
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'
    
@app.route('/')
def home():
    return  render_template('layout.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 알람 카테고리에 따라 부트스트랩에서 다른 스타일을 적용 (success, danger) 
        flash(f'{form.username.data} 님 가입 완료!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/search', methods=["GET", "POST"])
def search():
    flag="대기"
    pushpop=[]
    if request.method=='GET':
        keyword=request.args.get('keyword')
        try:
            Pnum=int(request.args.get('PNum'))
        except:
            Pnum=-1
        try:
            Psize=int(request.args.get('Psize'))
        except:
            Psize=-1
        sortCd=request.args.get('sortC')
        #clearing=request.args.get('clearing')
        if (keyword != ""):
            result=get_result(key=keyword,number=Pnum,pSize=Psize,SortCd=sortCd)
            pushpop.append(result[4])
            insertCollection(result)
            flag="완료"
            return render_template('search.html',dd=flag) 
    return render_template('search.html',dd=flag)

if __name__ == "__main__":
    app.run(debug=True)
