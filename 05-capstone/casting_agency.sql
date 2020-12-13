--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    gender character varying
);


ALTER TABLE public.actors OWNER TO app_user;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: app_user
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO app_user;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_user
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO app_user;

--
-- Name: cast; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public."cast" (
    id integer NOT NULL,
    movie_id integer,
    actor_id integer
);


ALTER TABLE public."cast" OWNER TO app_user;

--
-- Name: cast_id_seq; Type: SEQUENCE; Schema: public; Owner: app_user
--

CREATE SEQUENCE public.cast_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cast_id_seq OWNER TO app_user;

--
-- Name: cast_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_user
--

ALTER SEQUENCE public.cast_id_seq OWNED BY public."cast".id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: app_user
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    release_date date NOT NULL
);


ALTER TABLE public.movies OWNER TO app_user;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: app_user
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO app_user;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_user
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: cast id; Type: DEFAULT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public."cast" ALTER COLUMN id SET DEFAULT nextval('public.cast_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public.actors (id, name, gender) FROM stdin;
1	Tom Hanks	male
2	Antonio Banderas	male
3	Scarlett Johansson	female
4	Joaquin Phoenix	male
5	Brad Pitt	male
6	Margot Robbie	male
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public.alembic_version (version_num) FROM stdin;
fb4edceedf6f
\.


--
-- Data for Name: cast; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public."cast" (id, movie_id, actor_id) FROM stdin;
1	1	6
2	1	5
3	2	2
4	3	3
5	4	4
6	5	6
7	6	1
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: app_user
--

COPY public.movies (id, title, release_date) FROM stdin;
1	Once Upon a Time in Hollywood	2020-01-01
2	Pain and Glory	2019-03-22
3	Marriage Story	2019-11-06
4	Joker	2019-10-04
5	I, Tonya	2017-12-08
6	Philadelphia	1993-12-22
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_user
--

SELECT pg_catalog.setval('public.actors_id_seq', 6, true);


--
-- Name: cast_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_user
--

SELECT pg_catalog.setval('public.cast_id_seq', 7, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app_user
--

SELECT pg_catalog.setval('public.movies_id_seq', 6, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cast cast_pkey; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public."cast"
    ADD CONSTRAINT cast_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: cast cast_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public."cast"
    ADD CONSTRAINT cast_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id) ON DELETE CASCADE;


--
-- Name: cast cast_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: app_user
--

ALTER TABLE ONLY public."cast"
    ADD CONSTRAINT cast_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--
