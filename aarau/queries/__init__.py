import math

from pyramid.decorator import reify


class PaginatedQuery:
    def __init__(self, query_or_model, current_page, items_per_page):
        self._current_page = current_page
        self._items_per_page = items_per_page
        self._query = query_or_model

    @reify
    def page(self):
        """Current page number."""
        if self._current_page and self._current_page.isdigit():
            return max(1, int(self._current_page))
        return 1

    @reify
    def next_page(self):
        if self.page >= self.page_count:
            return None
        return self.page + 1

    @reify
    def prev_page(self):
        if self.page < 2:
            return None
        return self.page - 1

    @reify
    def page_count(self):
        """Pages count."""
        return int(math.ceil(
            float(self.total_count) / self._items_per_page))

    @reify
    def total_count(self):
        """Total records count."""
        return self._query.count()

    def get_objects(self):
        if self.page > self.page_count:
            return ()
        return self._query.paginate(self.page, self._items_per_page)
