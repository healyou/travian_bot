from abc import abstractmethod


class IView(object):
    @abstractmethod
    def test(self):
        pass


class IPresenter(object):
    @abstractmethod
    def test(self):
        pass
