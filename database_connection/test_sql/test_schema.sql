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

CREATE TABLE "category" (
	`category_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`importance`	REAL
);

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

CREATE TABLE "t_unit" (
	`t_unit_Id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`article_id`	INTEGER,
	`sentence`	TEXT NOT NULL,
	`url`	TEXT,
	`access_timestamp`	NUMERIC,
	`lat`	REAL,
	`long`	REAL,
	`num_likes`	INTEGER,
	`num_mehs`	INTEGER,
	`num_dislikes`	INTEGER,
	FOREIGN KEY(`article_id`) REFERENCES `article`(`article_id`) ON DELETE SET NULL
);