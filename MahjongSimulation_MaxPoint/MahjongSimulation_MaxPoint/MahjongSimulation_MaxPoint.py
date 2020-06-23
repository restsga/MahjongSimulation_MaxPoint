import random
import copy
import syanten

#プレイヤー数
PLAYER_COUNT=4

#シード値を決定
random.seed(2**20-1)

#シミュレーション時の鳴き確率
CALL_P=0.5

#カード文字列
CARD_STRING=list([
    "1m","2m","3m","4m","5m","6m","7m","8m","9m",
    "1p","2p","3p","4p","5p","6p","7p","8p","9p",
    "1s","2s","3s","4s","5s","6s","7s","8s","9s",
    "to","na","sy","pe","wh","gr","re"])

#カード表示
def CardIdToString(list):
    #表示用文字列
    message=""
    #文字列に変換
    for card in list:
        message+=CARD_STRING[card//4]
    #結果を返す
    return message

#捨て札をシャンテン数が下がらないように選択
def Discard_Syanten(hand_list,discard_list,call_lists,player):
    #捨て札をする前のシャンテン数
    syanten_root=syanten.Syanten(hand_list)

    #捨て札検索
    for i in random.sample(range(len(hand_list)),len(hand_list)):
        #配列を値渡しでコピー
        hand_copy=copy.deepcopy(hand_list)
        #捨て札してみる
        hand_copy.pop(i)
        #シャンテン数が変わらないならそれを捨てる
        if syanten.Syanten(hand_copy)==syanten_root:
            return i
    #実行されない
    return 100

#シミュレーションによる捨て札選択
def Discard_Simulation(hand_list,discard_lists,call_lists,player):
    #シミュレーション用の山札
    deck_sim_root=[i for i in range((9*3+7)*4)]

    #手札を除外
    for card in hand_list:
        deck_sim_root.remove(card)
    #捨て札を除外
    for discard in discard_lists:
        for card in discard:
            deck_sim_root.remove(card)
    #鳴き札を除外
    for calls in call_lists:
        for card in calls:
            deck_sim_root.remove(card)

    #成功回数カウンタ
    win_counts=list([0]*len(hand_list))
    #シミュレーション回数カウンタ
    sim_counts=list([0]*len(hand_list))
    sim_count_all=0

    #捨て札候補リスト
    will_discard_index=WillDiscardIndex_Syanten(hand_list)

    #確率が収束する程度の回数繰り返す
    while True:
        #第1手目の捨て札を決定
        r_1=random.randrange(0,len(will_discard_index))
        i=will_discard_index[r_1]
        #配列を値渡しでコピー
        hand_copy=copy.deepcopy(hand_list)
        call_copy=copy.deepcopy(call_lists[player])
        #捨て札する
        hand_copy.pop(i)
        #山札をシャッフル
        deck_sim_copy=random.sample(deck_sim_root,len(deck_sim_root))
        #手番
        turn=0
        #流局までシミュレーション
        while len(deck_sim_copy)>14:
            #手番移動
            turn=(turn+1)%PLAYER_COUNT
            #自分以外
            if turn!=0:
                #引いたカードを直接捨て札とする
                discard_id=deck_sim_copy.pop()
                #枚数カウント
                count=1
                for card in hand_copy:
                    if card//4==discard_id//4:
                        count+=1
                #鳴き判定
                if count>=3:
                    #鳴き実行
                    if random.random()<CALL_P:
                        #鳴き札に追加
                        call_copy.append(list([discard_id]*3))
                        #手札から削除
                        hand_copy=[id for id in hand_copy if not discard_id//4==id//4]
                        #捨て札候補生成
                        will_discard_rand=range(len(hand_copy))
                        #捨て札する
                        r=random.randrange(0,len(will_discard_rand))
                        hand_copy.pop(will_discard_rand[r])
                        #手番を強制移動
                        turn=0
            #自分の手番
            else:
                #カードを引く
                hand_copy.append(deck_sim_copy.pop())
                #勝利
                if syanten.Syanten(hand_copy)==-1:
                    #勝利回数カウント
                    win_counts[i]+=1
                    #シミュレーション回数カウント
                    sim_counts[i]+=1
                    sim_count_all+=1
                    #終了
                    break
                #捨て札候補生成
                will_discard_rand=range(len(hand_copy))
                #捨て札する
                r=random.randrange(0,len(will_discard_rand))
                hand_copy.pop(will_discard_rand[r])
        #シミュレーション回数カウント
        sim_counts[i]+=1
        sim_count_all+=1

        if sim_count_all%100==0:
            print(str(sim_count_all/10)+"%")

        #シミュレーション回数が規定値を超えた
        if sim_count_all>=1000:
            #終了
            break

    #勝率
    win=[win_counts[i]/(sim_counts[i]+0.001) for i in range(len(hand_list))]

    print(win)

    #勝利1以上のindexが存在
    if sum(win_counts)>0:
        #最大値のindexを返す
        return win.index(max(win))

    #シミュレーション結果では判定できないので別の方法で捨て札を選択
    return Discard_MaybeYakuman(hand_list,discard_lists,call_lists,player)

#役満が出やすそうなものを切る
def Discard_MaybeYakuman(hand_list,discard_lists,call_lists,player):
    #手札を枚数形式に変換
    hand_count=syanten.HandToCount(hand_list)
    #探索
    for i in random.sample(range(len(hand_list)),len(hand_list)):
        #1枚しか存在しないカードを捨てる
        card=hand_list[i]
        if hand_count[card//4]==1:
            #ただし19字は除外
            if card//4<3*9 and (card//4)%9!=0 and (card//4)%9!=8:
                #条件を満たすものを抽出
                result=[id for id in hand_list if id//4==card//4]
                #indexに変換して返す
                return hand_list.index(result[0])
    #どうしようもないので通常のシャンテン数に基づいて返す
    return Discard_Syanten(hand_list,discard_lists,call_lists,player)

#シャンテン数を元にした捨て札候補
def WillDiscardIndex_Syanten(hand_list):
    #捨て札候補リスト
    will_discard_index=[]
    #シャンテン数が確実に悪化するものを除去
    for i in range(len(hand_list)):
        #配列を値渡しでコピー
        hand_copy=copy.deepcopy(hand_list)
        #捨て札
        hand_copy.pop(i)
        #シャンテン数が悪化
        if syanten.Syanten(hand_list)<syanten.Syanten(hand_copy):
            if syanten.Syanten_Kokushi(hand_list)<syanten.Syanten_Kokushi(hand_copy):
                continue
        #シャンテン数に問題が無い
        will_discard_index.append(i)
    return will_discard_index

#門前AI
def No_Call():
    return False

#AIの思考ルーチン
AI=[Discard_MaybeYakuman,Discard_Syanten,Discard_Syanten,Discard_Syanten]
AI_call=[No_Call,No_Call,No_Call,No_Call]

#カウンタ
count=0
#シャンテンカウンタ
syanten_counts=[0,0,0,0,0,0,0,0,0,0]
#無限にシミュレーション
while True:

    #カウンタ増加
    count+=1
    #山札生成
    deck_real=random.sample(list(range((9*3+7)*4)),(9*3+7)*4)

    #手札
    hand_real=[]
    #捨て札
    discard_real=[]
    #鳴き札
    call_real=[]
    #プレイヤー数分繰り返す
    for p in range(PLAYER_COUNT):
        #プレイヤーの初期手札
        hand_start=[]
        #初期手札の枚数分繰り返す
        for i in range(13):
            hand_start.append(deck_real.pop())
        #生成した手札を保存
        hand_real.append(hand_start)
        #捨て札を初期化
        discard_real.append([])
        #鳴き札を初期化
        call_real.append([])

    ##対戦用変数##
    #手番
    turn=0
    #鳴きプレイヤー
    call_id=-1

    #対戦開始
    while len(deck_real)>14:
        #鳴きなし
        if call_id==-1:
            #1枚引く
            draw=deck_real.pop()
            hand_real[turn].append(draw)
            hand_real[turn].sort()
        
            #勝利
            if syanten.Syanten(hand_real[turn])==-1:
                print("ツモ！,PL:"+str(turn))
                break

        #1枚捨てる
        hand_real[turn].sort()
        discard_id= hand_real[turn].pop(AI[turn](hand_real[turn],discard_real,call_real,turn))
        discard_real[turn].append(discard_id)

        #鳴きプレイヤーを初期化
        call_id=-1
        #鳴き
        for p in range(PLAYER_COUNT):
            #手番プレイヤーは鳴き不可
            if p!=turn:
                #枚数カウント
                hand_count=1
                for card in hand_real[p]:
                    hand_count+=1 if card//4==discard_id//4 else 0
                #鳴き可能
                if hand_count>=3:
                    #AIの判断
                    if AI_call[p]():
                        #鳴き札に追加
                        call_real[p].append(list([discard_id]*3))
                        #捨て札から削除
                        discard_real[turn].pop()
                        #手札から削除
                        hand_real[p]=[id for id in hand_real[p] if not discard_id//4==id//4]
                        
                        #鳴きの実行を保存
                        call_id=p
                        #終了
                        break

        #手番移動
        if call_id==-1:
            #鳴きなし
            turn=(turn+1)%PLAYER_COUNT
        else:
            #鳴きあり
            turn=call_id

    #シャンテン数を保存
    last_syanten=syanten.Syanten(hand_real[0])
    syanten_counts[last_syanten+1]+=1

    print(CardIdToString(hand_real[0]))
    print(CardIdToString(discard_real[0]))
    print(str(last_syanten))
    print(str(syanten_counts[0]*100/count)+"%")
    print(str(syanten_counts[1]*100/count)+"%")
    print(str(syanten_counts[2]*100/count)+"%")
    print(str(syanten_counts[3]*100/count)+"%")
    print("sample:"+str(count))
    print("====================終局====================")
    