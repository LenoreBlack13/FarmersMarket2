CREATE DATABASE farmersmarkets
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	
CREATE TABLE IF NOT EXISTS public.reviews
(
    reviewid integer NOT NULL DEFAULT nextval('reviews_reviewid_seq'::regclass),
    marketid character(10) COLLATE pg_catalog."default",
    userid integer,
    reviewtext text COLLATE pg_catalog."default",
    rating integer,
    reviewdate timestamp without time zone DEFAULT now(),
    CONSTRAINT reviews_pkey PRIMARY KEY (reviewid),
    CONSTRAINT reviews_marketid_fkey FOREIGN KEY (marketid)
        REFERENCES public.markets (fmid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT reviews_userid_fkey FOREIGN KEY (userid)
        REFERENCES public.users (userid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT reviews_rating_check CHECK (rating >= 1 AND rating <= 5)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.reviews
    OWNER to postgres;
	
CREATE TABLE IF NOT EXISTS public.users
(
    userid integer NOT NULL DEFAULT nextval('users_userid_seq'::regclass),
    firstname character varying(255) COLLATE pg_catalog."default",
    lastname character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (userid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;