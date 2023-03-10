-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';
-- public."User" definition

-- Drop table

-- DROP TABLE public."User";

CREATE TABLE public."User" (
	username varchar(50) NOT NULL,
	user_id varchar(24) NULL,
	"_id" varchar(24) NULL,
	CONSTRAINT user_pk PRIMARY KEY (username)
);


-- public.course definition

-- Drop table

-- DROP TABLE public.course;

CREATE TABLE public.course (
	course_id varchar(50) NOT NULL,
	CONSTRAINT course_pk PRIMARY KEY (course_id)
);


-- public.table_messages_grade_titres_20000_threads definition

-- Drop table

-- DROP TABLE public.table_messages_grade_titres_20000_threads;

CREATE TABLE public.table_messages_grade_titres_20000_threads (
	message_id varchar(24) NOT NULL,
	message_type varchar(20) NULL,
	message_created_at timestamp NULL,
	message_parent bpchar(24) NULL,
	message_depth int2 NULL,
	message_endorsed bool NULL,
	massage_body text NULL,
	username varchar(50) NULL,
	course_id varchar(50) NULL,
	grade numeric NULL,
	certificate_delivered varchar(10) NULL,
	certificate_eligible varchar(10) NULL,
	certificate_type varchar(10) NULL,
	user_id_short varchar(24) NULL,
	user_id_long varchar(24) NULL,
	title text NULL
);
CREATE INDEX table_messages_grade_titres_20000_threads_certificate_delivered ON public.table_messages_grade_titres_20000_threads USING btree (certificate_delivered, certificate_eligible, certificate_type);
CREATE INDEX table_messages_grade_titres_20000_threads_course_id_idx ON public.table_messages_grade_titres_20000_threads USING btree (course_id);
CREATE INDEX table_messages_grade_titres_20000_threads_grade_idx ON public.table_messages_grade_titres_20000_threads USING btree (grade);
CREATE INDEX table_messages_grade_titres_20000_threads_message_created_at_id ON public.table_messages_grade_titres_20000_threads USING btree (message_created_at);
CREATE INDEX table_messages_grade_titres_20000_threads_message_depth_idx ON public.table_messages_grade_titres_20000_threads USING btree (message_depth);
CREATE INDEX table_messages_grade_titres_20000_threads_message_endorsed_idx ON public.table_messages_grade_titres_20000_threads USING btree (message_endorsed);
CREATE INDEX table_messages_grade_titres_20000_threads_message_id_idx ON public.table_messages_grade_titres_20000_threads USING btree (message_id);
CREATE INDEX table_messages_grade_titres_20000_threads_message_parent_idx ON public.table_messages_grade_titres_20000_threads USING btree (message_parent);
CREATE INDEX table_messages_grade_titres_20000_threads_message_type_idx ON public.table_messages_grade_titres_20000_threads USING btree (message_type);
CREATE INDEX table_messages_grade_titres_20000_threads_title_idx ON public.table_messages_grade_titres_20000_threads USING btree (title);
CREATE INDEX table_messages_grade_titres_20000_threads_username_idx ON public.table_messages_grade_titres_20000_threads USING btree (username);


-- public."Result" definition

-- Drop table

-- DROP TABLE public."Result";

CREATE TABLE public."Result" (
	username varchar(50) NOT NULL,
	course_id varchar(50) NOT NULL,
	grade numeric NULL,
	certificate_delivered varchar(10) NULL,
	certificate_eligible varchar(10) NULL,
	certificate_type varchar(10) NULL,
	CONSTRAINT result_pk PRIMARY KEY (username, course_id),
	CONSTRAINT result_fk FOREIGN KEY (username) REFERENCES public."User"(username),
	CONSTRAINT result_fk_1 FOREIGN KEY (course_id) REFERENCES public.course(course_id)
);


-- public."Threads" definition

-- Drop table

-- DROP TABLE public."Threads";

CREATE TABLE public."Threads" (
	"_id" varchar(24) NOT NULL,
	title text NULL,
	course_id varchar(50) NULL,
	username varchar(50) NULL,
	CONSTRAINT thread_pk PRIMARY KEY (_id),
	CONSTRAINT thread_fk_course FOREIGN KEY (course_id) REFERENCES public.course(course_id),
	CONSTRAINT threads_fk_user FOREIGN KEY (username) REFERENCES public."User"(username)
);


-- public.message definition

-- Drop table

-- DROP TABLE public.message;

CREATE TABLE public.message (
	id varchar(24) NOT NULL,
	"type" varchar(20) NULL,
	created_at timestamp NULL,
	parent_id bpchar(24) NULL,
	username varchar(50) NULL,
	body text NULL,
	"depth" int2 NULL,
	endorsed bool NULL,
	CONSTRAINT message_pk PRIMARY KEY (id),
	CONSTRAINT message_fk_parent FOREIGN KEY (parent_id) REFERENCES public.message(id),
	CONSTRAINT message_fk_user FOREIGN KEY (username) REFERENCES public."User"(username)
);


-- public.vue_messages_grade_titres_threads source

CREATE OR REPLACE VIEW public.vue_messages_grade_titres_threads
AS SELECT messages_grade.message_id,
    messages_grade.message_type,
    messages_grade.message_created_at,
    messages_grade.message_parent,
    messages_grade.message_depth,
    messages_grade.message_endorsed,
    messages_grade.massage_body,
    messages_grade.username,
    messages_grade.course_id,
    messages_grade.grade,
    messages_grade.certificate_delivered,
    messages_grade.certificate_eligible,
    messages_grade.certificate_type,
    messages_grade.user_id_short,
    messages_grade.user_id_long,
    "Threads".title
   FROM ( SELECT message.id AS message_id,
            message.type AS message_type,
            message.created_at AS message_created_at,
            message.parent_id AS message_parent,
            message.depth AS message_depth,
            message.endorsed AS message_endorsed,
            message.body AS massage_body,
            message.username,
            "Result".course_id,
            "Result".grade,
            "Result".certificate_delivered,
            "Result".certificate_eligible,
            "Result".certificate_type,
            "User".user_id AS user_id_short,
            "User"._id AS user_id_long
           FROM message,
            "User",
            "Result"
          WHERE message.username::text = "User".username::text AND "Result".username::text = "User".username::text) messages_grade
     LEFT JOIN "Threads" ON messages_grade.message_id::text = "Threads"._id::text;


-- public.vue_peuplement_tables source

CREATE OR REPLACE VIEW public.vue_peuplement_tables
AS SELECT cl."?column?",
    cl.count
   FROM ( SELECT 'user'::text AS "?column?",
            count(*) AS count
           FROM "User"
        UNION
         SELECT 'course'::text,
            count(*) AS count
           FROM course
        UNION
         SELECT 'Result'::text,
            count(*) AS count
           FROM "Result"
        UNION
         SELECT 'Fil'::text,
            count(*) AS count
           FROM "Threads"
        UNION
         SELECT 'message'::text,
            count(*) AS count
           FROM message
        UNION
         SELECT 'table message'::text,
            count(*) AS count
           FROM vue_messages_grade_titres_threads) cl
  ORDER BY cl.count DESC;

