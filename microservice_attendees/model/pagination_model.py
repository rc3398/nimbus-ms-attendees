from datetime import date, datetime, time, timezone
from dateutil import parser
from flask_restx import Model
from flask_restx.fields import Boolean, DateTime, Integer, List, Nested, String, Url
from flask_restx.inputs import positive, URL
from flask_restx.reqparse import RequestParser


pagination_links_model = Model(
    "Nav Links",
    {"self": String, 
     "prev": String, 
     "next": String, 
     "first": String, 
     "last": String},
)

pagination_model = Model(
    "Pagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        # "items": List(Nested(widget_model)),
    },
)
