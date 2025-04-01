--
-- PostgreSQL database dump
--

-- Dumped from database version 13.20 (Debian 13.20-1.pgdg120+1)
-- Dumped by pg_dump version 13.20 (Debian 13.20-1.pgdg120+1)

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
-- Name: attendance; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.attendance (
    attendanceid integer NOT NULL,
    studentid integer NOT NULL,
    courseid integer NOT NULL,
    datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.attendance OWNER TO myuser;

--
-- Name: attendance_attendanceid_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.attendance_attendanceid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attendance_attendanceid_seq OWNER TO myuser;

--
-- Name: attendance_attendanceid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.attendance_attendanceid_seq OWNED BY public.attendance.attendanceid;


--
-- Name: courses; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.courses (
    courseid integer NOT NULL,
    coursename character varying(100) NOT NULL,
    instructorid integer,
    meetingdays character varying(50),
    classstarttime time without time zone,
    classendtime time without time zone
);


ALTER TABLE public.courses OWNER TO myuser;

--
-- Name: courses_courseid_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.courses_courseid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.courses_courseid_seq OWNER TO myuser;

--
-- Name: courses_courseid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.courses_courseid_seq OWNED BY public.courses.courseid;


--
-- Name: instructors; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.instructors (
    instructorid integer NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    profilepic bytea
);


ALTER TABLE public.instructors OWNER TO myuser;

--
-- Name: instructors_instructorid_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.instructors_instructorid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instructors_instructorid_seq OWNER TO myuser;

--
-- Name: instructors_instructorid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.instructors_instructorid_seq OWNED BY public.instructors.instructorid;


--
-- Name: location; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.location (
    locationid integer NOT NULL,
    buildingname character varying(50) NOT NULL,
    roomnumber character varying(10) NOT NULL
);


ALTER TABLE public.location OWNER TO myuser;

--
-- Name: location_locationid_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.location_locationid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.location_locationid_seq OWNER TO myuser;

--
-- Name: location_locationid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.location_locationid_seq OWNED BY public.location.locationid;


--
-- Name: meetingdays; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.meetingdays (
    meetingdayid integer NOT NULL,
    dayname character varying(20) NOT NULL
);


ALTER TABLE public.meetingdays OWNER TO myuser;

--
-- Name: meetingdays_meetingdayid_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.meetingdays_meetingdayid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meetingdays_meetingdayid_seq OWNER TO myuser;

--
-- Name: meetingdays_meetingdayid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.meetingdays_meetingdayid_seq OWNED BY public.meetingdays.meetingdayid;


--
-- Name: studentcourses; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.studentcourses (
    studentid integer NOT NULL,
    courseid integer NOT NULL
);


ALTER TABLE public.studentcourses OWNER TO myuser;

--
-- Name: students; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.students (
    studentid integer NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    profilepic bytea
);


ALTER TABLE public.students OWNER TO myuser;

--
-- Name: students_studentid_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.students_studentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.students_studentid_seq OWNER TO myuser;

--
-- Name: students_studentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.students_studentid_seq OWNED BY public.students.studentid;


--
-- Name: attendance attendanceid; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.attendance ALTER COLUMN attendanceid SET DEFAULT nextval('public.attendance_attendanceid_seq'::regclass);


--
-- Name: courses courseid; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.courses ALTER COLUMN courseid SET DEFAULT nextval('public.courses_courseid_seq'::regclass);


--
-- Name: instructors instructorid; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.instructors ALTER COLUMN instructorid SET DEFAULT nextval('public.instructors_instructorid_seq'::regclass);


--
-- Name: location locationid; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.location ALTER COLUMN locationid SET DEFAULT nextval('public.location_locationid_seq'::regclass);


--
-- Name: meetingdays meetingdayid; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.meetingdays ALTER COLUMN meetingdayid SET DEFAULT nextval('public.meetingdays_meetingdayid_seq'::regclass);


--
-- Name: students studentid; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students ALTER COLUMN studentid SET DEFAULT nextval('public.students_studentid_seq'::regclass);


--
-- Data for Name: attendance; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.attendance (attendanceid, studentid, courseid, datetime) FROM stdin;
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.courses (courseid, coursename, instructorid, meetingdays, classstarttime, classendtime) FROM stdin;
\.


--
-- Data for Name: instructors; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.instructors (instructorid, firstname, lastname, profilepic) FROM stdin;
\.


--
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.location (locationid, buildingname, roomnumber) FROM stdin;
\.


--
-- Data for Name: meetingdays; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.meetingdays (meetingdayid, dayname) FROM stdin;
\.


--
-- Data for Name: studentcourses; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.studentcourses (studentid, courseid) FROM stdin;
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.students (studentid, firstname, lastname, profilepic) FROM stdin;
\.


--
-- Name: attendance_attendanceid_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.attendance_attendanceid_seq', 1, false);


--
-- Name: courses_courseid_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.courses_courseid_seq', 1, false);


--
-- Name: instructors_instructorid_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.instructors_instructorid_seq', 1, false);


--
-- Name: location_locationid_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.location_locationid_seq', 1, false);


--
-- Name: meetingdays_meetingdayid_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.meetingdays_meetingdayid_seq', 1, false);


--
-- Name: students_studentid_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.students_studentid_seq', 1, false);


--
-- Name: attendance attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_pkey PRIMARY KEY (attendanceid);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (courseid);


--
-- Name: instructors instructors_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_pkey PRIMARY KEY (instructorid);


--
-- Name: location location_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_pkey PRIMARY KEY (locationid);


--
-- Name: meetingdays meetingdays_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.meetingdays
    ADD CONSTRAINT meetingdays_pkey PRIMARY KEY (meetingdayid);


--
-- Name: studentcourses studentcourses_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.studentcourses
    ADD CONSTRAINT studentcourses_pkey PRIMARY KEY (studentid, courseid);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (studentid);


--
-- Name: courses courses_instructorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_instructorid_fkey FOREIGN KEY (instructorid) REFERENCES public.instructors(instructorid);


--
-- Name: studentcourses fk_course; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.studentcourses
    ADD CONSTRAINT fk_course FOREIGN KEY (courseid) REFERENCES public.courses(courseid) ON DELETE CASCADE;


--
-- Name: attendance fk_course_attendance; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT fk_course_attendance FOREIGN KEY (courseid) REFERENCES public.courses(courseid) ON DELETE CASCADE;


--
-- Name: studentcourses fk_student; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.studentcourses
    ADD CONSTRAINT fk_student FOREIGN KEY (studentid) REFERENCES public.students(studentid) ON DELETE CASCADE;


--
-- Name: attendance fk_student_attendance; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT fk_student_attendance FOREIGN KEY (studentid) REFERENCES public.students(studentid) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

