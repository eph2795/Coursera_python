from abc import ABC, abstractmethod


# class Engine(ABC):
#     pass


class ObservableEngine(Engine):

    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, achievement):
        for observer in self._observers:
            observer.update(achievement)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, achievement):
        pass

    def __str__(self):
        return str(self.achievements)

    def __repr__(self):
        return str(self.achievements)


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        self.achievements.add(achievement['title'])


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = []

    def update(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
