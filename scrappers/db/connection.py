import rethinkdb as r
r.connect('localhost', 28015).repl()

def table_create():
    r.db('test').table_create('authors').run()

def insert_product(data):
    r.db('test').table('products').insert(data).run()
