def format_schemas_for_prompt(results: list[dict]) -> str:
    """
    Trim retrieved schema objects down to only what the LLM needs for SQL gen.
    Strips out: doc_id, score, has_lineage, upstream, downstream, table, schema fields.

    Input (from query_schema):
        [{"fqn": "...", "table_type": "VIEW", "score": 0.82,
          "description": "...", "columns": [{"name":..,"type":..}], ...}]

    Output (compact schema context string):
        -- TABLE: railways.railway.passengers
        -- Dataset Name: passengers | Purpose: stores passenger info
        passenger_id BIGINT, name VARCHAR, email VARCHAR ...

        -- VIEW: railways_ai.popular_routes
        -- Identifies the most frequently traveled routes
        source_station VARCHAR, destination_station VARCHAR, passenger_count BIGINT
    """
    lines = []
    for r in results:
        col_str = ", ".join(f"{c['name']} {c['type']}" for c in r["columns"])
        # First line of description only — enough context, avoids noise
        desc_summary = r["description"].splitlines()[0] if r["description"] else "No description"
        lines.append(
            f"-- {r['table_type']}: {r['fqn']}\n"
            f"-- {desc_summary}\n"
            f"{col_str}"
        )
    return "\n\n".join(lines)