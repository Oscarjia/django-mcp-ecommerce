import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route,Mount
from starlette.requests import Request

from mcp.server.sse import SseServerTransport
from mcp_order_server.mcp_server import mcp

# 1) Instantiate the SSE transport,pointing at /messages
sse_transport = SseServerTransport("/messages")

# 2) Define the GET /sse endpoint
async def handle_sse(request: Request) :
    """
    Connect MCP Server to  the /sse endpoint.
    """
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        pass

# 3) Assemble the Starlette app
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ]
)