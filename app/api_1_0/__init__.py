from flask.ext.restful import Resource, Api, reqparse
from flask import request


appApi = Api(prefix='/api')

parser = reqparse.RequestParser()
parser.add_argument('event', type=str)
from app import mongo


class PostLog(Resource):

    def post(self):
        args = parser.parse_args()
        if 'event' not in args.keys():
            return 400
        clientIp = request.remote_addr
        clientEvent = args['event']
        logEvent = {'ip': clientIp, 'event': clientEvent}

        # TODO: Log validation here

        # log to mongoDB
        print logEvent

        mongo.db.app.log.insert(logEvent)
        return 201

appApi.add_resource(PostLog, "/log_event")
