INSERT INTO article (article_id, title, lat, long)
VALUES (1, 'a', 18.1, -66.7),
       (2, 'b', 30.0, 30.25),
       (3, 'c', -1.0, 30.0),
       (4, 'd', -1.0, 30.25),
       (5, 'e', NULL, NULL),
       (6, 'f', NULL, NULL),
       (7, 'g', NULL, NULL),
       (8, 'h', NULL, NULL),
       (9, 'i', NULL, NULL),
       (10, 'j', NULL, NULL);

INSERT INTO category (category_id, name, importance)
VALUES (1, 'category_a', 1),
       (2, 'category_b', 0),
       (3, 'category_c', 0.5);

INSERT INTO article_category (article_id, category_id)
VALUES (1, 1),
       (1, 2),
       (1, 3),
       (2, 1),
       (3, 2);

INSERT INTO user
VALUES (1, 'Jill', 'jill@email.com', 'pass1', 5, 5, 10, 5),
       (2, 'Jack', 'jack@email.com', 'pass2', 7, 7, 14, 7);

INSERT INTO t_unit
VALUES (1, 1, 'sentence_a', 'url', 1234, 18.1, -66.7, 0, 0, 0),
       (2, 2, 'sentence_b', 'url', 1234, 30.0, 30.25, 1, 1, 1),
       (3, 3, 'sentence_c', 'url', 1234, -1.0, 30.0, 2, 2, 2),
       (4, 4, 'sentence_d', 'url', 1234, -1.0, 30.25, 3, 3, 3);

INSERT INTO location (zip, lat, long)
VALUES ('00601', 18.180555, -66.749961)

