import os
import json
import pandas as pd

from flask import current_app         # retrieves current app

from ui import db
from ui.database.db_schemas import Job, Review, Result


def _create_job_record(web_class, attr, cur_time):
    return Job(web_cls_num=web_class, 
                    attr_nm=attr,
                    date_created=cur_time)

def _create_result_record(web_class, 
                          attr, attr_val, confidence, 
                          job_id, model_id,
                          cur_time):
    return Result(web_cls_num=web_class, 
                    attr_nm=attr,
                    attr_val= attr_val,
                    confidence = confidence,
                    model_id = model_id,
                    job_id = job_id, 
                    date_created=cur_time)

def _create_review_record( 
                          sku_num, item_desc, attr_nm, attr_val, attr_val_rev,
                          date_created, web_cls_num):
    return Review(
                    sku_num=sku_num,
                    item_desc=item_desc,
                    attr_nm=attr_nm,
                    attr_val=attr_val,
                    attr_val_rev=attr_val_rev,
                    date_created=date_created,
                    web_cls_num=web_cls_num)

def _add_to_database(item):
    db.session.add(item)
    db.session.commit()

def _bulk_add_to_database(items):
    db.session.bulk_save_objects(items)
    db.session.commit()

def _delete_from_database(item):
    db.session.delete(item)
    db.session.commit()