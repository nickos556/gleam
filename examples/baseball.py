import os
from collections import OrderedDict

from flask import Flask
from wtforms import fields
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from gleam import Page, panels


# setup

stats = ['At-Bats (AB)', 'Runs (R)', 'Hits (H)', 'Doubles (2B)',
         'Triples (3B)', 'Home Runs (HR)', 'Runs Batted In (RBI)',
         'Stolen Bases (SB)', 'Caught Stealing (CS)', 'Walks (BB)',
         'Intentional Walk (IBB)', 'Salary', 'Attendance']

statchoices = [(s, s) for s in stats]

dir = os.path.split(__file__)[0]
players = pd.read_csv(os.path.join(dir, "baseball_data", "players.csv"))
teams = pd.read_csv(os.path.join(dir, "baseball_data", "teams.csv"))


class BaseballInput(panels.InputPanel):
    xvar = fields.SelectField(label="X axis", choices=statchoices,
                              default="Hits (H)")
    yvar = fields.SelectField(label="Y axis", choices=statchoices,
                              default="Runs (R)")

    year = fields.IntegerField(label="Year", default=2013)

    linear = fields.BooleanField(label="Linear Fit")
    shownames = fields.BooleanField(label="Show Names")


class DataScatter(panels.PlotPanel):
    height = 500
    width = 700

    def __init__(self, name, dat, ID_col):
        self.name = name
        self.dat = dat
        self.ID_col = ID_col
        panels.PlotPanel.__init__(self)

    def plot(self, inputs):
        """Plot the given X and Y axes on a scatter plot"""
        if inputs.year not in self.dat.Year.values:
            return

        if inputs.xvar not in self.dat or inputs.yvar not in self.dat:
            return

        subdat = self.dat[self.dat.Year == inputs.year]

        p = plt.plot(subdat[inputs.xvar], subdat[inputs.yvar])

        return p


class BaseballGleam(Page):
    title = "Baseball Statistics"
    input = BaseballInput()
    output = panels.TabPanel([DataScatter("Teams", teams, "teamID"),
                              DataScatter("Players", players, "name")])


app = Flask("BaseballGleam")
BaseballGleam.add_flask(app)
app.debug = True
app.run()
