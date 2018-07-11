CREATE TABLE IF NOT EXISTS projects (
    id integer PRIMARY KEY,
    name text NOT NULL,
    url text NOT NULL,
    like text NOT NULL,
    dislike integer NOT NULL
);
 
