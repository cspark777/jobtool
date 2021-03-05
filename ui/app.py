from datetime import datetime
import sqlite3
from werkzeug.exceptions import abort
import pandas as pd

from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Response

import sys
sys.path.append('../')


from ui.database.utils import _add_to_database, _create_job_record, _create_review_record, _bulk_add_to_database
from ui.database.db_schemas import Job, Result, PyramidPool, Review
from ui import create_app

import json

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

@app.route('/get_attrs', methods=["GET"])
def get_attrs():
    web_class = request.args.get('web_class')
    attrs = PyramidPool.query.with_entities(PyramidPool.attr_nm).distinct().filter(PyramidPool.web_cls_num==web_class).all()

    res = []
    for attr in attrs:
        data = {"attr_name": attr.attr_nm}
        res.append(data)

    res_json = json.dumps(res)
    return res_json

@app.route('/job_list', methods=["GET"])
def job_list():
    jobs = Job.query.order_by(Job.id.desc()).all()
    
    result = []
    for job in jobs:
        job.date_created = job.date_created.strftime("%Y-%m-%d %H:%M:%S")

        result.append(job)
    return render_template('job_list.html', jobs=result)

@app.route('/extract', methods=('GET', 'POST'))
def extract():
    if request.method == 'GET':
        web_classes = PyramidPool.query.with_entities(PyramidPool.web_cls_num, PyramidPool.web_cls_nm).distinct().all()

        attrs = []
        if len(web_classes) > 0:
            first_web_class = web_classes[0]
            attrs = PyramidPool.query.with_entities(PyramidPool.attr_nm).distinct().filter(PyramidPool.web_cls_num==first_web_class[0]).all()
            
        return render_template('extract.html', web_classes=web_classes, attrs=attrs)
    else:
        web_class = request.form['web_class']
        attr_nm = request.form['attr_nm']

        attrs = PyramidPool.query.with_entities(PyramidPool.attr_nm).distinct().filter(PyramidPool.web_cls_num==web_class).filter(PyramidPool.attr_nm==attr_nm).all()

        cur_time = datetime.datetime.today()

        job_record = _create_job_record(web_class, attrs[0].attr_nm, cur_time)
        _add_to_database(job_record)

        return redirect(url_for('job_list'))

@app.route('/get_result_attrs', methods=["GET"])
def get_result_attrs():
    web_class = request.args.get('web_class')
    attrs = Result.query.with_entities(Result.attr_nm).distinct().filter(Result.web_cls_num==web_class).all()

    res = []
    for attr in attrs:
        data = {"attr_name": attr.attr_nm}
        res.append(data)

    res_json = json.dumps(res)
    return res_json


@app.route('/extract-results', methods=('GET', 'POST'))
def retrieve_results():
    
    web_classes = Result.query.with_entities(Result.web_cls_num, PyramidPool.web_cls_nm).join(PyramidPool, PyramidPool.web_cls_num==Result.web_cls_num).distinct().all()

    attrs = []
    if len(web_classes) > 0:
        first_web_class = web_classes[0]
        attrs = Result.query.with_entities(Result.attr_nm).distinct().filter(Result.web_cls_num==first_web_class[0]).all()  

    if request.method == 'GET':  

        download_url = ""
        results = None
        return render_template('result_list.html', web_classes=web_classes, attrs=attrs, download_url=download_url, results=results)

    else:        
        web_class = request.form['web_class']
        attr_nm = request.form['attr_nm']

        results = Result.query.filter_by(web_cls_num=web_class, attr_nm=attr_nm)
        response_results = []
        for r in results:
            r.date_created = r.date_created.strftime("%Y-%m-%d %H:%M:%S")
            response_results.append(r)

        download_url = "/export?class={}&attr_nm={}".format(web_class, attr_nm)
        return render_template('result_list.html', web_classes=web_classes, attrs=attrs, download_url=download_url, results=response_results)   


@app.route('/submit-review', methods=('GET', 'POST'))
def submit_review():
    reviews = []
    error = ""

    if request.method == 'POST': 
       
        #TODO3 : upload a review document
        # and it to the database 
        #create a training job, add it to database
        # and run training

        file = request.files['file']
                 
        col_names = ['Review_ID','SKU_NUM','ITEM_DESC', 'ATTR_NM', 'ATTR_VAL', 'ATTR_VAL_Reviewed' , 'Creation_Date', 'WEB_CLASS_NUM']
        #try:
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(file,names=col_names, header=0)
        
        bulk_reviews = []
        for i,row in csvData.iterrows():
            _bulk_add_to_database
            date_time_obj = datetime.strptime(row["Creation_Date"], '%Y-%m-%d %H:%M:%S')
            new_review = _create_review_record(row["Review_ID"], row["SKU_NUM"], 
                            row["ITEM_DESC"], row["ATTR_NM"], row["ATTR_VAL"], 
                            row["ATTR_VAL_Reviewed"], 
                            date_time_obj, row["WEB_CLASS_NUM"])
            
            bulk_reviews.append(new_review)

            reviews.append({"review_id": row["Review_ID"], 
                            "sku_num": row["SKU_NUM"], 
                            "item_desc": row["ITEM_DESC"], 
                            "attr_nm": row["ATTR_NM"], 
                            "attr_val": row["ATTR_VAL"], 
                            "attr_val_rev": row["ATTR_VAL_Reviewed"], 
                            "create_date": row["Creation_Date"], 
                            "web_cls_num": row["WEB_CLASS_NUM"]})

        _bulk_add_to_database(bulk_reviews)
        #except:
        #    error = "CSV file format error"
             
    return render_template('submit_review.html', reviews=reviews, error_msg=error)
        

@app.route("/export", methods=["GET"])
def export():

    web_class = request.args.get('class')
    attr_nm = request.args.get('attr_nm')

    results = Result.query.filter_by(web_cls_num=web_class, attr_nm=attr_nm)

    csv = "Extract_ID,SKU_NUM,ITEM_DESC,ATTR_NM,ATTR_VAL,PRED_ATTR_VAL,Confidence,Creation_Date,Model_ID,Job_ID,WEB_CLASS_NUM\n"

    for res in results:
        csv = csv + '{},{},\"{}\",\"{}\",\"{}\",\"{}\",{},{},{},{},{}\n'.format(res.extract_id, res.sku_num, res.item_desc, res.attr_nm, res.attr_val, res.pred_attr_val, res.confidence, res.date_created, res.model_id, res.job_id, res.web_cls_num)

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=results.csv"})


app.run(debug = False, host="0.0.0.0", port="8080", use_reloader=False,)