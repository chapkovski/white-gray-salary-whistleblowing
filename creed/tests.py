from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Intro, {'user_id': 1}
            yield Instructions,
            yield CQ, {'cq1': True, 'cq2': False, 'cq3': False, 'cq4': True, }
        yield Salary, {'white': random.choice([False, True])}
        yield WB, {'wb': random.choice([False, True])}
        if self.round_number > 1:
            yield Results,
