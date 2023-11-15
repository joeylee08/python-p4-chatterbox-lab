from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import ipdb
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = []
        # messages = [item.to_dict() for item in Message.query.order_by('created_at').all()]
        for item in Message.query.order_by('created_at').all():
            messages.append(item.to_dict())
        return make_response(messages, 200)
    else:
        new_message = Message(body=request.get_json()["body"], username=request.get_json()["username"])
        db.session.add(new_message)
        db.session.commit()
        response_dict = new_message.to_dict()
        return make_response(response_dict, 201)
    
@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == "PATCH":
        for attr in request.get_json():
            setattr(message, attr, request.get_json()[attr])
        db.session.add(message)
        db.session.commit()
        response_dict = message.to_dict()

        return make_response(response_dict, 200)
    else:
        db.session.delete(message)

if __name__ == '__main__':
    app.run(port=5555)
