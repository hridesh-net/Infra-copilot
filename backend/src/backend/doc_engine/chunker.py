def chunk_text(text: str, chunk_size: int = 300) -> list[str]:
    """
    Splits raw doc text into smaller paragraphs/chunks.
    """
    paragraphs = text.split("\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current + para) < chunk_size:
            current += para + "\n"
        else:
            chunks.append(current.strip())
            current = para
    chunks.append(current.strip())
    return chunks
