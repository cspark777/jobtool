import os
import json
import pandas as pd

from flask import current_app         # retrieves current app

from ui import db
from ui.database.db_schemas import Job


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

def _add_to_database(item):
    db.session.add(item)
    db.session.commit()

def _delete_from_database(item):
    db.session.delete(item)
    db.session.commit()