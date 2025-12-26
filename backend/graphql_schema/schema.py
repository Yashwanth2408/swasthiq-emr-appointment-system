"""
GraphQL Schema definition
Combines queries and mutations into a single schema
"""

import strawberry
from graphql_schema.queries import Query
from graphql_schema.mutations import Mutation


# Create the complete GraphQL schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
