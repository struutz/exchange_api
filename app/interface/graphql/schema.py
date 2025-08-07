import strawberry
from app.interface.graphql.mutations import TransactionMutation
from app.interface.graphql.queries.query_rates import RatesQuery, TransactionQuery


@strawberry.type
class Query(RatesQuery, TransactionQuery):
    @strawberry.field
    def health(self) -> str:
        return "OK"

@strawberry.type
class Mutation(TransactionMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)