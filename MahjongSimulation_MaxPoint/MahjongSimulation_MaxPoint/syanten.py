import copy

#シャンテン数テーブル
#左1つは雀頭,0:あり,1:なし
#右4つは面子,0:面子,1:面子候補,2:孤立
SYANTEN_TABLE=list([
    #[[1,2,2,2,2]],
    [[1,1,2,2,2],[0,2,2,2,2]],
    [[1,1,1,2,2],[1,0,2,2,2],[0,1,2,2,2]],
    [[1,1,1,1,2],[1,0,1,2,2],[0,1,1,2,2],[0,0,2,2,2]],
    [[1,1,1,1,1],[1,0,1,1,2],[1,0,0,2,2],[0,1,1,1,2],[0,0,1,2,2]],
    [[1,0,1,1,1],[1,0,0,1,2],[0,1,1,1,1],[0,0,1,1,2],[0,0,0,2,2]],
    [[1,0,0,1,1],[1,0,0,0,2],[0,0,1,1,1],[0,0,0,1,2]],
    [[1,0,0,0,1],[0,0,0,1,1],[0,0,0,0,2]],
    [[1,0,0,0,0],[0,0,0,0,1]],
    [[0,0,0,0,0]]
    ])

#シャンテン数計算
def Syanten(hand_list):
    #手札を枚数形式に変換
    hand_count_root=[0]*(9*3+7)
    for card in hand_list:
        hand_count_root[card//4]+=1

    #シャンテン数
    syanten=8
    #シャンテン数テーブル全てを探索
    for table_s in SYANTEN_TABLE:
        #検索完了フラグ
        search_flag=False
        #シャンテン数ごとのテーブルを取得
        for table in table_s:
            #雀頭の有無
            if table[0]==0:
                #雀頭探索
                for id in range(9*3+7):
                    #2枚以上存在
                    if hand_count_root[id]>=2:
                        #配列を値渡しでコピー
                        hand_count_copy=copy.deepcopy(hand_count_root)
                        #雀頭を抜き取る
                        hand_count_copy[id]-=2
                        #面子分解
                        if HandAnalyze(hand_count_copy,table,1):
                            #検索完了
                            search_flag=True
                            break
            else:
                #面子分解
                if HandAnalyze(hand_count_root,table,1):
                    #検索完了
                    search_flag=True
            #検索完了
            if search_flag:
                break
        #シャンテン数に該当する分解方法が存在
        if search_flag:
            syanten-=1
        else:
            #存在しない
            break
    #シャンテン数を返す
    return syanten

#手札の面子分解
def HandAnalyze(hand_count,table,depth):
    #配列を値渡しでコピー
    hand_count_copy=copy.deepcopy(hand_count)
    #最後まで分解可能なら終了
    if depth>=len(table):
        return True
    #探索不要なら終了
    if table[depth]==2:
        return True
    #面子候補
    if table[depth]==1:
        #刻子候補
        for id in range(9*3+7):
            #2枚以上存在
            if hand_count_copy[id]>=2:
                #候補を抜き取る
                hand_count_copy[id]-=2
                #さらに解析
                if HandAnalyze(hand_count_copy,table,depth+1):
                    #解析完了なら終了
                    return True
        #順子候補
        for color in range(3):
            #連続(12,56,89など)
            for num in range(8):
                index=color*9+num
                #各1枚以上存在
                if hand_count_copy[index]>=1 and hand_count_copy[index+1]>=1:
                    #該当カードを抜き取る
                    hand_count_copy[index]-=1
                    hand_count_copy[index+1]-=1
                    #さらに解析
                    if HandAnalyze(hand_count_copy,table,depth+1):
                        #解析完了なら終了
                        return True
            #離れている(13,57,79など)
            for num in range(7):
                index=color*9+num
                #各1枚以上存在
                if hand_count_copy[index]>=1 and hand_count_copy[index+2]>=1:
                    #該当カードを抜き取る
                    hand_count_copy[index]-=1
                    hand_count_copy[index+2]-=1
                    #さらに解析
                    if HandAnalyze(hand_count_copy,table,depth+1):
                        #解析完了なら終了
                        return True
    #面子
    else:
        #刻子
        for id in range(9*3+7):
            #3枚以上存在
            if hand_count_copy[id]>=3:
                #候補を抜き取る
                hand_count_copy[id]-=3
                #さらに解析
                if HandAnalyze(hand_count_copy,table,depth+1):
                    #解析完了なら終了
                    return True
        #順子
        for color in range(3):
            for num in range(7):
                index=color*9+num
                #各1枚以上存在
                if hand_count_copy[index]>=1:
                    if hand_count_copy[index+1]>=1:
                        if hand_count_copy[index+2]>=1:
                            #該当カードを抜き取る
                            hand_count_copy[index]-=1
                            hand_count_copy[index+1]-=1
                            hand_count_copy[index+2]-=1
                            #さらに解析
                            if HandAnalyze(hand_count_copy,table,depth+1):
                                #解析完了なら終了
                                return True
    #分解不可
    return False

