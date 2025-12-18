create temporary table products_to_delete (
    product_id int primary key, name varchar(250), rownum int, url text
);  

insert into products_to_delete 
select p.product_id, p.name as name, row_number() over (partition by name order by o.url), o.url as url from products as p 
join offers as o on o.product_id = p.product_id;

delete from products_to_delete 
where rownum = 1;

delete from products 
where product_id in (select product_id from products_to_delete);  

drop temporary table products_to_delete;