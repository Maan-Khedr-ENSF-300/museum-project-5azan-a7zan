DROP DATABASE IF EXISTS ARTGALLERY;
CREATE DATABASE ARTGALLERY; 
USE ARTGALLERY;

CREATE TABLE ARTIST
(
  name_            	VARCHAR(100) NOT NULL,
  description_     	VARCHAR(60),
  main_style   	  	VARCHAR(30),
  Epoch	           	VARCHAR(30),
  Country_of_origin VARCHAR(20),
  Date_died		 	DATE,
  Date_born		 	DATE,
  
PRIMARY KEY (name_));


CREATE TABLE ART_OBJECTS
( ID_NO            INT   	NOT NULL,
  title            VARCHAR(20),
  description_     VARCHAR(100),
  artist           VARCHAR(100), 
  year_            INT,
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (artist) REFERENCES ARTIST(name_) ON DELETE SET NULL ON UPDATE CASCADE);


CREATE TABLE PAINTING
( ID_NO           INT  			NOT NULL,
  Paint_type      VARCHAR(20),
  Drawn_on        VARCHAR(20),
  Style           VARCHAR(20),
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE SCULPTURE
( ID_NO         INT   			NOT NULL,
  material      VARCHAR(20),
  height        DECIMAL(10,2),
  weight        DECIMAL(10,2),
  Style		    VARCHAR(20),
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE STATUE
( ID_NO         INT			   	NOT NULL,
  material      VARCHAR(20),
  height        VARCHAR(20),
  weight        VARCHAR(20),
  Style		    VARCHAR(20),
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE OTHER
( ID_NO         INT			   	NOT NULL,
  type_         VARCHAR(20),
  Style         VARCHAR(20),
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE EXHIBITIONS
( name_         VARCHAR(50),
  State_date    DATE,
  End_date      DATE,
  
PRIMARY KEY (name_));

CREATE TABLE PART_OF
( ID_NO         INT		   	NOT NULL,
  name_   	    VARCHAR(50),
  
PRIMARY KEY (name_, ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (name_) REFERENCES EXHIBITIONS(name_) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE BORROWED
( ID_NO            INT        	NOT NULL,
  From_  	       VARCHAR(40),
  Date_borrowed    DATE,
  Date_returned    DATE,
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE PERMENANT_COLLECTIONS
( ID_NO            INT   			NOT NULL,
  Date_acquired    DATE,
  Status_          CHAR(15)		    NOT NULL,
  Cost		  	   DECIMAL(10, 2),
  
PRIMARY KEY (ID_NO),
FOREIGN KEY (ID_NO) REFERENCES ART_OBJECTS(ID_NO) ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE COLLECTIONS
( name_            	VARCHAR(50)   	NOT NULL,
  Type_   	 	  	VARCHAR(20),
  Description_     	VARCHAR(100)		NOT NULL,
  Contact_person 	VARCHAR(20),
  Phone		 		VARCHAR(10),
  Address            VARCHAR(50),
  
PRIMARY KEY (name_));

INSERT INTO ARTIST
VALUES      ('Yacoub KmarEldin','Arabic man who has lived in Greek times','Geometric','Ancient','Greek','1124-01-05','1053-02-20'),
            ('Khaled Kashmery','Romantic man who has shown love through art','Figurative','Romanticism','Jordanian','1670-05-23','1580-02-13'),
            ('Khedr Karaweta','Turks of today describing art of now','Figurative','Modern','Turkish','2008-10-16','1912-03-20'),
            ('Mohamed Sombol','African master of art','Abstract','Renaissance','Sudanese','1702-08-12','1630-02-19'),
            ('Ismael Ahmed Kanabawy','Named as abo el donya and master of art','Portraiture','Ancient','Egyptian','1103-01-06','1010-10-12'),
			('Othman Abdlejalel Shesha','Arabian legend','Abstract','Romanesque','Saudi Arabian','1305-06-22','1216-07-30');
  
INSERT INTO ART_OBJECTS
VALUES      (5051,'Shapes of Freedom','Geometric shapes defining what freedom looks like','Yacoub KmarEldin',1100),
            (5253,'Modern Man','A representation of a modern man','Khedr Karaweta',1988),
            (5455,'El Hob Keda','Love described on pottery','Khaled Kashmery',1654),
            (5657,'Leaders of Now','Statue of a great leader','Ismael Ahmed Kanabawy',1074),
            (5859,'Kaas Hob','Pottery used by lovers','Khaled Kashmery',1665),
            (6061,'Suns of Gilt','Oil paintwork of stolen golden during era','Mohamed Sombol',1698),
            (6263,'Masculinity','Statue of a brave man','Othman Abdlejalel Shesha',1297),
            (6465,'Karaweta Army','Sculpture for Khedr supporters','Khedr Karaweta',1992);


INSERT INTO PAINTING
VALUES      (5051,'Oil','Paper','Geometric'),
            (6061,'Oil','Canvas','Abstract');
            
INSERT INTO SCULPTURE
VALUES      (5253,'Stone','132.24','54.65','Figurative'),
            (6465,'Stone','154.56','80.52','Figurative');
            
INSERT INTO STATUE
VALUES      (5657,'Bronze','76.21','24.21','Portaiture'),
            (6263,'Marble','187.75','65.45','Figurative');

INSERT INTO OTHER
VALUES      (5455,'Pottery','Figurative'),
            (5859,'Pottery','Abstract');
            
INSERT INTO EXHIBITIONS
VALUES      ('Art Paintings','2018-06-20','2018-07-21'),
			('Sculpture and Statues','2022-04-12','2022-06-11'),
            ('Pottery Art','2012-10-05','2013-10-06');
            
INSERT INTO PART_OF
VALUES      (5051,'Art Paintings'),
			(6061,'Art Paintings'),
            (5657,'Sculpture and Statues'),
            (6263,'Sculpture and Statues'),
            (5253,'Sculpture and Statues'),
            (6465,'Sculpture and Statues'),
            (5455,'Pottery Art'),
            (5859,'Pottery Art');

INSERT INTO BORROWED
VALUES      (5051,'Modern Antiques','2018-05-25','2018-08-12'),
			(5253,'Taylor Museum','2022-02-10','2022-08-20'),
            (5455,'John Ancient Museum','2011-12-06','2013-12-05');

INSERT INTO PERMENANT_COLLECTIONS
VALUES      (6061,'2010-05-24','On Display',54322.64),
			(5657,'2010-04-12','Stored',10343.32),
            (6263,'2013-05-05','Stored',7632.43),
            (5859,'2011-12-12','On Display',12423.45),
            (6465,'2005-06-20','On Loan',43224.22);
            
INSERT INTO COLLECTIONS
VALUES      ('Divinity in Art','Museum','Religious artwork','Essam Karara','403658784','6 Mostafa ElNahaas'),
			('Masterpiece of the Masters','Museum','Work done by the masters of the era','John McLarry','8356454875','132 Northland Ave'),
            ('Art of White Nature','Personal','White colored nature art','Natasha Bond','5879546745','5 Cuthbertson St');
            
