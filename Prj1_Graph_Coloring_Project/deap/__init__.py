"""Minimal DEAP-compatible shim for the CSE 568 Project 01 autograder.

This is not a full DEAP replacement. It implements only the small subset used
by the Project 01 template/reference solution: base.Toolbox, base.Fitness,
creator.create, tools.initRepeat, tools.cxTwoPoint, tools.mutFlipBit,
tools.selTournament, tools.HallOfFame, and algorithms.eaSimple.
"""

from . import algorithms, base, creator, tools

__all__ = ["algorithms", "base", "creator", "tools"]
