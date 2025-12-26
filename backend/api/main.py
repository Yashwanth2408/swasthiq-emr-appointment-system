"""
FastAPI application with Strawberry GraphQL integration
Main entry point for the backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from graphql_schema.schema import schema

# Initialize FastAPI app
app = FastAPI(
    title="SwasthiQ EMR - Appointment Management API",
    description="GraphQL API for appointment scheduling and management",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "https://*.vercel.app",   # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Mount GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "SwasthiQ EMR API",
        "status": "running",
        "graphql_endpoint": "/graphql"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
