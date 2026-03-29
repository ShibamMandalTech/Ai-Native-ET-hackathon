def decide(row):
    if row["retries"] > 3:
        return "skip"

    stage = row.get("processing_stage")

    if stage is None or stage == "pending":
        return "short"

    if stage == "short_done":
        return "deep"

    if stage == "deep_done":
        return "summary"

    return "complete"


# def decide(row):
#     if row["retries"] > 3:
#         return "skip"

#     if not row["content"]:
#         return "short"

#     if not row["cluster_id"]:
#         return "cluster"

#     if not row["deep_content"]:
#         return "deep"

#     if not row["summary_points"]:
#         return "summary"

#     return "complete"