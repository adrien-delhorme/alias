from schematics.models import Model


class Handler(Model):
    credentials = None

    def __init__(self, credentials, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self.credentials = credentials
