
USE ARTGALLERY;

/*Showing all tables*/
/*

*/
select *
 From ARTIST;

select *
 From ART_OBJECTS;

select *
 From PAINTING;

select *
 From SCULPTURE;

select *
 From STATUE;
 
select *
 From OTHER;

select *
 From EXHIBITIONS;

select *
 From BORROWED;

select *
 From PERMENANT_COLLECTIONS;
 
select *
 From COLLECTIONS;

select *
 From PART_OF;
 
 

 

/*A basic retrieval query to find a record using a title*/
select *
 From art_objects
 where title = 'Modern Man';



/*A retrieval query with ordered results by years ascending*/
select title,year_
 from art_objects
 order by year_ asc;


/*a ested query to find the largest year recorded for an art object*/ 
select title,year_
 from art_objects
 where year_=(select max(year_) from art_objects);




/*a query that uses 2 tables to find the correlating records between them and display the title,description and paint type*/
select x.title,x.description_,y.Paint_type
 from art_objects as x
 inner JOIN painting as y on x.ID_NO=y.ID_NO;


/*a query updates a specific year of a certain record by use of the primary key*/
update art_objects
 set year_ = 2300
 where ID_NO = 5051;


/*a query deletes a record*/
delete from art_objects where ID_NO = 6061;
