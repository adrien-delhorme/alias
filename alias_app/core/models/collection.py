from requests.exceptions import HTTPError
from schematics.models import Model
from schematics.types.compound import ListType
from schematics.types.compound import ModelType


class Collection(Model):
    items_class = None
    handler = None

    @property
    def items(self):
        if len(self._items) == 0:
            self.fetch()
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    def __init__(self, handler, *args, **kwargs):
        super(Collection, self).__init__(*args, **kwargs)
        self.handler = handler
        self._items = ListType(ModelType(self.items_class))(self)

    def __str__(self):
        return "{}".format(self.items)

    def find(self, field, value):
        items_dict = dict(zip([getattr(item, field) for item in self.items], self.items))

        if value in items_dict:
            return items_dict[value]

    def fetch(self):
        raise NotImplementedError

    def add(self, item):
        self._items.append(item)

    def remove(self, field, value):
        item = self.find(field, value)
        if item is None:
            raise IndexError("Item with {} = {} not found in collection".format(field, value))
            return
        try:
            item.delete()
        except HTTPError:
            print "Can not remove item with {} = {}".format(field, value)
        else:
            self._items.remove(item)
