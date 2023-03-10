/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE IF NOT EXISTS "course" (
	"course_id" VARCHAR(50) NOT NULL,
	PRIMARY KEY ("course_id")
);

CREATE TABLE IF NOT EXISTS "message" (
	"id" VARCHAR(40) NOT NULL,
	"type" VARCHAR(20) NULL DEFAULT 'NULL::character varying',
	"created_at" TIMESTAMP NULL DEFAULT NULL,
	"parent_id" CHAR(40) NULL DEFAULT 'NULL::bpchar',
	"username" VARCHAR(50) NULL DEFAULT 'NULL::character varying',
	"body" TEXT NULL DEFAULT NULL,
	"depth" SMALLINT NULL DEFAULT NULL,
	"endorsed" BOOLEAN NULL DEFAULT NULL,
	"thread_id" VARCHAR(40) NULL DEFAULT 'NULL::character varying',
	"courseware_title" VARCHAR(300) NULL DEFAULT 'NULL::character varying',
	"pinned" VARCHAR(10) NULL DEFAULT 'NULL::character varying',
	"votes_up_count" INTEGER NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "message_fk_parent" FOREIGN KEY ("parent_id") REFERENCES "message" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "message_fk_user" FOREIGN KEY ("username") REFERENCES "users" ("username") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE "newview" (
	"?column?" TEXT NULL,
	"count" BIGINT NULL
) ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS "result" (
	"username" VARCHAR(50) NOT NULL,
	"course_id" VARCHAR(50) NOT NULL,
	"grade" NUMERIC NULL DEFAULT NULL,
	"certificate_delivered" VARCHAR(10) NULL DEFAULT 'NULL::character varying',
	"certificate_eligible" VARCHAR(10) NULL DEFAULT 'NULL::character varying',
	"certificate_type" VARCHAR(10) NULL DEFAULT 'NULL::character varying',
	"level_education" VARCHAR(10) NULL DEFAULT NULL,
	"gender" VARCHAR(4) NULL DEFAULT NULL,
	"year_of_burth" VARCHAR(4) NULL DEFAULT NULL,
	"country" VARCHAR(5) NULL DEFAULT NULL,
	PRIMARY KEY ("username", "course_id"),
	CONSTRAINT "result_fk" FOREIGN KEY ("username") REFERENCES "users" ("username") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "result_fk_1" FOREIGN KEY ("course_id") REFERENCES "course" ("course_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "threads" (
	"_id" VARCHAR(24) NOT NULL,
	"title" TEXT NULL DEFAULT NULL,
	"course_id" VARCHAR(50) NULL DEFAULT 'NULL::character varying',
	"username" VARCHAR(50) NULL DEFAULT 'NULL::character varying',
	"comments_count" INTEGER NULL DEFAULT NULL,
	PRIMARY KEY ("_id"),
	CONSTRAINT "thread_fk_course" FOREIGN KEY ("course_id") REFERENCES "course" ("course_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "threads_fk_user" FOREIGN KEY ("username") REFERENCES "users" ("username") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "users" (
	"username" VARCHAR(50) NOT NULL,
	"user_id" VARCHAR(24) NULL DEFAULT 'NULL::character varying',
	"_id" VARCHAR(24) NULL DEFAULT 'NULL::character varying',
	PRIMARY KEY ("username")
);

CREATE TABLE "vue_messages_grade_titres_threads" (
	"message_id" VARCHAR(40) NULL,
	"message_type" VARCHAR(20) NULL,
	"message_created_at" TIMESTAMP NULL,
	"message_parent" CHAR(40) NULL,
	"message_depth" SMALLINT NULL,
	"message_endorsed" BOOLEAN NULL,
	"massage_body" TEXT NULL,
	"username" VARCHAR(50) NULL,
	"course_id" VARCHAR(50) NULL,
	"grade" NUMERIC NULL,
	"certificate_delivered" VARCHAR(10) NULL,
	"certificate_eligible" VARCHAR(10) NULL,
	"certificate_type" VARCHAR(10) NULL,
	"user_id_short" VARCHAR(24) NULL,
	"user_id_long" VARCHAR(24) NULL,
	"title" TEXT NULL
) ENGINE=MyISAM;

DROP TABLE IF EXISTS "newview";
CREATE VIEW "newview" AS  SELECT cl."?column?",
    cl.count
   FROM ( SELECT 'user'::text AS "?column?",
            count(*) AS count
           FROM users
        UNION
         SELECT 'course'::text AS text,
            count(*) AS count
           FROM course
        UNION
         SELECT 'result'::text AS text,
            count(*) AS count
           FROM result
        UNION
         SELECT 'fil'::text AS text,
            count(*) AS count
           FROM threads
        UNION
         SELECT 'message'::text AS text,
            count(*) AS count
           FROM message
        UNION
         SELECT 'table message'::text AS text,
            count(*) AS count
           FROM vue_messages_grade_titres_threads) cl
  ORDER BY cl.count DESC;;

DROP TABLE IF EXISTS "vue_messages_grade_titres_threads";
CREATE VIEW "vue_messages_grade_titres_threads" AS  SELECT messages_grade.message_id,
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
    threads.title
   FROM (( SELECT message.id AS message_id,
            message.type AS message_type,
            message.created_at AS message_created_at,
            message.parent_id AS message_parent,
            message.depth AS message_depth,
            message.endorsed AS message_endorsed,
            message.body AS massage_body,
            message.username,
            message.thread_id,
            message.pinned,
            message.votes_up_count,
            result.course_id,
            result.grade,
            result.certificate_delivered,
            result.certificate_eligible,
            result.certificate_type,
            users.user_id AS user_id_short,
            users._id AS user_id_long,
            result.level_education,
            result.gender,
            result.year_of_burth,
            result.country
           FROM message,
            users,
            result
          WHERE (((message.username)::text = (users.username)::text) AND ((result.username)::text = (users.username)::text))) messages_grade
     LEFT JOIN threads ON (((messages_grade.message_id)::text = (threads._id)::text)));;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
