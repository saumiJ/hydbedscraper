from hydbedscraper.types import t_Response


def decode_streamed_string_response(response: t_Response) -> str:
    response_content = ""
    for chunk in response.iter_content(8192, decode_unicode=True):
        response_content += chunk
    return response_content
