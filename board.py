#!/usr/bin/env python
# -*-coding:utf8-*-
import numpy as np


class Cell(object):
    def __init__(self, problemcell, input, memo):
        self.problemcell = problemcell
        self.memo = memo
        self.input = input

    def __eq__(self, other):
        return type(self) == type(other) and \
            (self.problemcell, self.input) == (other.problemcell, other.input)\
            and all(self.memo == other.memo)

    @property
    def type(self):
        if self.problemcell.isfixed:
            return 'fixed'
        elif self.input != 0:
            return 'inputed'
        elif any(self.memo):
            return 'memo'
        else:
            return 'empty'

    @property
    def num(self):
        if self.type == 'fixed':
            return self.problemcell.pnum
        elif self.type == 'inputed':
            return self.input

    @property
    def iscorrect(self):
        return self.problemcell.snum == self.input


class Board(object):
    def __init__(self, problem):
        self._problem = problem
        size = problem.size

        self.input = np.ndarray((size,)*2)
        self.memo = np.ndarray((size,)*3, dtype='bool')
        self.memo.fill(False)

    @property
    def size(self):
        return self._problem.size

    def setmemo(self, pos, num, check):
        self.memo[pos][num] = check

    def setinput(self, pos, num):
        self.input[pos] = num

    def __getitem__(self, pos):
        return Cell(
            self._problem[pos],
            self.input[pos],
            self.memo[pos])

    @property
    def solution(self):
        return self._problem.solution

    @property
    def problem(self):
        return self._problem.problem

    @property
    def issolved(self):
        return all(
            self[i, j].iscorrect
            for i in xrange(0, self.size)
            for j in xrange(0, self.size))


class ProblemCell(object):
    def __init__(self, pnum, snum):
        self.pnum = pnum
        self.snum = snum

    @property
    def isfixed(self):
        return self.pnum != 0

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Problem(object):
    @property
    def size(self):
        return len(self.problem)

    def __init__(self, problem, solution):
        self.problem = problem
        self.solution = solution

    @classmethod
    def loads(cls, problem_str, solution_str, size):
        problem = cls.__str_to_ndarray(problem_str, size)
        solution = cls.__str_to_ndarray(solution_str, size)
        return cls(problem, solution)

    @classmethod
    def __str_to_ndarray(cls, string, size):
        return np.array([int(i) for i in string]).reshape(size, size)

    def __getitem__(self, pos):
        return ProblemCell(self.problem[pos], self.solution[pos])
