DROP TABLE IF EXISTS task;

CREATE TABLE task(
   task_id INT NOT NULL AUTO_INCREMENT,
   task_startTime VARCHAR(255),
   task_userName VARCHAR(255),
   task_entityName VARCHAR(255),
   task_descriptionId VARCHAR(255),
   task_state VARCHAR(255),
   PRIMARY KEY ( task_id )
);
