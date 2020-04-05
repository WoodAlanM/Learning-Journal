from flask import Flask, render_template

from peewee import *

db = SqliteDatabase("Entries.db")

app = Flask(__name__)


class Entry(Model):
    entry_id = AutoField()
    entry_title = CharField(max_length=255)
    entry_date = DateField()
    time_spent = IntegerField()
    what_learned = TextField()
    resources = TextField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)


def add_data(title, date, time_spent, what_learned, resources):
    try:
        Entry.create(entry_title=title,
                     entry_date=date,
                     time_spent=time_spent,
                     what_learned=what_learned,
                     resources=resources
                     )
        return True
    except IntegrityError:
        return False


def get_data():
    list_of_entries = Entry.select().order_by(Entry.entry_id)
    return_list = []
    for entry in list_of_entries:
        temp_list = entry.resources.split(", ")
        entry_list = [entry.entry_id,
                      entry.entry_title,
                      entry.entry_date,
                      entry.time_spent,
                      entry.what_learned,
                      temp_list]
        return_list.append(entry_list)
    return return_list


@app.route("/")
@app.route("/entries")
def index():
    initialize()
    list_of_entries = get_data()
    list_of_items = []
    for entry in list_of_entries:
        ids_titles_dates = [entry[0], entry[1], entry[2]]
        list_of_items.append(ids_titles_dates)
    return render_template("index.html", titledates=list_of_items)


@app.route("/entries/<id>")
def view_details(id):
    initialize()
    list_of_entries = get_data()
    detail_data = list_of_entries[int(id) - 1]
    return render_template("detail.html", details=detail_data)


app.run(debug=True, host='127.0.0.1', port=8000)
