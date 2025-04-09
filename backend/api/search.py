from typing import Dict, Sequence

from fastapi import APIRouter, Query
from sqlalchemy import text, Result, RowMapping

from backend.db.session import SessionLocal
from jinja2 import Template


SEARCH_ITEMS = text("""
    SELECT * FROM items 
    WHERE 
        TRUE
        {% for term in search_terms %}
        AND (
            name ILIKE :term{{loop.index}} 
            OR brand ILIKE :term{{loop.index}}
        )
        {% endfor %}
""")


router = APIRouter(
    prefix="/search",
)


@router.get("/items/query")
async def search_items(
        query: str = Query(..., min_length=1, description="Search term for name, brand, or description"),
) -> Dict[str, str]:
    # Split the query into individual terms
    search_terms: list[str] = query.strip().split()

    # Create a dynamic query with parameters for each term
    query_template: Template = Template(SEARCH_ITEMS.text)
    rendered_query: str = query_template.render(search_terms=search_terms)

    # Create parameter dictionary with wildcard for each term
    query_params: dict[str, str] = {}
    for index, term in enumerate(search_terms, 1):
        query_params[f"term{index}"] = f"%{term}%"

    print(f"Executing search with terms: {search_terms}")

    with SessionLocal() as session:
        result: Result = session.execute(text(rendered_query), query_params)
        items: Sequence[RowMapping] = result.mappings().all()

    return {"query": query, "items": items}
