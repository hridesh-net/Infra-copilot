import tiktoken


def chunk_text(
    text: str,
    metadata: dict,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    model: str = "text-embedding-ada-002"
) -> list[dict]:
    """
    Splits input text into token-based chunks with overlap.

    Args:
        text: The raw text to split.
        metadata: Base metadata dict to attach to each chunk.
        chunk_size: Maximum number of tokens per chunk.
        chunk_overlap: Number of overlapping tokens between consecutive chunks.
        model: The embedding model name for tokenization.

    Returns:
        A list of dicts, each with:
          - text: The chunk text.
          - metadata: Base metadata plus 'chunk_id', 'start_token', 'end_token'.
    """
    # Initialize tokenizer
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)

    chunks: list[dict] = []
    total_tokens = len(tokens)
    chunk_id = 0
    start = 0

    while start < total_tokens:
        end = min(start + chunk_size, total_tokens)
        chunk_tokens = tokens[start:end]
        chunk_str = encoder.decode(chunk_tokens)

        # Build metadata for this chunk
        chunk_meta = metadata.copy()
        chunk_meta.update({
            "chunk_id": chunk_id,
            "start_token": start,
            "end_token": end,
        })

        chunks.append({"text": chunk_str, "metadata": chunk_meta})

        # Move window
        chunk_id += 1
        start += chunk_size - chunk_overlap

    return chunks
