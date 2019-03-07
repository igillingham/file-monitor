from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from flask_restful import Resource, Api
from socket import gethostname
import dbmanager
import file_manager

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    """index(): This is the root URL handler.
        Simply redirect to the 'help' page.
    """
    return redirect(url_for('help'))


@app.route('/help/')
@app.route('/help/<name>')
def help(name=None):
    """ help(): Render some helpful information in the user browser
        If a trailing argument has been supplied in the URL, then
        interpret it as a topic help request and display further info.
    """
    return render_template('help.html', name=name)


class FilesAvailable(Resource):
    def get(self):
        avail = dbmanager.db.get_available_entries()
        return avail


class FilesArchived(Resource):
    def get(self):
        avail = dbmanager.db.get_archived_entries()
        return avail


class FilesAll(Resource):
    def get(self):
        avail = dbmanager.db.get_all_entries()
        return avail


# This is the RESTful API definition area...
api.add_resource(FilesAvailable, '/filesavailable')
api.add_resource(FilesArchived, '/filesarchived')
api.add_resource(FilesAll, '/filesall')


if __name__ == '__main__':
    # db.create_all()

    # Start the database manager
    if dbmanager.db.connect():
        print("Database connected OK")

        # Start monitoring the directory given in conf.json
        status = file_manager.rhea_monitor_fs()

        if status == file_manager.ERR_NO_ERROR:
            if 'liveconsole' not in gethostname():  # Avoid app.run() if deploying on PythonAnywhere service
                print("Directory monitoring started.")
                app.run(host='127.0.0.1', port=8000, debug=True)
        elif status == file_manager.ERR_NO_CONF:
            print("Monitoring directory not specified in conf.json")
        elif status == file_manager.ERR_NO_DIR:
            print("Monitoring directory does not exist")
    else:
        print("Failed to find database!")

