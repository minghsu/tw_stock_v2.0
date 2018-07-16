#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from constant.analysis import AnalyzeFieldIdx
from pandas.core.frame import DataFrame
import pandas as pd
import os

DEF_STOCK_COULMN_NAME = ["Date", "Volumn", "Money", "Open",
                         "Max", "Min", "Close", "Spread", "Count"]

DEF_EXPORT_FOLDER_NAME = "exportfile"


def export_analyze_result(arg_filename, arg_data, arg_plugins, arg_result):
    if not os.path.exists(DEF_EXPORT_FOLDER_NAME):
        os.makedirs(DEF_EXPORT_FOLDER_NAME)

    main_data = DataFrame(list(arg_data))
    main_data.columns = DEF_STOCK_COULMN_NAME

    result_data = []
    result_data.append(main_data)
    result_data += arg_result

    df = pd.concat(result_data, axis=1)

    try:
        df.to_csv(DEF_EXPORT_FOLDER_NAME + os.sep +
                  arg_filename, sep=',', encoding='utf-8')
    except:
        return False

    return True
