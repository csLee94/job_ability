
        
CREATE TABLE Code_details
(
  code_parent  varchar(10)  NOT NULL,
  code_details varchar(5)   NOT NULL,
  name_details varchar(255) NULL    ,
  PRIMARY KEY (code_details)
);

CREATE TABLE Code_parent
(
  code_parent varchar(10)  NOT NULL,
  name_parent varchar(255) NULL    ,
  PRIMARY KEY (code_parent)
);

CREATE TABLE Fail_Crawling
(
  code_d      varchar(5)  NULL    ,
  ID_num      varchar(10) NULL    ,
  url         varchar(50) NULL    ,
  Company_nm  text        NULL    ,
  Flyer_title text        NULL    ,
  time        DATETIME    NULL    
);

CREATE TABLE Flyers
(
  code_details varchar(5)   NULL    ,
  ID_num       varchar(10)  NULL    ,
  Maintask     varchar(255) NULL    ,
  Qual         varchar(255) NULL    ,
  Pre_Qual     varchar(255) NULL    ,
  Company_nm   text         NULL    ,
  Flyer_title  text         NULL    
);

CREATE TABLE Words
(
  code_details varchar(5)  NULL    ,
  word         varchar(30) NULL    
);

ALTER TABLE Code_details
  ADD CONSTRAINT FK_Code_parent_TO_Code_details
    FOREIGN KEY (code_parent)
    REFERENCES Code_parent (code_parent);

ALTER TABLE Flyers
  ADD CONSTRAINT FK_Code_details_TO_Flyers
    FOREIGN KEY (code_details)
    REFERENCES Code_details (code_details);

ALTER TABLE Words
  ADD CONSTRAINT FK_Code_details_TO_Words
    FOREIGN KEY (code_details)
    REFERENCES Code_details (code_details);

      