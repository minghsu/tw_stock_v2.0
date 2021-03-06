#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from multiprocessing import Process
from .. baseanalysis import BaseAnalyer
from constant.stock import Info, RetriveType, StockDataField
from enum import Enum, unique
from pandas.core.frame import DataFrame

import pandas as pd


@unique
class ResultField(Enum):
    IDX_K = 0
    IDX_D = 1
    IDX_J = 2


class kdj(Process, BaseAnalyer):
    def __init__(self, arg_share_data, arg_queue, **kwargs):
        super(kdj, self).__init__()
        self.__data = arg_share_data
        self.queue = arg_queue

        # default parameters
        self.__fast_k_period = 9
        self.__slow_k_period = 3
        self.__slow_d_period = 3

        # update parameters if provided
        for key in kwargs:
            if key == "fast_k_period":
                self.__fast_k_period = kwargs[key]
            elif key == "slow_k_period":
                self.__slow_k_period = kwargs[key]
            elif key == "slow_d_period":
                self.__slow_d_period = kwargs[key]

    def analysis_name(self):
        return "K/D/J"

    def colnum_info(self):
        return ("K", "D", "J")

    def get_max_min_value(self, arg_idx):
        ret_max = float(self.__data[arg_idx]
                        [StockDataField.IDX_MAX.value])
        ret_min = float(self.__data[arg_idx]
                        [StockDataField.IDX_MIN.value])

        for j in range(arg_idx - self.__fast_k_period + 1, arg_idx + 1):
            if ret_max < float(self.__data[j][StockDataField.IDX_MAX.value]):
                ret_max = float(self.__data[j][StockDataField.IDX_MAX.value])
            if ret_min > float(self.__data[j][StockDataField.IDX_MIN.value]):
                ret_min = float(self.__data[j][StockDataField.IDX_MIN.value])

        return (ret_max, ret_min)

    def run(self):
        super(kdj, self).delay()

        # K, D, J
        self.__df_result = DataFrame([[0, 0, 0]] * len(self.__data))

        for i in range(len(self.__data)):
            if (i < self.__fast_k_period - 1):
                pass
            elif (i == self.__fast_k_period - 1):
                self.__df_result.iloc[[i], [ResultField.IDX_K.value]] = 50
                self.__df_result.iloc[[i], [ResultField.IDX_D.value]] = 50
                self.__df_result.iloc[[i], [ResultField.IDX_J.value]] = 50
            else:
                max, min = self.get_max_min_value(i)
                rsv = float(
                    100*(float(self.__data[i][StockDataField.IDX_CLOSE.value])-min)/(max-min))

                k_val = float('%.2f' % ((1/self.__slow_k_period) *
                                        rsv + (2/self.__slow_k_period) * self.__df_result[ResultField.IDX_K.value].values[i-1]))
                d_val = float('%.2f' % ((1/self.__slow_d_period) *
                                        k_val + (2/self.__slow_d_period) * self.__df_result[ResultField.IDX_D.value].values[i-1]))
                j_val = float('%.2f' % ((d_val*3) - (k_val*2)))
                self.__df_result.iloc[[i], [ResultField.IDX_K.value]] = k_val
                self.__df_result.iloc[[i], [ResultField.IDX_D.value]] = d_val
                self.__df_result.iloc[[i], [ResultField.IDX_J.value]] = j_val

        self.__df_result.columns = self.colnum_info()

        self.queue.put(
            [RetriveType.DATA, self.__df_result])
        self.queue.put(
            [RetriveType.INFO, [self.analysis_name(), Info.INFO_CALCULATED]])
