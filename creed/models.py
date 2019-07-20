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
    players_per_group = 2
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
    cq1, cq2, cq3, cq4 = [models.BooleanField(label='',
                                              widget=widgets.RadioSelectHorizontal,
                                              choices=((False, "Нет"), (True, "Да")), ) for _ in range(4)]

    def cq1_error_message(self, value):
        if value != True:
            return 'Проверьте правильность ответа'

    def cq2_error_message(self, value):
        if value != False:
            return 'Проверьте правильность ответа'

    def cq3_error_message(self, value):
        if value != False:
            return 'Проверьте правильность ответа'

    def cq4_error_message(self, value):
        if value != True:
            return 'Проверьте правильность ответа'


    def get_partner(self):
        return self.group.get_player_by_id(self.partner)

    def set_check_of_partner(self):
        if self.wb:
            self.get_partner().checked = True

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
