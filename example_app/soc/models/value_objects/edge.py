from pydantic import BaseModel, Field


class Edge(BaseModel):
    """
    Represents an edge in a graph, connecting two exam points. Edges define relationships between exam points
    and may include a bridging concept to describe the connection between them.
    """
    from_ep: str = Field("", description="The exam point where the edge originates.")
    to_ep: str = Field("", description="The exam point where the edge terminates.")
    bridging_concept: str = Field("", description="The concept bridging the connection between exam points.")
    weight: float = Field(1.0, description="The weight or importance of the edge in the overall assessment.")

