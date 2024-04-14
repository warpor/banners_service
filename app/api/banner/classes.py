from typing import NamedTuple


class TagsForChange(NamedTuple):
    tag_ids_for_add: list[int]
    tag_ids_for_delete: list[int]
