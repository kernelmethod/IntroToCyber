"""
Inject some JavaScript into the webpage returned in an HTTP response.
"""

from mitmproxy import ctx, http

def response(flow: http.HTTPFlow) -> None:
    if (response := flow.response) is None or response.content is None:
        return

    # Only inject JavaScript in pgaes that return status code 200
    if response.status != 200:
        return

    # The `response` variable holds a `Response` object, with various fields
    # that you would find in an HTTP response:
    #     https://docs.mitmproxy.org/stable/api/mitmproxy/http.html#Response
    #
    # If the request contains HTML, you should modify the response.content
    # variable so that it contains your custom JavaScript code.

    # TODO: your code here!
