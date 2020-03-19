import sqlite3

def insert_categories():
    db = sqlite3.connect('itdb.db')

    with open('ranked-categories.tsv', 'r') as f:
        for line in f.read().splitlines():


            category_name, importance = line.split('\t')
            if importance == '-Infinity':
                importance = -1.0
            else:
                importance = float(importance)

            try:
                print(f'Inserting {category_name}...')
                cursor = db.cursor()
                cursor.execute('''INSERT INTO category(name, importance) VALUES (?, ?);''', [category_name, importance])
                # Commit the change
                db.commit()
            # Catch the exception
            except Exception as e:
                # Roll back any change if something goes wrong
                db.rollback()
                print(e)

    db.close()

def insert_articles():
    db = sqlite3.connect('itdb.db')
    
    with open('page2cat.tsv', 'r') as f:
        for line in f.read().splitlines():
            line_split = line.split('\t')
            article_name, article_categories = line_split[0], line_split[1:]

            try:
                print(f'Inserting {article_name}...')
                cursor = db.cursor()
                cursor.execute('''INSERT INTO article(title) VALUES (?);''', [article_name])
                cursor.execute('''SELECT article_id FROM article WHERE title = ?;''', [article_name])
                article_id = cursor.fetchone()[0]
                for category in article_categories:
                    cursor.execute('''SELECT category_id FROM category WHERE name = ?;''', [category])
                    category_id = cursor.fetchone()
                    if category_id is not None:
                        cursor.execute('''INSERT INTO article_category(article_id, category_id) VALUES (?, ?);''', [article_id, category_id[0]])
                db.commit()
            # Catch the exception
            except Exception as e:
                # Roll back any change if something goes wrong
                db.rollback()
                print(e)
    
    db.close()

if __name__ == '__main__':
    insert_articles()