import hashlib
import json
from dremio_mcp import DremioMcpClient
from ingest import ingest, get_vectorstore


async def fetch_metadata() -> list[dict]:

        vs=get_vectorstore()
        count = vs._collection.count()
        print(count)
        if count == 0:
            tools        = await DremioMcpClient().connect()
            by_name = {t.name: t for t in tools}

            # 1. Discover all tables + views across all spaces (excludes system tables)
            sql = (
                'SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE '
                'FROM INFORMATION_SCHEMA."TABLES" '
                "WHERE TABLE_TYPE != 'SYSTEM_TABLE' and TABLE_TYPE != 'TABLE'"
            )
            raw = await by_name["RunSqlQuery"].ainvoke({"query": sql})
            text_block = next(b for b in raw if b["type"] == "text")
            rows = json.loads(text_block["text"])["result"]
            print(f"Discovered {len(rows)} tables/views")

            docs = []
            for row in rows:
                fqn = f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
                table_type = row["TABLE_TYPE"]  # TABLE or VIEW
                print(f"  processing [{table_type}] {fqn}")

                schema = await by_name["GetSchemaOfTable"].ainvoke({"table_name": fqn})
                schema = json.loads(next(b for b in schema if b["type"] == "text")["text"])

                description = await by_name["GetDescriptionOfTableOrSchema"].ainvoke({"name": fqn})
                description = json.loads(next(b for b in description if b["type"] == "text")["text"])

                try:
                    lineage = await by_name["GetTableOrViewLineage"].ainvoke({"table_name": fqn})
                    lineage = json.loads(next(b for b in lineage if b["type"] == "text")["text"])
                except Exception:
                    lineage = None

                docs.append(build_document(fqn, table_type, schema, description, lineage))
                ingest(docs)
                return docs

        return []

def _doc_id(table_fqn: str) -> str:
    return hashlib.md5(table_fqn.encode()).hexdigest()


def build_document(fqn: str, table_type: str, schema: dict, description: dict, lineage: dict | None) -> dict:
    # --- schema: fields are under "fields", type is nested as type.name ---
    fields = schema.get("fields", [])
    col_lines = [
        f"  {f['name']} {f['type']['name']}"
        for f in fields
    ]
    col_text = "\n".join(col_lines)

    # --- description: nested under quoted FQN key, or top-level fallback ---
    # key format: "\"schema\".\"table\""
    quoted_fqn = '.'.join(f'\"{p}\"' for p in fqn.split("."))
    desc_block = description.get(quoted_fqn) or next(iter(description.values()), {})
    desc_text = (desc_block.get("description") or schema.get("description") or "").strip()
    tags = ", ".join(desc_block.get("tags", []) or schema.get("tags", []))

    lineage_up = ", ".join(lineage.get("upstream", [])) if lineage else ""
    lineage_dn = ", ".join(lineage.get("downstream", [])) if lineage else ""

    # embed_content: compact string for vector embedding
    embed_content = (
        f"{table_type}: {fqn}\n"
        f"Description: {desc_text}\n"
        f"Columns: {', '.join(f['name'] + ' ' + f['type']['name'] for f in fields)}"
    ).strip()

    meta = {
        "fqn": fqn,
        "schema": fqn.rsplit(".", 1)[0] if "." in fqn else "",
        "table": fqn.rsplit(".", 1)[-1],
        "table_type": table_type,
        "column_count": len(fields),
        "has_lineage": bool(lineage_up or lineage_dn),
        "tags": tags,
        "upstream": lineage_up,
        "downstream": lineage_dn,
    }
    return {
        "doc_id": _doc_id(fqn),
        "content": embed_content,  # used for ChromaDB embedding
        "description": desc_text,  # full wiki/description text
        "columns": [{"name": f["name"], "type": f["type"]["name"]} for f in fields],
        "metadata": meta,
    }