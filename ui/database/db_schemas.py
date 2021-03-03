from ui import db
import datetime

class Job(db.Model):
    __tablename__ = 'extract_job'

    id = db.Column('Job_ID', db.Integer, primary_key=True)
    date_created = db.Column('Creation_Date', db.DateTime, nullable=False)
    web_cls_num  = db.Column('WEB_CLASS_NUM', db.Integer)
    attr_nm  = db.Column('ATTR_NM', db.Text)
    #results_filename  = db.Column('Results_Filename', db.String(128), nullable=False)
    #results_notes     = db.Column('Results_Notes', db.String(256), default=None)
    #status = db.Column('Status', db.String(32), nullable=False, default='Incomplete')
    results = db.relationship('Result', backref='extract_job', lazy='dynamic')
    models = db.relationship('TrainedModel', backref='extract_job', lazy='dynamic')
    
    def __repr__(self):
        return f'Job("{self.id}")'
    
class Result(db.Model):
    __tablename__ = 'extract_result'

    id = db.Column('Result_ID', db.Integer, primary_key=True)
    date_created = db.Column('Creation_Date', db.DateTime, nullable=False)
    web_cls_num  = db.Column('WEB_CLASS_NUM', db.Integer)
    attr_nm  = db.Column('ATTR_NM', db.Text)
    attr_val = db.Column('ATTR_VAL', db.Text)
    confidence = db.Column('Confidence', db.Float)
    model_id = db.Column('Model_ID', db.Integer, db.ForeignKey('trained_model.Model_ID'), nullable=False)
    job_id = db.Column('Job_ID', db.Integer, db.ForeignKey('extract_job.Job_ID'), nullable=False)
    
    def __repr__(self):
        return f'Result("{self.id}")'

class TrainedModel(db.Model):
    __tablename__ = "trained_model"

    id = db.Column('Model_ID', db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column('Creation_Date', db.DateTime, nullable=False)
    model_path = db.Column('Model_Path', db.Text)
    web_cls_num  = db.Column('WEB_CLASS_NUM', db.Integer)
    attr_nm  = db.Column('ATTR_NM', db.Text)
    job_id = db.Column('Job_ID', db.Integer, db.ForeignKey('extract_job.Job_ID'))
    models = db.relationship('Result', backref='trained_model', lazy='dynamic')
    
    def __repr__(self):
        return f'<TrainedModel: {self.id}><Name: {self.name}>'

class Review(db.Model):
    __tablename__ = 'match_review'

    id = db.Column('Review_ID', db.Integer, primary_key=True)
    date_created = db.Column('Creation_Date', db.DateTime, nullable=False)
    web_cls_num  = db.Column('WEB_CLASS_NUM', db.Integer)
    attr_nm  = db.Column('ATTR_NM', db.Text)
    attr_val = db.Column('ATTR_VAL', db.Text)
    attr_val_rev = db.Column('ATTR_VAL_Reviewed', db.Text, default=None)

    def __repr__(self):
        return f'Review("{self.id}")'

class PyramidPool(db.Model):
    __tablename__ = 'pyr'
    
    sku_num = db.Column('SKU_NUM', db.String(50), primary_key=True)
    attr_nm  = db.Column('ATTR_NM', db.Text, primary_key=True)
    web_cls_num  = db.Column('WEB_CLASS_NUM', db.Integer)
    web_cls_nm = db.Column('WEB_CLASS', db.String(255))
    item_desc = db.Column('ITEM_DESC', db.Text)
    attr_val = db.Column('ATTR_VAL', db.Text)
