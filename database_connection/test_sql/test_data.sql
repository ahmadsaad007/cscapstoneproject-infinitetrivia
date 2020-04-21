INSERT INTO article (article_id, title)
VALUES (1, 'a'),
       (2, 'b'),
       (3, 'c'),
       (4, 'd'),
       (5, 'e'),
       (6, 'f'),
       (7, 'g'),
       (8, 'h'),
       (9, 'i'),
       (10, 'j');

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
VALUES (1, 1, 'sentence_a', 'url', 1234, 30.0, 30.0, 0, 0, 0),
       (2, 2, 'sentence_b', 'url', 1234, 30.0, 30.25, 1, 1, 1),
       (3, 3, 'sentence_c', 'url', 1234, -1.0, 30.0, 2, 2, 2),
       (4, 4, 'sentence_d', 'url', 1234, -1.0, 30.25, 3, 3, 3);

