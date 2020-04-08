INSERT INTO article (article_id, title)
VALUES (0, 'a'),
       (1, 'b'),
       (2, 'c'),
       (3, 'd'),
       (4, 'e'),
       (5, 'f'),
       (6, 'g'),
       (7, 'h'),
       (8, 'i'),
       (9, 'j');

INSERT INTO category (category_id, name, importance)
VALUES (0, 'category_a', 1),
       (1, 'category_b', 0),
       (2, 'category_c', 0.5);

INSERT INTO article_category (article_id, category_id)
VALUES (0, 0),
       (0, 1),
       (0, 2),
       (1, 1),
       (2, 2);

INSERT INTO user
VALUES (0, 'Jill', 'jill@email.com', 'pass1', 5, 5, 10, 5),
       (1, 'Jack', 'jack@email.com', 'pass2', 7, 7, 14, 7);

INSERT INTO t_unit
VALUES (0, 0, 'sentence_a', 'url', 1234, 30, 30, 0, 0, 0),
       (1, 1, 'sentence_b', 'url', 1234, 30.25, 30.25, 1, 1, 1),
       (2, 2, 'sentence_c', 'url', 1234, -30, 30, 2, 2, 2),
       (3, 3, 'sentence_d', 'url', 1234, 10, 10, 3, 3, 3);

