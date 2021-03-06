from flask import Flask, render_template, url_for, request

from peewee import *

db = SqliteDatabase("Entries.db")

app = Flask(__name__)


# Class for developing and managing the database
class Entry(Model):
    entry_id = AutoField()
    entry_title = CharField(max_length=255)
    entry_date = DateField()
    time_spent = IntegerField()
    what_learned = TextField()
    resources = TextField()

    class Meta:
        database = db


# Initialize database by making the connection each time
# and creating the tables if they dont exist
def initialize():
    db.connect(reuse_if_open=True)
    db.create_tables([Entry], safe=True)


# Function for adding data to the database
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


# Function for updating a record in the database
def update_data(an_id, title, date, time_spent, what_learned, resources):
    Entry.update({Entry.entry_title: title,
                  Entry.entry_date: date,
                  Entry.time_spent: time_spent,
                  Entry.what_learned: what_learned,
                  Entry.resources: resources}
                 ).where(Entry.entry_id == int(an_id)).execute()


# Function for retrieving data from the databse
# if an id is provided it gets a specifi entry
def get_data(id=None):
    list_of_entries = Entry.select().order_by(Entry.entry_id)
    if id:
        list_of_entries = list_of_entries.where(Entry.entry_id == id)
        an_entry = []
        for entry in list_of_entries:
            temp_list = entry.resources.split(", ")
            an_entry.append(entry.entry_id)
            an_entry.append(entry.entry_title)
            an_entry.append(entry.entry_date)
            an_entry.append(entry.time_spent)
            an_entry.append(entry.what_learned)
            an_entry.append(temp_list)
        return an_entry
    else:
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


# Function for deleting an enty in the database
def delete_entry(an_id):
    Entry.delete().where(Entry.entry_id == int(an_id)).execute()


# Route for homepage
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


# Route for viewing details of a specific entry
@app.route("/entries/<int:an_id>")
def view_details(an_id):
    initialize()
    detail_data = get_data(an_id)
    return render_template("detail.html", details=detail_data)


# Route for creating a new entry
@app.route("/entries/new", methods=["GET", "POST"])
def add_new():
    initialize()
    if request.method == "GET":
        return render_template("new.html")
    elif request.method == "POST":
        data = dict(request.form.items())
        add_data(data["title"],
                 data["date"],
                 data['timeSpent'],
                 data["whatILearned"],
                 data["ResourcesToRemember"]
                 )
        return index()


# Route for editing an entry given an id
@app.route("/entries/<an_id>/edit", methods=["GET", "POST"])
def edit(an_id):
    initialize()
    if request.method == "GET":
        an_entry = get_data(an_id)
        resources_string = ", ".join(an_entry[5])
        new_entry = an_entry[0:5]
        new_entry.append(resources_string)
        return render_template("edit.html", details=an_entry)
    elif request.method == "POST":
        data = dict(request.form.items())
        update_data(an_id,
                    data["title"],
                    data["date"],
                    data['timeSpent'],
                    data["whatILearned"],
                    data["ResourcesToRemember"]
                    )
        return index()


# Route for deleting an entry given an id
@app.route("/entries/<an_id>/delete")
def delete(an_id):
    initialize()
    delete_entry(an_id)
    return index()


# Runs flask
app.run(debug=True, host='127.0.0.1', port=8000)
