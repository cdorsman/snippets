# This very rough snippet is a implementation of MVC design pattern with a routing class routing to 
# different controller classes linking to different models and views.
#
# The Controller, Model and Views classes are subclasses from abstract base classes


#!/usr/bin/env python3

from abc import ABC, abstractmethod
from collections.abc import Iterable
from sys import argv

class Model(ABC, Iterable):
    _instances = []

    @abstractmethod
    def __iter__(self):
        return iter(getattr(self, '_instances', []))

    @abstractmethod
    def get(self, item):
        ...


class TestModel(Model):
    test_items = {
        "one": { "name": "1" },
        "two": { "name": "2" },
    }

    def __iter__(self):
        yield from self.test_items

    def get(self, item):
        try:
            return self.test_items[item]
        except KeyError as key_err:
            print("Key cannot be found", key_err)


class DummyModel(Model):
    test_items = {
        "one": { "name": "1" },
        "two": { "name": "2" },
    }

    def __iter__(self):
        yield from self.test_items

    def get(self, item):
        try:
            return self.test_items[item]
        except KeyError as key_err:
            print("Key cannot be found", key_err)


class View(ABC):
    @abstractmethod
    def show_item_list(self, item_list):
        ...

    @abstractmethod
    def show_item_information(self, item_name, item_info):
        ...

    @abstractmethod
    def item_not_found(self, item_name):
        ...


class TestView(View):
    def show_item_list(self, item_list):
        print(item_list)
        for item in item_list:
            print(item)
        print("")

    def show_item_information(self, item_name, item_info):
        print(f" INFORMATION of username {item_name} \n")
        labels = ""
        printout = ""

        for key, value in item_info.items():
            labels += (str(key)).upper() + "\t"

        print(labels)

        for key, value in item_info.items():
            printout += str(value) + "\t\t"

        print(printout)

    def item_not_found(self, item_name):
        print(f'That  "{item_name}" does not exist in the records')


class DummyView(View):
    def show_item_list(self, item_list):
        print(item_list)
        for item in item_list:
            print(item)
        print("")

    def show_item_information(self, item_name, item_info):
        print(f" INFORMATION of username {item_name} \n")
        labels = ""
        printout = ""

        for key, value in item_info.items():
            labels += (str(key)).upper() + "\t"

        print(labels)

        for key, value in item_info.items():
            printout += str(value) + "\t\t"

        print(printout)

    def item_not_found(self, item_name):
        print(f'That  "{item_name}" does not exist in the records')

class BaseController(ABC):
    @abstractmethod
    def show_items(self):
        pass

    @abstractmethod
    def show_item_information(self, item_name):
        pass


class TestController(BaseController):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = list(self.model)
        #item_type = self.model.item_type
        self.view.show_item_list(items)

    def show_item_information(self, item_name):
        try:
            item_info = self.model.get(item_name)
        except Exception:
            item_type = self.model.item_type
            self.view.item_not_found(item_type, item_name)
        else:
            item_type = self.model.item_type
            self.view.show_item_information(item_type, item_name, item_info)

class DummyController(BaseController):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = list(self.model)
        #item_type = self.model.item_type
        self.view.show_item_list(items)

    def show_item_information(self, item_name):
        try:
            item_info = self.model.get(item_name)
        except Exception:
            item_type = self.model.item_type
            self.view.item_not_found(item_type, item_name)
        else:
            item_type = self.model.item_type
            self.view.show_item_information(item_type, item_name, item_info)

class Router:
    def __init__(self):
        self.routes = {}

    def register(self, route, controller, model, view):
        model = model(); view = view()
        self.routes[route] = controller(model, view)

    def resolve(self, route):
        if self.routes.get(route):
            controller = self.routes[route]
            return controller
        else:
            raise ValueError("Cannot find route", route)

def main():
    router = Router()
    router.register("test", TestController, TestModel, TestView)
    router.register("dummy", DummyController, DummyModel, DummyView)

    request = argv[1]

    controller = router.resolve(request)
    if hasattr(controller, "show_items"):
        controller.show_items()


if __name__ == '__main__':
    main()
