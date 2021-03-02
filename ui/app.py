import datetime
import sqlite3
from werkzeug.exceptions import abort

from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Response

import sys
sys.path.append('../')


from ui.database.utils import _add_to_database, _create_job_record
from ui.database.db_schemas import Job, Result, PyramidPool
from ui import create_app



"""
1. In extract() function, after 'if request.method ',
    replace the way web_class and attr are collected from
    the user by web_cls_select(). that way, the UI is much more
    user friendly and the user can select.

2. In retrieve_resutls() function, put the results in a 
    CSV document and set up a link for the user to download the 
    results. you can use export() function, at the end

3. In submit review, ask user to upload a CSV document,
    and then add this to the database

"""


app = create_app()

@app.route('/')
def index():
    print(Job.query.all())
    return render_template('index.html', jobs=Job.query.all())

@app.route('/extract', methods=('GET', 'POST'))
def extract():
    web_class = None
    if request.method == 'POST':
        #TODO: 1
        web_class = request.form['web_class']
        attr = request.form['attr']
        cur_time = datetime.datetime.today()

    if not web_class:
        flash('Web Class is required!')
    else:
        job_record = _create_job_record(web_class, attr, cur_time)
        _add_to_database(job_record)
        return redirect(url_for('index'))
    return render_template('extract.html')

@app.route('/extract-results', methods=('GET', 'POST'))
def retrieve_resutls():
    web_class = None
    if request.method == 'POST':
        web_class = request.form['web_class']
        attr = request.form['attr']
        cur_time = datetime.datetime.today()

    if not web_class:
        flash('Web Class is required!')
    else:
        res = Result.query.filter_by(web_cls_num=web_class, attr_nm=attr)#1. from db.resutls get the latest extraction results
        #TODO:2
        
        return redirect(url_for('index'))
    return render_template('extract.html')   


@app.route('/submit-review', methods=('GET', 'POST'))
def submit_review():
    web_class = None
    if request.method == 'POST':
        web_class = request.form['web_class']
        attr = request.form['attr']
        cur_time = datetime.datetime.today()

    if not web_class:
        flash('Web Class is required!')
    else:
        #TODO3 : upload a review document
        # and it to the database 
        #create a training job, add it to database
        # and run training

        return redirect(url_for('index'))
    return render_template('extract.html')

#select web class 
def web_cls_select():
    ''' Matching Tool -- Web Class Filter '''
    search = request.args.get('q')
    results = PyramidPool.query.with_entities(PyramidPool.web_cls_num, PyramidPool.web_cls_nm) \
                             .distinct() \
                             .filter(or_(PyramidPool.web_cls_nm.like(str(search)+"%"), PyramidPool.web_cls_num.like(str(search)+"%"))) \
                             .all()
    results_dict = dict()
    results_dict["results"] = [{"id": x[0], "text": "{0}: {1}".format(*x)} for x in sorted(results)]
    return jsonify(results_dict)

@app.route("/export", methods=["GET", "POST"])
def export():
    results_filename='testing_export'
    ''' Download Match Results to CSV File without ATP '''
    def retrieve_data():
        for result in ['khuiy','fuyuu','fhfh']:
            yield (
                str(result[:2]),
                str(result[:3]),
                str(result[:4])
            )

    # streaming CSV content -- to send over large data
    def generate(rows):
        data = StringIO()       # In-Memory File
        w    = csv.writer(data)
        
        # CSV File Headers
        w.writerow(('SKU_NUM','ATTR_NM', 'ATTR_VAL'))
        yield data.getvalue()
        data.seek(0)     # reset pointer
        data.truncate(0) # reset StringIO size
        for row in rows:
            w.writerow(row)
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
    
    rows = (x for x in retrieve_data())   
    # stream the response as the data is generated
    response = Response(generate(rows), mimetype='text/csv')
    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename=f"{results_filename}.csv")
    return render_template('export.html', response = response)

app.run(debug = False, host="0.0.0.0", port="8080", use_reloader=False,)