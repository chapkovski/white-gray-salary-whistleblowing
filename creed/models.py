from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'creed'
    players_per_group = 6
    assert players_per_group % 2 == 0, "Количество участников должно быть четным"
    num_rounds = 10
    payoff_matrix = {'Белая': 50, 'Серая': 150}
    white_coef = 50
    gray_coef = 40
    endowment = 100


class Subsession(BaseSubsession):
    prob_catch = models.FloatField(doc='Вероятность поимки')
    fine = models.IntegerField(doc="Размер штрафа")

    def creating_session(self):
        self.prob_catch = self.session.config['prob_catch']
        self.fine = self.session.config['fine']
        for g in self.get_groups():
            players = g.get_players()
            random.shuffle(players)
            g.set_players(players)
            for p in g.get_players():
                if self.round_number == 1:
                    p.endowment = Constants.endowment
                else:
                    p.endowment = 0
                p.checked = random.random() < self.prob_catch
                if p.id_in_group % 2 == 1:
                    p.partner = p.id_in_group + 1
                else:
                    p.partner = p.id_in_group - 1


class Group(BaseGroup):
    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()

    def white_share(self):
        whites = len([p for p in self.get_players() if p.white])
        return whites / Constants.players_per_group

    def in_previous_round(self):
        return self.in_round(self.round_number - 1)


class Player(BasePlayer):
    user_id = models.IntegerField(label='Введите номер указанный на табличке у вас на столе')
    endowment = models.CurrencyField()
    white = models.BooleanField(choices=((True, 'Белая'), (False, 'Серая')),
                                label='Выберите тип зарплаты',
                                widget=widgets.RadioSelectHorizontal)
    wb = models.BooleanField(choices=((False, 'Не информировать'), (True, 'Информировать')),
                             label='Выберите хотели бы вы проинформировать налоговую',
                             widget=widgets.RadioSelectHorizontal)
    checked = models.BooleanField(initial=False)
    partner = models.IntegerField()
    base_payoff = models.CurrencyField(doc='Здесь мы храним базовый доход до штрафа')

    def set_check_of_partner(self):
        partner = self.group.get_player_by_id(self.parnter)
        if self.wb:
            partner.checked = True

    def set_payoff(self):
        if self.white:
            self.base_payoff = Constants.payoff_matrix[
                                   self.get_white_display()] + Constants.white_coef * self.group.white_share()
        else:
            self.base_payoff = Constants.payoff_matrix[self.get_white_display()] - Constants.gray_coef * (
                    1 - self.group.white_share())
        self.payoff = self.endowment + self.base_payoff - self.actual_fine()

    def in_previous_round(self):
        return self.in_round(self.round_number - 1)

    def delta(self):
        """Дельта прибыли между прошлым и позапрошлым периодами"""
        if self.round_number > 2:
            cur = self.round_number
            return self.in_round(cur - 1).base_payoff - self.in_round(cur - 2).base_payoff
        return 0

    def actual_fine(self):
        return (1 - self.white) * self.checked * self.subsession.fine

    def accumulated_payoff(self):
        """Возвращает аккумулированную прибыль к моменту прошлого периода"""
        return sum([p.payoff for p in self.in_all_rounds()])
