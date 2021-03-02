DROP TABLE IF EXISTS posts;


CREATE TABLE extract_job (
    Job_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Creation_Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    WEB_CLASS_NUM INTEGER NOT NULL,
    ATTR_NM TEXT NOT NULL
);

CREATE TABLE extractor_model (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    model_parameters TEXT NOT NULL,
    model_checkpoint, 
    attr_name TEXT NOT NULL,
    evaluation_results,
);

CREATE TABLE extractor_result(
    res_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    job_id INTEGER NOT NULL,
    class_name,
    sku,
    attr_name,
    attr_value,
    attr_pred_value,
    confidence  
);

CREATE TABLE extractor_review (
    rev_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    res_id INTEGER NOT NULL,
    class_name,
    sku,
    attr_name,
    attr_value_by_reviewer,
    comment
);




