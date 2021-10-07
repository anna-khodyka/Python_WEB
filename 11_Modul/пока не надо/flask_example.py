from flask import Flask, request, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'Home Page'


@app.route('/career/')
def career():
    return 'Career Page'


@app.route('/feedback/')
def feedback():
    return 'Feedback Page'


@app.route('/user/<id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


@app.route('/find/user')
def find_user():
    # получаем value по имеющемуся ключу
    # строка http://127.0.0.1:5000/find/user?name=Test
    user_name = request.args.get('name')
    return f"Searching for user by name '{user_name}'"


@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    app.run()
