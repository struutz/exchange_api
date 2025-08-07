import strawberry
from app.interface.graphql.queries.query_rates import RatesQuery


@strawberry.type
class Query(RatesQuery):
    pass