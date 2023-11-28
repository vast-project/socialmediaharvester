--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Ubuntu 15.1-1.pgdg22.10+1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg22.10+1)

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

--
-- Name: socialcampaigns; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA socialcampaigns;


ALTER SCHEMA socialcampaigns OWNER TO postgres;

--
-- Name: dstatus; Type: DOMAIN; Schema: socialcampaigns; Owner: postgres
--

CREATE DOMAIN socialcampaigns.dstatus AS text
	CONSTRAINT dstatus_check CHECK (((VALUE)::text = ANY ((ARRAY['Created'::text, 'Scheduled'::text, 'Published'::text, 'Deleted'::text])::text[])));


ALTER DOMAIN socialcampaigns.dstatus OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: socialcampaigns; Owner: postgres
--

CREATE SEQUENCE socialcampaigns.answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialcampaigns.answer_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.answer (
    id int DEFAULT nextval('socialcampaigns.answer_id_seq'::regclass) NOT NULL,
    post int,
    content text,
    author text,
    id_on_network text,
    publication_date date,
    reply_to int
);


ALTER TABLE socialcampaigns.answer OWNER TO postgres;

--
-- Name: appuser; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.appuser (
    username text NOT NULL,
    password text NOT NULL,
    is_active boolean DEFAULT true
    -- CONSTRAINT appuser_password_check CHECK ((length(password) > 7))
);


ALTER TABLE socialcampaigns.appuser OWNER TO postgres;

--
-- Name: identity; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.identity (
    s_network int NOT NULL,
    appuser text NOT NULL,
    id_on_network text
);


ALTER TABLE socialcampaigns.identity OWNER TO postgres;

--
-- Name: image_id_seq; Type: SEQUENCE; Schema: socialcampaigns; Owner: postgres
--

CREATE SEQUENCE socialcampaigns.image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialcampaigns.image_id_seq OWNER TO postgres;

--
-- Name: image; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.image (
    id int DEFAULT nextval('socialcampaigns.image_id_seq'::regclass) NOT NULL,
    path text,
    post int,
    id_on_network text
);


ALTER TABLE socialcampaigns.image OWNER TO postgres;

--
-- Name: items_id_seq; Type: SEQUENCE; Schema: socialcampaigns; Owner: postgres
--

CREATE SEQUENCE socialcampaigns.items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialcampaigns.items_id_seq OWNER TO postgres;

--
-- Name: post_id_seq; Type: SEQUENCE; Schema: socialcampaigns; Owner: postgres
--

CREATE SEQUENCE socialcampaigns.post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialcampaigns.post_id_seq OWNER TO postgres;

--
-- Name: post; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.post (
    id int DEFAULT nextval('socialcampaigns.post_id_seq'::regclass) NOT NULL,
    s_network int,
    id_on_network text,
    content text,
    creation_date date,
    scheduling_date date,
    publication_date date,
    author text,
    status int
);


ALTER TABLE socialcampaigns.post OWNER TO postgres;

--
-- Name: setting; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.setting (
    s_network int NOT NULL,
    appuser text NOT NULL,
    key text NOT NULL,
    value text
);


ALTER TABLE socialcampaigns.setting OWNER TO postgres;

--
-- Name: social_network_id_seq; Type: SEQUENCE; Schema: socialcampaigns; Owner: postgres
--

CREATE SEQUENCE socialcampaigns.social_network_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialcampaigns.social_network_id_seq OWNER TO postgres;

--
-- Name: social_network; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.social_network (
    id int DEFAULT nextval('socialcampaigns.social_network_id_seq'::regclass) NOT NULL,
    s_name text NOT NULL
);


ALTER TABLE socialcampaigns.social_network OWNER TO postgres;

--
-- Name: status_id_seq; Type: SEQUENCE; Schema: socialcampaigns; Owner: postgres
--

CREATE SEQUENCE socialcampaigns.status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialcampaigns.status_id_seq OWNER TO postgres;

--
-- Name: status; Type: TABLE; Schema: socialcampaigns; Owner: postgres
--

CREATE TABLE socialcampaigns.status (
    id int DEFAULT nextval('socialcampaigns.status_id_seq'::regclass) NOT NULL,
    status_name socialcampaigns.dstatus NOT NULL
);


ALTER TABLE socialcampaigns.status OWNER TO postgres;

--
-- Name: appuser appuser_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.appuser
    ADD CONSTRAINT appuser_pkey PRIMARY KEY (username);


--
-- Name: identity identity_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.identity
    ADD CONSTRAINT identity_pkey PRIMARY KEY (s_network, appuser);


--
-- Name: image image_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.image
    ADD CONSTRAINT image_pkey PRIMARY KEY (id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: setting setting_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.setting
    ADD CONSTRAINT setting_pkey PRIMARY KEY (s_network, appuser, key);


--
-- Name: social_network social_network_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.social_network
    ADD CONSTRAINT social_network_pkey PRIMARY KEY (id);


--
-- Name: status status_pkey; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id);


--
-- Name: status status_status_name_key; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.status
    ADD CONSTRAINT status_status_name_key UNIQUE (status_name);


--
-- Name: social_network unique_s_name; Type: CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.social_network
    ADD CONSTRAINT unique_s_name UNIQUE (s_name);


--
-- Name: ix_socialcampaigns_image_id; Type: INDEX; Schema: socialcampaigns; Owner: postgres
--

CREATE INDEX ix_socialcampaigns_image_id ON socialcampaigns.image USING btree (id);


--
-- Name: ix_socialcampaigns_post_id; Type: INDEX; Schema: socialcampaigns; Owner: postgres
--

CREATE INDEX ix_socialcampaigns_post_id ON socialcampaigns.post USING btree (id);


--
-- Name: identity identity_appuser_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.identity
    ADD CONSTRAINT identity_appuser_fkey FOREIGN KEY (appuser) REFERENCES socialcampaigns.appuser(username);


--
-- Name: identity identity_s_network_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.identity
    ADD CONSTRAINT identity_s_network_fkey FOREIGN KEY (s_network) REFERENCES socialcampaigns.social_network(id);


--
-- Name: image image_post_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.image
    ADD CONSTRAINT image_post_fkey FOREIGN KEY (post) REFERENCES socialcampaigns.post(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: post post_s_network_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.post
    ADD CONSTRAINT post_s_network_fkey FOREIGN KEY (s_network) REFERENCES socialcampaigns.social_network(id);

ALTER TABLE ONLY socialcampaigns.post
    ADD CONSTRAINT post_author_fkey FOREIGN KEY (author) REFERENCES socialcampaigns.appuser(username);


--
-- Name: post post_status_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.post
    ADD CONSTRAINT post_status_fkey FOREIGN KEY (status) REFERENCES socialcampaigns.status(id);

--
-- Name: setting setting_appuser_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.setting
    ADD CONSTRAINT setting_appuser_fkey FOREIGN KEY (appuser) REFERENCES socialcampaigns.appuser(username);


--
-- Name: setting setting_s_network_fkey; Type: FK CONSTRAINT; Schema: socialcampaigns; Owner: postgres
--

ALTER TABLE ONLY socialcampaigns.setting
    ADD CONSTRAINT setting_s_network_fkey FOREIGN KEY (s_network) REFERENCES socialcampaigns.social_network(id);


--
-- PostgreSQL database dump complete
--

