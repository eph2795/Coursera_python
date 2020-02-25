from abc import ABC, abstractmethod


# class Hero:
#     def __init__(self):
#         self.positive_effects = []
#         self.negative_effects = []
#         self.stats = {
#             "HP": 128,  # health points
#             "MP": 42,  # magic points,
#             "SP": 100,  # skill points
#             "Strength": 15,  # сила
#             "Perception": 4,  # восприятие
#             "Endurance": 8,  # выносливость
#             "Charisma": 2,  # харизма
#             "Intelligence": 3,  # интеллект
#             "Agility": 8,  # ловкость
#             "Luck": 1  # удача
#         }
#
#     def get_positive_effects(self):
#         return self.positive_effects.copy()
#
#     def get_negative_effects(self):
#         return self.negative_effects.copy()
#
#     def get_stats(self):
#         return self.stats.copy()


class AbstractEffect(ABC, Hero):

    def __init__(self, base):
        # if type(self) is AbstractEffect:
        #     raise Exception()
        super().__init__()
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Berserk']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] += 7
        stats['Endurance'] += 7
        stats['Agility'] += 7
        stats['Luck'] += 7
        stats['HP'] += 50
        stats['Perception'] -= 3
        stats['Charisma'] -= 3
        stats['Intelligence'] -= 3
        return stats


class Blessing(AbstractPositive):

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Blessing']

    def get_stats(self):
        stats = self.base.get_stats()
        for k, v in stats.items():
            if k in ['Strength', 'Perception', 'Endurance', 'Charisma',
                     'Intelligence', 'Agility', 'Luck']:
                stats[k] = v + 2
        return stats


class Weakness(AbstractNegative):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Weakness']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] -= 4
        stats['Endurance'] -= 4
        stats['Agility'] -= 4
        return stats


class EvilEye(AbstractNegative):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Luck'] -= 10
        return stats


class Curse(AbstractNegative):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']

    def get_stats(self):
        stats = self.base.get_stats()
        for k, v in stats.items():
            if k in ['Strength', 'Perception', 'Endurance', 'Charisma',
                     'Intelligence', 'Agility', 'Luck']:
                stats[k] = v - 2
        return stats
