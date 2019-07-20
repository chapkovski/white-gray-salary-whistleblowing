from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):
    form_fields = ['user_id']
    form_model = 'player'

    def before_next_page(self):
        self.participant.label = str(self.player.user_id)

    def is_displayed(self) -> bool:
        return self.round_number == 1


class Instructions(Page):
    def is_displayed(self) -> bool:
        return self.round_number == 1


class CQ(Page):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 'cq3', 'cq4']

    def is_displayed(self) -> bool:
        return self.round_number == 1


class Salary(Page):
    form_model = 'player'
    form_fields = ['white']


class WB(Page):
    form_model = 'player'
    form_fields = ['wb']


class ResultsWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self) -> bool:
        return self.round_number != 1


class FinalResults(Page):
    def is_displayed(self) -> bool:
        return self.round_number == Constants.num_rounds


page_sequence = [
    Intro,
    Instructions,
    CQ,
    Salary,
    WB,
    ResultsWP,
    Results,
    # FinalResults,

]
