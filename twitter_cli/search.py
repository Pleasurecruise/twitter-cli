"""Advanced search query builder.

Composes Twitter search operators into a raw query string for the
SearchTimeline GraphQL endpoint.

Reference: https://help.x.com/en/using-x/x-advanced-search
"""

from __future__ import annotations

from typing import List, Optional, Sequence


def build_search_query(
    query: str = "",
    *,
    from_user: Optional[str] = None,
    to_user: Optional[str] = None,
    lang: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    has: Optional[Sequence[str]] = None,
    exclude: Optional[Sequence[str]] = None,
    min_likes: Optional[int] = None,
    min_retweets: Optional[int] = None,
) -> str:
    """Build an advanced search query string.

    Args:
        query: Base search keywords.
        from_user: Only tweets from this user (screen_name).
        to_user: Only tweets directed at this user.
        lang: ISO 639-1 language code (e.g. "en", "fr", "ja").
        since: Start date in YYYY-MM-DD format.
        until: End date in YYYY-MM-DD format.
        has: List of content types to require. Accepted values:
            "links", "images", "videos", "media".
        exclude: List of content types to exclude. Accepted values:
            "retweets", "replies", "links".
        min_likes: Minimum number of likes (faves).
        min_retweets: Minimum number of retweets.

    Returns:
        Composed query string ready for the rawQuery API parameter.
    """
    parts: List[str] = []

    if query and query.strip():
        parts.append(query.strip())

    if from_user:
        parts.append("from:%s" % from_user.lstrip("@"))
    if to_user:
        parts.append("to:%s" % to_user.lstrip("@"))
    if lang:
        parts.append("lang:%s" % lang)
    if since:
        parts.append("since:%s" % since)
    if until:
        parts.append("until:%s" % until)
    if has:
        for item in has:
            parts.append("filter:%s" % item)
    if exclude:
        for item in exclude:
            if item == "retweets":
                parts.append("-filter:retweets")
            elif item == "replies":
                parts.append("-filter:replies")
            elif item == "links":
                parts.append("-filter:links")
            else:
                parts.append("-filter:%s" % item)
    if min_likes is not None:
        parts.append("min_faves:%d" % min_likes)
    if min_retweets is not None:
        parts.append("min_retweets:%d" % min_retweets)

    return " ".join(parts)
