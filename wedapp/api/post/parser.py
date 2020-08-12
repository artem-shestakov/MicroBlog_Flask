from flask_restful import reqparse

post_get_parser = reqparse.RequestParser()

# Post API
# GET params
post_get_parser.add_argument("page", type=int, location=["args", "headers"], required=False)
post_get_parser.add_argument("user", type=str, location=["args", "headers"], required=False)

# POST params
post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument("title", type=str, location=["json", "values"], required=True)
post_post_parser.add_argument("text", type=str, location=["json", "values"], required=True)
post_post_parser.add_argument("tags", type=str, location=["json", "values"], action="append")

# PUT params
post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument("title", type=str, location=["json", "values"])
post_put_parser.add_argument("text", type=str, location=["json", "values"])
post_put_parser.add_argument("tags", type=str, location=["json", "values"], action="append")
