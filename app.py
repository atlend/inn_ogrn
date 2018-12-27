from flask import Flask, request, render_template

from db_use import DBUse
import req

app = Flask(__name__)


def what_type(number):
    if len(number) == 10:
        return 'ИНН'
    elif len(number) == 13:
        return 'ОГРН'
    return ''


def what_status(boolean):
    if boolean:
        return "является"
    return "не является"


@app.route('/', methods=['get', 'post'])
def init():
    d = {}
    if request.method == 'POST':
        d['number'] = request.form["a"]
        d['type'] = what_type(d['number'])
        if d['type']:
            with DBUse() as db:
                status = db.find_cached_status(d['number'])
                if not status:
                    status = d['status'] = what_status(req.send_query(d['number']))
                    db.push_data(d)
                    title = f"{d['type']} c сайта"
                else:
                    status = status[0]
                    title = f"{d['type']} из кэша"
            return render_template('index.html', title=title, status=status)
        else:
            title = "10 или 13 цифр!"
            return render_template('index.html', title=title)
    else:
        with DBUse() as db:
            results = db.pull_data()
            keys = db.column_keys()
            for i in range(len(results)):
                results[i] = {keys[j]: results[i][j] for j in range(len(results[i]))}
        title = "Журнал"
        return render_template('index.html', title=title, results=results)


if __name__ == '__main__':
    app.run(debug=True)
