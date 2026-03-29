def build_timeline(chunks):

    # sort by date
    sorted_chunks = sorted(
        chunks,
        key=lambda x: x.get("created_at", "")
    )

    timeline = []

    for c in sorted_chunks:
        timeline.append({
            "date": c.get("created_at"),
            "event": c["text"][:200],
            "title": c.get("title"),
            "source": c.get("source")
        })

    return timeline