import sys
import pygame
from pygame.locals import *
pygame.font.init()
import random

french = []
english = []

file = open("./french/metiers.txt", "r", errors="ignore")
content = file.readlines()
size = len(content)

replace_1 = ["\n", "Ã©", "Ã\xa0", "ã¨", "Ã´", "Ã¨"] #replace bad stuff
replace_2 = ["", "é", "à", "è", "ô", "è"]

for line in content:
    for i in range(0, len(replace_1)):
        line = line.replace(replace_1[i], replace_2[i])
    words = line.split(": ")
    french.append(words[0])
    english.append(words[1])

#print(french)

dx,dy = 800,200
color_a = pygame.Color(200,200,200)
color_i = pygame.Color(190,190,190)
color1 = pygame.Color(245,245,245)
color2 = pygame.Color(100,100,100)
pygame.init()
display = pygame.display.set_mode((dx,dy))
display.fill(color1)
fps = pygame.time.Clock()
fps.tick(60)
font = pygame.font.SysFont("courier new", 30)
font2 = pygame.font.SysFont("courier new", 50)
e_list = ["e", "é", "è", "ê", "ë"]
o_list = ["o", "ô", "œ"]
c_list = ["c", "ç"]
u_list = ["u", "ù", "û", "ü"]
y_list = ["y", "ÿ"]
a_list = ["a", "à", "â", "æ"]
i_list = ["i", "ï", "î"]

scroll_list = e_list + o_list + c_list + u_list + y_list + a_list + i_list

def scroll(letter):
    l = []
    lists = [e_list, o_list, c_list, u_list, y_list, a_list, i_list]
    for list in lists:
        if letter in list:
            l = list

    r = ""
    if l.index(letter) == (len(l) - 1):
        r = l[0]
    else:
        r = l[l.index(letter) + 1]

    return r

def stop():
    pygame.quit()
    sys.exit

def process(inpt, word):
    inpt = inpt.lower()
    word = word.lower()
    if inpt == word:
        return "correct"
    else:
        return "it was " + word
    

class Box():
    def __init__(self, x, y, w, h):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color_i
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.textsurf = font.render(self.text, False, color2)
        self.active = False
    
    def event(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.color = color_a
            self.active = True
        else:
            self.color = color_i
            self.active = False

    def change(self):
        self.textsurf = font.render(textbox.text, False, color2)

textbox = Box(dx/30, dy - 70, 750, 45)

index = random.randrange(0, size - 1)
qs_text = ""
times = 0
words_per_round = 2
score = ""
correct = 0

while True:
    
    display.fill(color1)

    if times > words_per_round - 1:
        print(str(correct) + "/" + str(words_per_round))
        stop()
        break

    qs_text = english[index]
    ans = french[index]
    qs = font2.render(qs_text, False, color2)

    pygame.draw.rect(display, textbox.color, textbox.rect)
    display.blit(textbox.textsurf, (textbox.rect.x + 15, textbox.rect.y + 5))
    display.blit(qs, (25,20))
    for event in pygame.event.get():
        if event.type == QUIT:
            stop()
            break

        elif event.type == KEYDOWN:
            if textbox.active == True:
                if event.key == pygame.K_BACKSPACE:
                    textbox.text = textbox.text[:-1]
                    textbox.change()

                elif event.key == pygame.K_UP and textbox.text[len(textbox.text) - 1] in scroll_list:
                    a = textbox.text[len(textbox.text) - 1]
                    textbox.text = textbox.text[:-1]
                    textbox.text += scroll(a)
                    textbox.change()

                elif event.key == pygame.K_RETURN:
                    print(process(textbox.text, ans))
                    if process(textbox.text, ans) == "correct":
                        correct += 1
                    
                    textbox.text = ""
                    french.remove(french[index])
                    size = len(french)
                    english.remove(english[index])
                    index = random.randrange(0, size - 1)
                    times += 1
                    textbox.change()
                
                elif len(textbox.text) < 40:
                    textbox.text += event.unicode
                    textbox.change()
        elif event.type == MOUSEBUTTONDOWN:
            textbox.event()

    pygame.display.flip()
