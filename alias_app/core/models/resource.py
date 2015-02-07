
class Resource(object):
    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
