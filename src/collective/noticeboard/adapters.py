class NewsAdapter(object):
    def __init__(self, context):
        self.context = context

    @property
    def text(self):
        return "Example"

    @property
    def image_url(self):
        return "http://www.ccc.de"

    @property
    def position_x(self):
        return 1

    @property
    def position_y(self):
        return 2