# -*- coding: utf-8 -*-
"""Training schedulers.

This module contains classes implementing schedulers which control the
evolution of learning rule hyperparameters (such as learning rate) over a
training run.
"""

import numpy as np
import math


class ConstantLearningRateScheduler(object):
    """Example of scheduler interface which sets a constant learning rate."""

    def __init__(self, learning_rate):
        """Construct a new constant learning rate scheduler object.

        Args:
            learning_rate: Learning rate to use in learning rule.
        """
        self.learning_rate = learning_rate

    def update_learning_rule(self, learning_rule, epoch_number):
        """Update the hyperparameters of the learning rule.

        Run at the beginning of each epoch.

        Args:
            learning_rule: Learning rule object being used in training run,
                any scheduled hyperparameters to be altered should be
                attributes of this object.
            epoch_number: Integer index of training epoch about to be run.
        """
        learning_rule.learning_rate = self.learning_rate

class CosineAnnealingWithWarmRestarts(object):
    """Cosine annealing scheduler, implemented as in https://arxiv.org/pdf/1608.03983.pdf"""

    def __init__(self, min_learning_rate, max_learning_rate, total_iters_per_period, max_learning_rate_discount_factor,
                 period_iteration_expansion_factor):
        """
        Instantiates a new cosine annealing with warm restarts learning rate scheduler
        :param min_learning_rate: The minimum learning rate the scheduler can assign
        :param max_learning_rate: The maximum learning rate the scheduler can assign
        :param total_epochs_per_period: The number of epochs in a period
        :param max_learning_rate_discount_factor: The rate of discount for the maximum learning rate after each restart i.e. how many times smaller the max learning rate will be after a restart compared to the previous one
        :param period_iteration_expansion_factor: The rate of expansion of the period epochs. e.g. if it's set to 1 then all periods have the same number of epochs, if it's larger than 1 then each subsequent period will have more epochs and vice versa.
        """
        self.min_learning_rate = min_learning_rate
        self.max_learning_rate = max_learning_rate
        self.total_epochs_per_period = total_iters_per_period

        self.max_learning_rate_discount_factor = max_learning_rate_discount_factor
        self.period_iteration_expansion_factor = period_iteration_expansion_factor


    def update_learning_rule(self, learning_rule, epoch_number):
        """Update the hyperparameters of the learning rule.

        Run at the beginning of each epoch.

        Args:
            learning_rule: Learning rule object being used in training run,
                any scheduled hyperparameters to be altered should be
                attributes of this object.
            epoch_number: Integer index of training epoch about to be run.
        """
        
        
        self.Ti = []
        max_learning_rate_temp = self.max_learning_rate
        total_ti = self.total_epochs_per_period
        a = self.period_iteration_expansion_factor
        for i in range(100000): 
            if np.sum(self.Ti)+self.total_epochs_per_period*(a**(i)) < epoch_number and np.sum(self.Ti)+self.total_epochs_per_period*(a**(i))+self.total_epochs_per_period*(a**(i+1)) < epoch_number:
                self.Ti.append(self.total_epochs_per_period*(a**(i)) )
                max_learning_rate_temp = max_learning_rate_temp * self.max_learning_rate_discount_factor
            elif np.sum(self.Ti)+self.total_epochs_per_period*(a**(i)) < epoch_number and np.sum(self.Ti)+self.total_epochs_per_period*(a**(i))+self.total_epochs_per_period*(a**(i+1)) > epoch_number:
                self.Ti.append(self.total_epochs_per_period*(a**(i)))
                total_ti = self.total_epochs_per_period*(a**(i+1))
                max_learning_rate_temp = max_learning_rate_temp * self.max_learning_rate_discount_factor
                break 
            elif np.sum(self.Ti)+self.total_epochs_per_period*(a**(i))+self.total_epochs_per_period*(a**(i+1)) == epoch_number:
                self.Ti.append(self.total_epochs_per_period*(a**(i)))
                self.Ti.append(self.total_epochs_per_period*(a**(i+1)))
                total_ti = self.total_epochs_per_period*(a**(i+2))
                max_learning_rate_temp = max_learning_rate_temp * (self.max_learning_rate_discount_factor**2)
                break 
            elif np.sum(self.Ti)+self.total_epochs_per_period*(a**(i)) == epoch_number:
                self.Ti.append(self.total_epochs_per_period*(a**(i)))
                total_ti = self.total_epochs_per_period*(a**(i+1))
                max_learning_rate_temp = max_learning_rate_temp * self.max_learning_rate_discount_factor
                break
            else:
                break
        Tcur = epoch_number - np.sum(self.Ti) 
        update_learning_rate = self.min_learning_rate + 0.5*(max_learning_rate_temp - self.min_learning_rate)* (1+math.cos(math.pi*Tcur/total_ti))

        # self.max_learning_rate = self.max_learning_rate * self.max_learning_rate_discount_factor
        #self.total_epochs_per_period = self.total_epochs_per_period*self.period_iteration_expansion_factor
        # self.i += 1 
        return update_learning_rate
        
        
     



