from rest_framework.pagination import PageNumberPagination


class NoUrlPagination(PageNumberPagination):
    def get_next_link(self):
        # Override the default next page getter to remove the url
        if not self.page.has_next():
            return None
        next_num = self.page.next_page_number()
        return next_num

    def get_previous_link(self):
        # Override the default prev page getter to remove the url
        if not self.page.has_previous():
            return None
        prev_num = self.page.previous_page_number()
        return prev_num
