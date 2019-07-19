from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'creed'
    players_per_group = 10
    assert players_per_group % 2 == 0, "Количество участников должно быть четным"
    num_rounds = 1
    white_payoff = 100
    gray_payoff = 110



class Subsession(BaseSubsession):
    prob_catch = models.FloatField(doc='Вероятность поимки')
    fine = models.IntegerField(doc="Размер штрафа")
    def creating_session(self):
        for g in self.get_groups():
            for p in g.get_players():
                if p.id_in_group % 2 == 1:
                    p.partner = p.id_in_group + 1
                else:
                    p.partner = p.id_in_group - 1


class Group(BaseGroup):
    def set_payoffs(self):
        pass


class Player(BasePlayer):
    salary = models.BooleanField(choices=((False, 'Серая'), (True, 'Белая')))
    wb = models.BooleanField(choices=((False, 'Не информировать'), (True, 'Информировать')))
    partner = models.IntegerField()

    def set_payoff(self):
