'''

x..
.x.
o..

. - 0
x - 1
o - 2

'''
import sys
from random import choice
sys.setrecursionlimit(1<<18)

maxn = 1<<18
dp=[-1 for _ in range(maxn)]
move=[[] for _ in range(maxn)]

def inverse(mask):
    res=0
    for i in range(9):
        v=(3-(mask>>(2*i)&3))%3
        res|=v<<(2*i)
    return res

wins = [[0,1,2], [3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0, 4, 8],[2,4,6]]

def calc(mask):
    if dp[mask]!=-1:
        return
    mx = -1
    moves = []
    for i in range(9):
        v = mask>>(2*i)&3
        if v==3:
            return

    for win in wins:
        if mask>>(win[0]*2)&3==1 and mask>>(win[1]*2)&3==1 and mask>>(win[2]*2)&3==1:
            dp[mask]=2
            return
        if mask>>(win[0]*2)&3==2 and mask>>(win[1]*2)&3==2 and mask>>(win[2]*2)&3==2:
            dp[mask]=0
            return

    for i in range(9):
        v = mask>>(2*i)&3
        if v==0:
            new = mask | (1<<(2*i))
            calc(inverse(new))
            if 2-dp[inverse(new)] > mx:
                mx = 2-dp[inverse(new)]
                moves=[new]
            elif 2-dp[inverse(new)] == mx:
                moves.append(new)
            
    if mx==-1:
        dp[mask]=1
        return
    dp[mask] = mx
    move[mask] = moves

def field_to_state(s):
    s=s.replace('\n', '').replace(' ', '')
    res=0
    for i in range(9):
        if s[i]=='x':
            res|=1<<(2*i)
        elif s[i]=='o':
            res|=2<<(2*i)
    return res

def state_to_field(mask):
    s=''
    for i in range(9):
        s+='.xo'[mask>>(2*i)&3]
        if i%3==2:
            s+='\n'
    return s

def precalc():
    for i in range(maxn):
        calc(i)

if __name__ == '__main__':
    print('Вы играете за крестики. Ход обозначается цифрой от 1 до 9: номер клетки в порядке чтения строк')
    print('Предподсчет ходов...')
    precalc()
    state=0
    if input('Чей первый ход? (1 - ваш, 2 - оппонент): ').strip() == '2':
        state = inverse(choice(move[state]))

    while 1:
        print(f'Текущее поле: \tПредикт: {["lose", "draw", "win"][dp[state]]}')
        print(state_to_field(state))
        if not move[state]:
            print('End.')
            break
        cur=-1
        while cur < 0 or cur > 8 or state>>(cur*2)&3!=0:
            cur = int(input('Ваш ход: '))
            cur-=1
        state |= 1<<(2*cur)
        if not move[state]:
            print('End.')
            break
        print('Ход оппонента')
        state = inverse(choice(move[inverse(state)]))
