from flask import Flask

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

from MultiNest import Views

if __name__ == '__main__':
    app.run()
