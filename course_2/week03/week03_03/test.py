from solution import ObservableEngine, ShortNotificationPrinter, FullNotificationPrinter


def main():
    achievements = [
        {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"},
        {"title": "Расхититель", "text": "Дается выполнении всех заданий в игре"},
        {"title": "Разрушитель", "text": "Дается при всех заданий в игре"},
        {"title": "Устрашитель", "text": "Дается при выполнении заданий в игре"}
    ]

    obs1 = ShortNotificationPrinter()
    obs2 = FullNotificationPrinter()
    obs3 = ShortNotificationPrinter()

    engine = ObservableEngine()
    engine.subscribe(obs1)
    engine.subscribe(obs2)
    engine.subscribe(obs3)
    print(engine._observers)
    for achievement in achievements:
        engine.notify(achievement)
    engine.unsubscribe(obs1)
    engine.unsubscribe(obs2)
    engine.unsubscribe(obs3)
    print(obs1)
    print(obs2)
    print(obs3)


if __name__ == '__main__':
    main()