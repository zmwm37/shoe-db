DROP TABLE IF EXISTS shoe_links;
/*DROP TABLE IF EXISTS interactions;*/

CREATE TABLE shoe_links (
    shoe_id1 varchar(50) NOT NULL,
    shoe_id2 varchar(50) NOT NULL,
    weight integer);

/*CREATE TABLE interactions (
    user_id varchar(50) NOT NULL,
    shoe_id varchar(10) NOT NULL,
    rec_date date NOT NULL,
    add_rec boolean,
    add_rec_date date,
    delete_rec boolean,
    delete_rec_date date
); */

