from random import shuffle
import os

values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9,
        'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
suits = ['Clubs', 'Hearts','Spade','Diamonds']
ranks = ['Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']




class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.alldeckcards = []
        for suit in suits:
            for rank in ranks:
                self.alldeckcards.append(Card(suit, rank))

    def shuffle(self):
        shuffle(self.alldeckcards)

    def deal(self):
        return self.alldeckcards.pop(0)
        
    
    def show(self):
        for card in self.alldeckcards:
            print(card)    

class Hand:
    
    def __init__(self, name, money):        
        self.name = name
        self.money = money
        self.playercards = []
        
    
    def bet(self):
        
        p_bet = ''
        while p_bet.isdigit() == False:
            p_bet = input(f'Place you bet [{self.money} remaining ]: ')
            if p_bet.isdigit():
                p_bet = int(p_bet)
                if self.money >= p_bet:
                    self.money -= p_bet
                    return p_bet
                else:
                    print('Insufficient funds. Place smaller bet.')
                    p_bet =''
            elif p_bet.isdigit() == False:
                print('Place a digit please. Not some bunch of letters.')
                continue
    
    #applicable to player only
    def winmoney(self,amount):
        self.money += amount*2

    #applicable to player only when draw
    def moneyback(self,amount):
        self.money += amount
        
    #applicable to dealer only    
    def dealer_winmoney(self,amount):
        self.money += amount
    
    #applicable to dealer instance only
    def losemoney(self,amount):
        self.money -= amount

                
                
    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.playercards.extend(new_cards)
        else:
            self.playercards.append(new_cards)
        
    def __str__(self):
        return f'Player {self.name} has {self.money} amount of chips.'


def initialize_player():    
    
    #Input a name
    playername = '123456789012345678901'
    
    while int(len(playername)) > 20:
        playername = input('Input your name:')
        if int(len(playername)) > 20:
            print('Max name length is 20 char')
            continue
        else:
            break

   
    money = 1001
    while money < 50 or money > 1000:
        money = ''
        while type(money) == type(''):
            money = input('Input your initial money. 50-1000 only:')
            if money.isdigit():
                break
            else:
                print('Please enter a digit')
                continue
        money = int(money)
        if money > 1000 or money < 50:
            print('Money allowed is from 50-1000 only. Please try again.')
            continue
        else:
            break
            
            
    return playername,money


def deal_cards(deck):
    
    #deal 2 cards each
    for _x in range(2):
        player.add_cards(deck.deal())
        dealer.add_cards(deck.deal())
        

def show_cards_withhidden():
    print('Dealer\'s cards:')
    
    for i in range(len(dealer.playercards)):
        if i == 0:
            print('--Hidden Card--')
        else:
            print(dealer.playercards[i])
        
    print('--------------')
    print('Player\'s cards:')
    for j in range(len(player.playercards)):
        print(player.playercards[j])
        
    print('--------------')
   

def showall_cards():
    print('Dealer\'s cards:')
    
    for i in range(len(dealer.playercards)):
        print(dealer.playercards[i])
        
    print('--------------')
    print(f'{player.name}\'s cards:')
    for j in range(len(player.playercards)):
        print(player.playercards[j])
        
    print('--------------')


def player_hit_or_stand(deck):
    choices = ['hit','stand']
    choice = ''
    
    while choice not in choices:
        choice = input(f'{player.name}, do you like to hit or stand?:')
        choice = choice.lower()
        
    if choice == 'hit':
        player.add_cards(deck.deal())
        return True
    if choice == 'stand':
        return False

def dealer_hit(deck):
    dealer.add_cards(deck.deal())


def aceadjusted(player_dealer):
    
    #playercardsvalue including decision for Ace card.
    currentcardvalue = 0
    for i in player_dealer.playercards:
        currentcardvalue += i.value
    
    aces = []
    for i in player_dealer.playercards:
        if i.rank == 'Ace':
            aces.append('Ace')
    
    
    if currentcardvalue > 21 and len(aces) == 1:
        currentcardvalue -= 10
    elif currentcardvalue > 31 and len(aces) == 2:
        currentcardvalue -= 20
    elif currentcardvalue > 21 and len(aces) == 2:
        currentcardvalue -= 10
    elif currentcardvalue > 21 and len(aces) == 3:
        currentcardvalue -= 20
    elif currentcardvalue > 21 and len(aces) == 4:
        currentcardvalue -= 30        
    else:
        return currentcardvalue
        
    return currentcardvalue


def playercheckforbust(value,player_dealer):

        
    if value > 21:
        print(f'{player_dealer.name} is bust')
        return True
    else:
        print(f'{player_dealer.name} card is good')
        return False

def dealer_decision(playercardvalue, deck):
    
    #currentplayer value
    playercurrentvalue = playercardvalue
    dealercurrentvalue = 0    
    dealercurrentvalue = aceadjusted(dealer)
    is_bust = False    
    
    while dealercurrentvalue < 21 and dealercurrentvalue <= playercurrentvalue:
        dealer_hit(deck)
        dealercurrentvalue = aceadjusted(dealer)
        is_bust = playercheckforbust(dealercurrentvalue,dealer)
        
    return playercurrentvalue,dealercurrentvalue,is_bust
    


