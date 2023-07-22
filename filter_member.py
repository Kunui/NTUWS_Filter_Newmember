import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

class admember():

    #引數讀取歡迎問卷（在前）總會員（在後）的檔案
    def __init__(self, welqmlist: str, ttmlist: str, qtlist: str) -> None:
       self.welqm =  pd.read_csv(welqmlist, encoding = 'utf-8')
       self.ttm = pd.read_csv(ttmlist, encoding = 'utf-8')
       self.qtm = pd.read_csv(qtlist, encoding = 'utf-8')
       self.welqm = self.welqm.rename(columns = {
            "您的信箱": "email",
            "您的手機號碼": "phone",
            "請輸入推薦您加入本平台的推薦人手機號碼（或訪員代碼），若無可直接進入下一頁": "recommender",
            "請問您的年齡": "AGE"
       })

       self.welqm = self.welqm[["email", "phone", "recommender", "AGE"]]
       #因原始檔案書處的資料格式緣故 兩份電話欄位皆需轉成字串操作
       self.welqm["phone"] = self.welqm["phone"].astype(str)
       #歡迎問卷電話為頭部不含0的整數 轉成字串後加回去
       self.welqm["phone"] = "0" + self.welqm["phone"]

       #隔離區樣本如上面操作
       self.qtm = self.qtm.rename(columns = {
            "您的信箱": "email",
            "您的手機號碼": "phone",
            "請輸入推薦您加入本平台的推薦人手機號碼（或訪員代碼），若無可直接進入下一頁": "recommender",
            "請問您的年齡": "AGE"
       })

       self.qtm = self.qtm[["email", "phone", "recommender", "AGE"]]
       self.qtm["phone"] = self.qtm["phone"].astype(str)
       self.qtm["phone"] = "0" + self.qtm["phone"]
       self.qtm["recommender"] = self.qtm["recommender"].astype(str)

       #先合併歡迎問卷與隔離區樣本
       self.welqm = pd.concat([self.welqm, self.qtm], axis = 0, ignore_index = True)

       self.ttm = self.ttm.rename(columns = {
            "姓名（暱稱）": "name",
            "電話": "phone",
            "信箱": "email",
            "年齡區間": "age",
            "城市": "city"
       })

       self.ttm = self.ttm[["name", "phone", "email", "age", "city"]]
       self.ttm["phone"] = self.ttm["phone"].astype(str)
       #受訪者根據是否滿50歲分成兩類
       self.ttm["age"] = self.ttm["age"].replace({
           "20-24": "youth",
           "25-29": "youth",
           "30-34": "youth",
           "35-39": "youth",
           "40-44": "youth",
           "45-49": "youth",
           "50-54": "elder",
           "55-59": "elder",
           "60-64": "elder",
           "65-69": "elder",
           "70以上": "elder",
       })
       #受訪者根據是否為大台北地區分成兩類
       self.ttm["city"] = self.ttm["city"].replace({
           "臺北市": "GTP",
           "新北市": "GTP",
           "基隆市": "NTP",
           "桃園市": "NTP",
           "新竹縣": "NTP",
           "新竹市": "NTP",
           "苗栗縣": "NTP",
           "臺中市": "NTP",
           "彰化縣": "NTP",
           "南投縣": "NTP",
           "雲林縣": "NTP",
           "嘉義縣": "NTP",
           "嘉義市": "NTP",
           "臺南市": "NTP",
           "高雄市": "NTP",
           "屏東縣": "NTP",
           "宜蘭縣": "NTP",
           "花蓮縣": "NTP",
           "臺東縣": "NTP",
           "澎湖縣": "NTP",
           "金門縣": "NTP",
           "連江縣": "NTP",
       })

       #訪員名單作為篩選器
       self.interviewer = [
        '101', '102', '401', '402', '403', '404', 
        '501', '502', '602', '603', '604',
        '701', '702','703','704', '705','706', '707', '708',
        '801', '802', '803'
        ]
    
    def get_filter(self):
        
        #先用推薦人篩選訪員獲取的歡迎問卷樣本
        recommender = self.welqm["recommender"].isin(self.interviewer)
        wqs = self.welqm[recommender]
        wqs.index = list(range(len(wqs))) #方便操作兩份檔案皆re_index
        #用篩好的歡迎問卷 再取其電話欄位 篩總會員數檔案
        tts = self.ttm[self.ttm["phone"].isin(wqs["phone"].to_list())]
        tts.index = list(range(len(tts)))
        return wqs, tts #回傳 訪員獲得的樣本 經過篩選過的 歡迎問卷（前）總會員（後）結果的物件
        #後續模組中的方法函式皆以這兩個物件操作
    
    def get_problem(self, wqs: pd.DataFrame, tts: pd.DataFrame):
        wqs = wqs.copy()
        #新增欄位存放電話號碼逐個比對 篩好的歡迎問卷與總會員的布林值
        wqs["comparison"] = wqs["phone"].isin(tts["phone"].to_list())
        #取出歡迎問卷有 但總會員沒有的電話號碼的 位置及同列特徵資訊
        problem = wqs.loc[wqs["comparison"] == False]
        problem = problem.drop(columns = "comparison", axis = 1)
        return problem

    def duplicate_number(self, wqs: pd.DataFrame):
        wqs = wqs.copy()
        #以groupby統計電話欄位的次數分配 並先找出不為1者在 統計次數中的判斷數列的 位置
        i = (wqs.groupby("phone").size() != 1).to_list().index(True)
        #以判斷數列的位置 找出不為1者的索引位置的值
        dup_num = wqs.groupby("phone").size().index[i]
        dup_num_df = wqs.loc[wqs["phone"] == dup_num]
        return dup_num_df
    
    def anti_dpnum(self, wqs: pd.DataFrame,  tts: pd.DataFrame):
        wqs = wqs.copy()
        tts = tts.copy()
        #以找重複電話門號的方法來刪
        dpnum = self.duplicate_number(wqs = wqs)
        #用總會員的email欄位比對 歡迎問卷重複但總會員只有一支的電話號碼 
        ttsnum = tts[tts["phone"].isin(dpnum["phone"].to_list())]
        i_series = dpnum["email"].isin(ttsnum["email"].to_list())
        #取得沒有在總會員email出現的 判斷式位置
        i = i_series.to_list().index(False)
        #用判斷式位置找出索引位置 再刪掉該列
        i = i_series.index.to_list()[i]
        anti_result = wqs.drop(index = i, axis = 0)
        return anti_result

    def sample_merge(self,  wqs: pd.DataFrame,  tts: pd.DataFrame):
        wqs = wqs.copy()
        tts = tts.copy()
        clean_wqs = self.anti_dpnum(wqs = wqs, tts = tts)
        merge_result = pd.merge(clean_wqs, tts, how = "inner", on = "phone")
        return merge_result
    
    def interviewers_performance(self, wqs: pd.DataFrame, tts: pd.DataFrame):
        wqs = wqs.copy()
        tts = tts.copy()
        total_sampleadd = self.sample_merge(wqs = wqs, tts = tts)
        #先求次數分配數列與取出特徵索引再合併成交叉分析表
        sum_series = total_sampleadd.groupby(["recommender", "age", "city"]).size()
        features = sum_series.index.to_frame()
        features.index = list(range(len(features)))
        sum_series.index = list(range(len(sum_series)))
        cross_table = pd.concat([features, sum_series], join = 'inner', axis = 1)
        cross_table.columns =  ["recommender", "age", "city", "frequency"]
        return cross_table
    
    def show_performance(self, wqs:pd.DataFrame, tts: pd.DataFrame):
        wqs = wqs.copy()
        tts = tts.copy()
        cross_table = self.interviewers_performance(wqs = wqs, tts = tts)
        #篩選訪員、年齡、城市三個條件 #先建容器再合併
        target_freq = []
        general_freq = []
        total_freq = []
        for n in self.interviewer:
            target_sum = sum(cross_table["frequency"].loc[(cross_table["recommender"] == n) &
                                                          (cross_table["age"] == "elder") &
                                                          (cross_table["city"] == "NTP")])
            target_freq.append(target_sum)
            general_sum = sum(cross_table["frequency"].loc[cross_table["recommender"] == n]) - target_sum
            general_freq.append(general_sum)
            total_sum = target_sum + general_sum
            total_freq.append(total_sum)
        #建立一個物件裝成功樣本次數
        self.indivisual_performance = pd.concat([
            pd.Series(self.interviewer, name = "recommender"),
            pd.Series(target_freq, name = "target_sample"),
            pd.Series(general_freq, name = "general_sample"),
            pd.Series(total_freq, name = "total_sample")],
            axis = 1)
        show_perf = self.indivisual_performance
        show_perf["general_sample"].loc[show_perf["general_sample"] >= 10] = "上限"
        show_perf = show_perf.drop(columns = "total_sample", axis = 1)
        return show_perf
    
    #把結果輸出成一個報表
    def export_result(self, wqs: pd.DataFrame, tts: pd.DataFrame, output: str):
        wqs = wqs.copy()
        tts = tts.copy()
        show_performance = self.show_performance(wqs = wqs, tts = tts)
        show_performance.columns = ["訪員編號", "目標樣本", "一般樣本"]
        result_table = show_performance.T
        #先取出均分的兩part 再垂直合併
        result_table_top = result_table.iloc[:, : 11]
        #把原本後半部的columns names去掉
        result_table_down = pd.DataFrame(result_table.iloc[:, 11: ].values, index = result_table.index)
        result_table = pd.concat([result_table_top, result_table_down], join = 'inner', axis =0)
        #把result_table先轉成2D list再轉成table
        result_table_list = result_table.values.tolist()
        #先設定中文字體以免亂碼
        matplotlib.rc("font", family = "Arial Unicode MS")
        #設定報表
        plt.figure()
        ax = plt.axes(frame_on = False)
        ax.axis('off')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        #設定表格顏色 分成編號、內容、索引四組色
        #先建一個裝各個顏色標籤字串的list 填滿一行編號與內容
        color_cell_names = ["royalblue", "aliceblue", "aliceblue"] *2
        #將顏色標籤水平延伸並裝進list
        color_cell = []
        for color in color_cell_names:
            color_cell.append([color] * 11)
        #設定索引的顏色裝進list 填滿一行
        color_index = ["cornflowerblue", "lightskyblue", "lightskyblue"] * 2
        #繪圖輸出
        ax.table(
            cellText = result_table_list,
            rowLabels = result_table.index,
            cellColours = color_cell,
            rowColours = color_index,
            edges = 'closed',
            loc = 'center',
            rowLoc = 'center',
            cellLoc = 'center',
            bbox = [0, 0, 1.5, 1]
        )
        export_path = f'{output}樣本進度.png'
        plt.savefig(export_path, bbox_inches = 'tight')
