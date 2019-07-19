from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield Salary, {'white': random.choice([False, True])}
        yield WB, {'wb': random.choice([False, True])}
        if self.round_number > 1:
            yield Results,
