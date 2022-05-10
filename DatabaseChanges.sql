CREATE TABLE attr_user_data (
   id int NOT NULL AUTO_INCREMENT,
   gender varchar(6) DEFAULT NULL,
   age  decimal(4,2) DEFAULT NULL,
   hypertension  int(1) DEFAULT NULL,
   heart_disease  int(1) DEFAULT NULL,
   ever_married  varchar(3) DEFAULT NULL,
   work_type  varchar(13) DEFAULT NULL,
   Residence_type  varchar(5) DEFAULT NULL,
   avg_glucose_level  decimal(5,2) DEFAULT NULL,
   bmi  varchar(3) DEFAULT NULL,
   smoking_status  varchar(15) DEFAULT NULL,
   stroke  int(1) DEFAULT NULL,
   uname varchar(255) NOT NULL,
   PRIMARY KEY (id));


 CREATE TABLE preds (
         uname varchar(255) NOT NULL,
         prediction varchar(255),
  ); 