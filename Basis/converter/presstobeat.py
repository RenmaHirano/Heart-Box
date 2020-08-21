import math

class Presstobeat():
    beat = 0 # 出力される心拍数
    
    def __init__(self,press): # press = 送られてきた圧力値(0-1023)
        self.beat =  math.exp(press/125.0) * (90/3500) + 60 # 関数のグラフはBasis/converter/graph.xlsxを参照



p = Presstobeat(950.0)
print(p.beat)