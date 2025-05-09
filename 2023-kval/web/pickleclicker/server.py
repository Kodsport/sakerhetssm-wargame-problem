import io
import pickle
import flask
# save = []
app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def button():
    if flask.request.method == 'POST':
        f = flask.request.files['Choose Savefile']
        if f.filename:
            try:
                pickle_load_result = pickle.load(f.stream)

                save = pickle_load_result
                if type(save) != list:
                    save = []
                return flask.render_template('index.html' , save_datas=save)

            except:
                print("error")
    return flask.render_template('index.html' , save_datas=[])

@app.route('/save', methods=['POST'])
def create_pickle_file():

    version = flask.request.form.get('version_name')

    pickles = flask.request.form.get('pickle_amount')
    pps = flask.request.form.get('pps_amount')

    amount_pickle_farmer = flask.request.form.get('amount_pickle_farmer')
    amount_pickle_factory = flask.request.form.get('amount_pickle_factory')
    amount_pickle_plane = flask.request.form.get('amount_pickle_plane')

    cost_pickle_farmer = flask.request.form.get('cost_pickle_farmer')
    cost_pickle_factory = flask.request.form.get('cost_pickle_factory')
    cost_pickle_plane = flask.request.form.get('cost_pickle_plane')


    save = [version, pickles, pps, amount_pickle_farmer, amount_pickle_factory, amount_pickle_plane, cost_pickle_farmer, cost_pickle_factory, cost_pickle_plane]


    savefile = io.BytesIO()
    pickle.dump(save, savefile)
    savefile.seek(0)

    return flask.send_file(savefile, attachment_filename="Savefile.pickle", as_attachment=True)


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if flask.request.method == 'POST':
#       f = flask.request.files['Choose Savefile']
#       if f.filename:
#           try:
#               pickle_load_result = pickle.load(f.stream)

#               global save
#               save = pickle_load_result
#               if type(save) != list:
#                   save = []
#               return flask.redirect("/")

#           except:
#               print("error")
#    return flask.redirect("/")

if __name__ == '__main__':

    app.run(debug=False, port=4001)

