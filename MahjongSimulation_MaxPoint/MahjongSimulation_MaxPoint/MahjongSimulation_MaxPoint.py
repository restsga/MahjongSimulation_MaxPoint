import random
import syanten

#プレイヤー数
PLAYER_COUNT=4

#シード値を決定
random.seed(2**10-1)

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

#捨て札をランダムに選択
def Discard_Random(hand_list,discard_lists):

    print("シャンテン数:"+str(syanten.Syanten(hand_list)))

    return random.randrange(14)

#シミュレーションによる捨て札選択
def Discard_Simulation(hand_list,discard_lists):
    #シミュレーション用の山札
    deck_sim=list(range((9*3+7)*4))

    #手札を除外
    for card in hand_list:
        deck_sim.remove(card)
    #捨て札を除外
    for discard in discard_lists:
        for card in discard:
            deck_sim.remove(card)

    print("deck_sim:"+CardIdToString(deck_sim))

    #山札をシャッフル
    random.shuffle(deck_sim)

    print("deck_sim:"+CardIdToString(deck_sim))

    return 13

#AIの思考ルーチン
AI=[Discard_Simulation,Discard_Random,Discard_Random,Discard_Random]

#無限にシミュレーション
while True:

    #山札生成
    deck_real=random.sample(list(range((9*3+7)*4)),(9*3+7)*4)

    print("山札")
    print(str(deck_real))

    #手札
    hand_real=[]
    #捨て札
    discard_real=[]
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

    print("手札")
    print(str(hand_real))
    print("山札")
    print(str(deck_real))
    print()

    ##対戦用変数##
    #手番
    turn=0

    #対戦開始
    while len(deck_real)>14:
        #1枚引く
        draw=deck_real.pop()
        hand_real[turn].append(draw)
        hand_real[turn].sort()
        
        print("ドロー:"+CARD_STRING[draw//4]+",PL"+str(turn))
        print(str(hand_real[turn]))
        print(CardIdToString(hand_real[turn]))

        #1枚捨てる
        hand_real[turn].sort()
        discard_id= hand_real[turn].pop(AI[turn](hand_real[turn],discard_real))
        discard_real[turn].append(discard_id)

        print("捨て札:"+CARD_STRING[discard_id//4]+",PL"+str(turn))
        print(str(hand_real[turn]))
        print(CardIdToString(hand_real[turn]))
        print(CardIdToString(discard_real[turn]))
        print()

        #手番移動
        turn=(turn+1)%PLAYER_COUNT

    #終了
    break