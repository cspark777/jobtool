from datetime import datetime
import sqlite3
from werkzeug.exceptions import abort
import pandas as pd

from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Response

import sys
sys.path.append('../')


from ui.database.utils import _add_to_database, _create_job_record, _create_review_record, _bulk_add_to_database, _update_database
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
    return render_template('index.html')

@app.route('/get_attrs', methods=["GET"])
def get_attrs():
    web_class = request.args.get('web_class')
    attrs = PyramidPool.query.with_entities(PyramidPool.attr_nm).distinct().filter(PyramidPool.web_cls_num==web_class).all()

    res = []
    for attr in attrs:
        data = {"attr_name": attr.attr_nm.strip()}
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
'''
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

        cur_time = datetime.today()

        job_record = _create_job_record(web_class, attrs[0].attr_nm, cur_time)
        _add_to_database(job_record)

        return redirect(url_for('job_list'))
'''

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


@app.route('/extract_results', methods=('GET', 'POST'))
def extract_results():
    
    web_classes = Result.query.with_entities(Result.web_cls_num, Result.web_cls_nm).distinct().all()

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
'''
@app.route('/submit_review', methods=('GET', 'POST'))
def submit_review():
    reviews_arr = []
    error = ""
    submit_count = 0

    if request.method == 'POST': 
       
        try:
            file = request.files['file']
                     
            col_names = ['SKU_NUM','ITEM_DESC', 'ATTR_NM', 'ATTR_VAL', 'ATTR_VAL_Reviewed', 'WEB_CLASS_NUM']
            #try:
            # Use Pandas to parse the CSV file
            csvData = pd.read_csv(file,names=col_names, header=0)
            
            bulk_reviews = []
            new_jobs = []
            for i,row in csvData.iterrows():
                
                date_time_obj = datetime.now()
                new_review = _create_review_record(row["SKU_NUM"], 
                                row["ITEM_DESC"], row["ATTR_NM"], row["ATTR_VAL"], 
                                row["ATTR_VAL_Reviewed"], 
                                date_time_obj, row["WEB_CLASS_NUM"])
                bulk_reviews.append(new_review)

                new_job = _create_job_record(row["WEB_CLASS_NUM"], row["ATTR_NM"], date_time_obj)
                new_jobs.append(new_job)

            submit_count = len(bulk_reviews)

            _bulk_add_to_database(bulk_reviews)
            _bulk_add_to_database(new_jobs)

            reviews = Review.query.order_by(Review.date_created.desc()).all()
        
            
            for review in reviews:
                review.date_created = review.date_created.strftime("%Y-%m-%d %H:%M:%S")

                reviews_arr.append(review)        
        except:
            error = "CSV file format error"
             
    return render_template('submit_review.html', reviews=reviews_arr, error_msg=error, submit_count=submit_count)
''' 
@app.route('/submit_review', methods=('GET', 'POST'))
def submit_review():
    reviews_arr = []
    error = ""

    try:       
        reviews = Review.query.order_by(Review.date_created.desc()).all()
    
        for review in reviews:
            review.date_created = review.date_created.strftime("%Y-%m-%d %H:%M:%S")

            reviews_arr.append(review)        
    except:
            error = "get review data error"
             
    return render_template('submit_review.html', reviews=reviews_arr, error_msg=error)

@app.route('/submit_review2', methods=('GET', 'POST'))
def submit_review2():
    reviews_arr = []
    error = ""
    attr_vals_json = ""
    attr_vals_arr = []
    #try:       
    attr_vals = Review.query.with_entities(Review.attr_val).distinct().all()
    _id = 0;
    for val in attr_vals:
        _id = _id + 1
        attr_vals_arr.append({"value":val.attr_val, "id": _id, "text": val.attr_val} )
    attr_vals_json = json.dumps(attr_vals_arr)

    reviews = Review.query.order_by(Review.date_created.desc()).all()

    for review in reviews:
        review.date_created = review.date_created.strftime("%Y-%m-%d %H:%M:%S")
        reviews_arr.append(review)    
        
    
    
    #except:
    #        error = "get review data error"
             
    return render_template('submit_review2.html', reviews=reviews_arr, attr_vals_json=attr_vals_json, error_msg=error)

@app.route('/update_attr_rev', methods=["POST"])
def update_attr_rev():
    pk = request.form['pk']
    attr_val_rev = request.form['value']

    print("-------------------")
    print(pk, attr_val_rev)

    review = Review.query.filter_by(id=int(pk)).first()

    if review is None:
        return Response("error")

    print(review)

    review.attr_val_rev = attr_val_rev
    _update_database()

    return Response("success")



@app.route("/export", methods=["GET"])
def export():

    web_class = request.args.get('class')
    attr_nm = request.args.get('attr_nm')

    results = Result.query.filter_by(web_cls_num=web_class, attr_nm=attr_nm)

    csv = "ID,SKU_NUM,ATTR_NM,ITEM_DESC,ATTR_VAL,PRED_ATTR_VAL,WEB_CLASS_NUM,WEB_CLASS_NM,Confidence,Model_ID,Job_ID,Creation_Date\n"

    for res in results:
        csv = csv + '{},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",{},\"{}\",{},{},{},\"{}\"\n'.format(res.id, res.sku_num, res.attr_nm, res.item_desc, res.attr_val, res.pred_attr_val, res.web_cls_num, res.web_cls_nm, res.confidence, res.model_id, res.job_id, res.date_created)

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=results.csv"})


app.run(debug = False, host="0.0.0.0", port="8080", use_reloader=False,)