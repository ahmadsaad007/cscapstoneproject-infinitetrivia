CREATE TABLE `article` (
	`article_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`title`	TEXT NOT NULL
);

CREATE TABLE "article_category" (
	`article_id`	INTEGER,
	`category_id`	INTEGER,
	PRIMARY KEY(`article_id`,`category_id`),
	FOREIGN KEY(`category_id`) REFERENCES `category`(`category_id`) ON DELETE SET NULL,
	FOREIGN KEY(`article_id`) REFERENCES `article`(`article_id`) ON DELETE SET NULL
);

CREATE TABLE "category" (
	`category_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`importance`	REAL
);

CREATE TABLE "question" (
	"qu_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"t_unit_id"	INTEGER NOT NULL,
	"text"	TEXT NOT NULL UNIQUE,
	"answer"	TEXT,
	FOREIGN KEY("t_unit_id") REFERENCES "t_unit"("t_unit_Id") ON DELETE CASCADE
);

CREATE TABLE "t_unit" (
	`t_unit_Id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`article_id`	INTEGER,
	`sentence`	TEXT NOT NULL,
	`rank`	INTEGER,
	`url`	TEXT,
	`access_timestamp`	NUMERIC,
	`lat`	REAL,
	`long`	REAL,
	`has_superlative`	NUMERIC,
	`has_contrasting`	NUMERIC,
	`root_word`	TEXT,
	`subj_word`	TEXT,
	`readability`	INTEGER,
	FOREIGN KEY(`article_id`) REFERENCES `article`(`article_id`) ON DELETE SET NULL
);

CREATE TABLE "user" (
	"user_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"username"	TEXT UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT,
	"wins"	INTEGER,
	"losses"	INTEGER,
	"num_answered"	INTEGER,
	"num_answered_correct"	INTEGER
);

CREATE TABLE "votes_on" (
	"user_id"	INTEGER NOT NULL,
	"q_id"	INTEGER NOT NULL,
	"interesting_rating"	INTEGER,
	"question_rating"	INTEGER,
	PRIMARY KEY("user_id","q_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id") ON DELETE CASCADE,
	FOREIGN KEY("q_id") REFERENCES "question"("qu_id") ON DELETE CASCADE
);

CREATE INDEX "user_username_ix" ON "user" (
	"username"
);