def checkforwinner(playervalue,dealervalue,bust,bet):
    
    
    if bust:
        print(f'Dealer is bust. {player.name} won!')
        print('--------------')
        showall_cards()
        betwinning(bet, p_player = True, d_dealer = False)
        print(f'{player.name} won {bet}. His/Her\'s total money is now {player.money}')
        replay = playagain()
        if replay:
            #clear_output()
            screen_clear()
            #print('Dealing new cards')
            return True
        else:
            return False
    elif playervalue == dealervalue and bust == False:
        print(f'{player.name} and dealer is draw!')
        print('--------------')
        showall_cards()
        player.moneyback(bet)
        replay = playagain()
        if replay:
            #clear_output()
            screen_clear()
            #print('Dealing new cards')
            return True
        else:
            return False
    elif playervalue > dealervalue and bust == False:
        print(f'{player.name} cards is greater than the dealer. {player.name} won!')
        print('--------------')
        showall_cards()
        betwinning(bet, p_player = True, d_dealer = False)
        print(f'{player.name} won {bet}. His/Her\'s total money is now {player.money}')
        replay = playagain()
        if replay:
            #clear_output()
            screen_clear()
            #print('Dealing new cards')
            return True
        else:
            return False
    else:
        print(f'Dealer cards is greater than {player.name}. Dealer won!')
        print('--------------')
        showall_cards()
        betwinning(bet, p_player = False, d_dealer = True)
        print(f'Dealer won {bet}. Dealer\'s total money is now {dealer.money}')
        replay = playagain()
        if replay:
            #clear_output()
            screen_clear()
            #print('Dealing new cards')
            return True
        else:
            return False


def playagain():
    
    playagainchoices = ['yes','no']
    playagainchoice = ''
    
    while playagainchoice not in playagainchoices:
        playagainchoice = input('Do you want to play again?')
        playagainchoice = playagainchoice.lower()
        
    if playagainchoice =='yes':            
        return True
    else:
        return False
        

#def deal_restart():
    
 #   player.playercards = []
 #   dealer.playercards = []
 #   game_start()


def betwinning(bet, p_player = False, d_dealer = False):
    
    if p_player == True:
        player.winmoney(bet)
        dealer.losemoney(bet)
        
    elif d_dealer == True:
        dealer.dealer_winmoney(bet)


def screen_clear():

   # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
      # for windows platfrom
        _ = os.system('cls')
   # print out some text
        
    
def game_start():
    
    global player
    global dealer

    newdeck = Deck()
    newdeck.shuffle()   

    player.playercards = []
    dealer.playercards = []

    game_on = True

   
    if player.money == 0 and  dealer.money != 0 and game_on:
            print(f'{player.name} is bankrupt.')
            replay = playagain()
            if replay:
                initialize = initialize_player()
                player = Hand(initialize[0], initialize[1])
                game_start()
            else:
                print('Thanks for playing BlackJack!')
                game_on = False
             
    
    if dealer.money == 0 and  player.money != 0 and game_on:
            print(f'{dealer.name} is bankrupt.')
            replay = playagain()
            if replay:
                dealer.money = 1000
                game_start()
            else:
                print('Thanks for playing BlackJack!')
                game_on = False
           
    
    while player.money != 0 and dealer.money != 0 and game_on:
        
    
        



        #place bet
        p_bet = player.bet()
    
        #deals 2 cards
        deal_cards(newdeck)
    
        #print dealing new cards
        print('Dealing new cards')
    
        #shows cards in hand
        show_cards_withhidden()
      
        #asks the player to continually hit or stand until satisfied
        hit = True
        while hit:
            hit = player_hit_or_stand(newdeck)
            #clear_output()
            screen_clear()
            show_cards_withhidden()
            
            #value of cards in hand with ace adjusted
            playercardvalue=aceadjusted(player)
    
            #check if bust
            player_bust = playercheckforbust(playercardvalue, player)
            if player_bust:
                hit = False
                break
            else:
                continue
            
                
        if hit == False and player_bust == True:
            print(f'{player.name} is bust. Dealer won!')
            betwinning(p_bet, p_player = False, d_dealer = True, )
            print(f'Dealer won {p_bet}. Dealer\'s total money is now {dealer.money}')
            replay = playagain()
            if replay:
                #clear_output()
                screen_clear()
                game_start()                
            else:
                print('Thanks for playing BlackJack!')
                game_on = False
                player.money = 0 
                dealer.money = 0
                
        elif hit == False and player_bust == False:
            #check for dealer's play
            output = dealer_decision(playercardvalue, newdeck)
            replay = checkforwinner(output[0],output[1],output[2],p_bet)
            if replay:
                screen_clear()
                game_start()
            else:                
                print('Thanks for playing BlackJack!')
                game_on = False
                player.money = 0 
                dealer.money = 0               



    
            

    
            




if __name__=="__main__":
    initialize = initialize_player()
    player = Hand(initialize[0], initialize[1])
    dealer = Hand('Dealer',1000)

    game_start()


