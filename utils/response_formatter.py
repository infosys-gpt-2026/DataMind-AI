from typing import Any


def clean_response(response: Any) -> str:
    """
    Convert different LangChain/Gemini response formats
    into a clean human-readable string.
    """

    # Already a normal string
    if isinstance(response, str):
        return response.strip()

    # Gemini/LangChain sometimes returns a list
    if isinstance(response, list):

        cleaned_parts = []

        for item in response:

            # Example:
            # {'type': 'text', 'text': 'Hello'}
            if isinstance(item, dict):

                if "text" in item:
                    cleaned_parts.append(
                        str(item["text"])
                    )

                elif "content" in item:
                    cleaned_parts.append(
                        str(item["content"])
                    )

            elif isinstance(item, str):
                cleaned_parts.append(item)

            else:
                cleaned_parts.append(str(item))

        return "\n".join(cleaned_parts).strip()

    # Dictionary response
    if isinstance(response, dict):

        if "text" in response:
            return str(response["text"]).strip()

        if "content" in response:
            return clean_response(response["content"])

        if "output" in response:
            return clean_response(response["output"])

        return str(response).strip()

    # LangChain AIMessage-like object
    if hasattr(response, "content"):
        return clean_response(response.content)

    # Fallback
    return str(response).strip()