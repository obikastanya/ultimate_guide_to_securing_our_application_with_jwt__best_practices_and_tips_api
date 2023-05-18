-- create database
create database jwt_best_practices;

-- Create Tables
CREATE TABLE IF NOT EXISTS public.permission
(
    id character varying(200) NOT NULL,
    description character varying(250) NOT NULL,
    CONSTRAINT permission_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.role
(
    id character varying(100) NOT NULL,
    description character varying(250)  NOT NULL,
    CONSTRAINT role_fkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.role_permission
(
    role_id character varying(100) NOT NULL,
    permission_id character varying(200) NOT NULL,
    CONSTRAINT role_permission_pkey PRIMARY KEY (role_id, permission_id),
    CONSTRAINT role_permission_permission_id_fkey FOREIGN KEY (permission_id)
        REFERENCES public.permission (id),
    CONSTRAINT role_permission_role_id_fkey FOREIGN KEY (role_id)
        REFERENCES public.role (id) 
)

CREATE TABLE IF NOT EXISTS public.user
(
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(250) NOT NULL,
    role_id character varying(100) NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (id),
    CONSTRAINT user_username_key UNIQUE (username),
    CONSTRAINT role_fkey FOREIGN KEY (role_id)
        REFERENCES public.role (id) 
)

CREATE TABLE IF NOT EXISTS public.revoked_token
(
    access_token character varying(250) NOT NULL,
    expired_at timestamp with time zone NOT NULL,
    CONSTRAINT revoked_token_pkey PRIMARY KEY (access_token)
)


CREATE TABLE IF NOT EXISTS public.product
(
    id integer,
    title character varying(200),
    description character varying(500),
    price integer,
    discountpercentage numeric(2,0),
    rating numeric(1,0),
    stock integer,
    brand character varying(100),
    category character varying(100)
)


-- Insert Data

INSERT INTO public.permission(
	id, description
) VALUES 
('product:view', 'View Product'),
('product:create', 'Create Product'),
('product:update', 'Update Product'),
('product:delete', 'Delete Product'),
('revoked_token:delete', 'Delete Revoked Token');


INSERT INTO public.role(
    id, description
) VALUES 
('admin', 'Admin'),
('cron', 'Cron Job'),
('user', 'User');

INSERT INTO public.role_permission(
	role_id, permission_id
    ) VALUES 
('admin', 'product:create'),
('admin', 'product:delete'),
('admin', 'product:view'),
('admin', 'product:update'),
('cron', 'revoked_token:delete'),
('user', 'product:view');

-- password: 1234567
INSERT INTO public.user(
	id, name, username, password, role_id
    ) VALUES 
(1, 'Super Admin', 'admin', E'\$2b$12$tBwZV/IzU8ROsKl1RuwJWuUeovig0zEU/lL1aIoKJZ/mgXmYrjmHu', 'admin'),
(2, 'User', 'user', E'\$2b$12$tBwZV/IzU8ROsKl1RuwJWuUeovig0zEU/lL1aIoKJZ/mgXmYrjmHu', 'user'),
(3, 'Cron Job', 'cron', E'\$2b$12$tBwZV/IzU8ROsKl1RuwJWuUeovig0zEU/lL1aIoKJZ/mgXmYrjmHu', 'cron');


INSERT INTO public.product(
  id, title, description, price, 
  discountpercentage, rating, stock, 
  brand, category
) 
VALUES (
    1, 'Samsung Universe 9',  'Samsungs new variant which goes beyond Galaxy to the Universe', 
    1249, 15.46, 4.09, 36, 'Samsung', 'smartphones'
),
(
    1, 'iPhone 9', 'An apple mobile which is nothing like apple',
    549, 12.96, 4.69, 94, 'Apple', 'smartphones'
);

