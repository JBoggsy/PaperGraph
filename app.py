from flask import Flask, render_template, session, request, url_for, redirect

from graph import PaperGraph

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.secret_key = 'AuhdpiuhPPUEFpUpIEUFeopBuoEWAwdwdfeifh3483pEPCnep9nPEp9'

graph = PaperGraph("static/graph.json")
graph.load_graph()


@app.route('/', methods=['GET', 'POST'])
def splash_page():
    if request.method == 'GET':
        if 'logged_in' not in session or not session['logged_in']:
            session['logged_in'] = False
            return render_template("login.html")
        else:
            return render_template("home.html", GRAPH_URL=url_for('static', filename="graph.json"))
    else:
        password = request.form['pwd']
        if password == app.config['PASSWORD']:
            session['logged_in'] = True
            return render_template("home.html", GRAPH_URL=url_for('static', filename="graph.json"))


@app.route('/new_paper', methods=['GET', 'POST'])
def new_paper_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('/')
    if request.method == 'GET':
        return render_template("new_paper.html")
    else:
        paper_title = request.form['title']
        paper_authors_str = request.form['auths']
        paper_year = int(request.form['year'])
        paper_authors = [a.strip().lower() for a in paper_authors_str.split(',')]
        paper_name = hash(paper_title+paper_authors_str+str(paper_year))
        paper_dict = {'name': paper_name,
                      'title': paper_title,
                      'authors': ','.join(paper_authors),
                      'year': paper_year}
        print(paper_dict)
        graph.add_paper(paper_name, paper_title, paper_authors_str, str(paper_year), str(1))
        return redirect('/')



if __name__ == '__main__':
    app.run()
