from cv2 import CAP_DSHOW
import tensorflow as tf
import numpy as np
import cv2 as cv
import pygame as pg 
import os
from ftfy import fix_encoding

# ------ Initialization--------
# load_model
model = tf.keras.models.load_model('model.h5')

# result of prediction
result = ['Paper', "Rock", "Scissors"]
Message = ["Tie", "You Win!", "You Lose YY", "Let's Start!"]
# default id_camera is 0, Usb_camera =1 
cap = cv.VideoCapture(0)
# global variable
i = 0
# Path to save image frame
path = os.path.abspath(os.getcwd())
# Load the image that the computer plays with the player
Image_directory = os.path.join(path, "Image_Engine")
List_image = [Image_directory + "\\Paper.png", Image_directory +"\\Rock.png", Image_directory + "\\Scissor.png"]
# Saved image directory
if not os.path.exists("Saved_Image"):
    os.mkdir("Saved_Image")
Saved_Image = os.path.join(path, "Saved_Image")
# Load player image default
Load_Player_Image = 0
# Initialize pygame
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((1400, 800), pg.RESIZABLE)
caption = pg.display.set_caption("Kéo Búa Bao")
# Color
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
# Create font 
font_Score = pg.font.SysFont("Corel", 35)
font_Player = pg.font.SysFont("Corel", 35)
font_Computer = pg.font.SysFont("Corel", 35)
font_Winner = pg.font.SysFont("Corel", 35)
font_CountDown = pg.font.SysFont("Corel", 35)
font_End = pg.font.SysFont("Corel", 50)
# Set coordination for GUI
coor_Computer = (200, 100)
coor_Player = (950, 100)
coor_Score_Computer = (500, 100)
coor_Score_Player = (750, 100)
coor_Image_Computer = (100, 200)
coor_Image_Player = (750, 200)
coor_Winner = (540, 700)
coor_Start_Button = (550, 400)
coor_CountDow = (600, 200)
coor_exit = (400, 220)
coor_replay = (100, 220)

# Draw boxes around computer and player areas
def DrawBoxesAroundImage(C_color, P_color):
    plVertices = [(750, 200), (1150, 200), (1150, 650), (750, 650), (750, 200)]
    coVertices = [(100, 200), (500, 200), (500, 650), (100, 650), (100, 200)]
    pg.draw.polygon(screen, P_color, plVertices, 10)
    pg.draw.polygon(screen, C_color, coVertices, 10)

# Start Button
Start_Button = pg.image.load("start.jpg")
Start_Button = pg.transform.scale(Start_Button, (150, 50))
# Check the camera can open or not
def OpenCamera(cap):
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
# end game
Exit_Image = pg.image.load("exit.png")
Exit_Image = pg.transform.scale(Exit_Image, (150, 100))
Replay_Image = pg.image.load("replay.png")
Replay_Image = pg.transform.scale(Replay_Image, (150, 100))



# Logic of game
def ShowGameResult(engine, player):
    '''
        0: "papers",
        1: "rock",
        2: "scissor"
    '''
    result = {
        0: "Hoa",
        1: "Thang",
        2: "Thua"
    }
    if engine == player:
        return 0
    if engine == 0:
        if player == 2:
            return 1
        else:
            return 2
    if engine == 1:
        if player == 0:
            return 1
        else:
            return 2
    if engine == 2:
        if player == 1:
            return 1
        else:
            return 2
    
# Predict image
def PredictionImage(path):
    img = tf.keras.preprocessing.image.load_img(path = path, target_size = (300, 200))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    print(classes)
    max_index_row = np.argmax(np.array(classes), axis=1)
    return int(max_index_row)
   
          
running = True
guessEngine = 0
guessPlayer = 0
winner = 3
# Score
Computer_Score = 0
Player_Score = 0
Computer_color = blue
Player_color = blue
check_count = False
counter, text = 10, '10'.rjust(3)
pg.time.set_timer(pg.USEREVENT, 1000)
check_count = False
reset = False
temp_score = 1
while running:
    screen.fill(white)
    OpenCamera(cap)
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # cv.imshow('frame', frame)
    Plr_guess_image = pg.image.frombuffer(frame,frame.shape[1::-1],"BGR")
    Player_guess_image = pg.transform.scale(Plr_guess_image, (450, 400))
    Player_guess_image = pg.transform.rotate(Player_guess_image, 90)
    
    save_image = False
    mouse = pg.mouse.get_pos() 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if 550<= mouse[0] <= 700 and 400<= mouse[1] <= 450:
                check_count = True
        if check_count and event.type == pg.USEREVENT:
            counter -= 1
            text = str(counter).rjust(3) if counter > 0 else 'Time up!'
                
        if event.type == pg.MOUSEMOTION:
            if 550 <= mouse[0] <= 700 and 400<= mouse[1] <= 450: 
                StartVertices = [(550, 400), (700, 400), (700, 450), (550, 450), (550, 400)]
                pg.draw.polygon(screen, green, StartVertices, 5) 
                
            if 100 <= mouse[0] <= 250 and 220<= mouse[1] <= 320: 
                ReplayVertices = [(100, 220), (250, 220), (250, 320), (100, 320), (100, 220)]
                pg.draw.polygon(screen, green, ReplayVertices, 5)
            if 400 <= mouse[0] <= 550 and 220<= mouse[1] <= 320: 
                ExitVertices = [(400, 220), (550, 220), (550, 320), (400, 320), (400, 220)]
                pg.draw.polygon(screen, green, ExitVertices, 5)
                    
    if ( text == 'Time up!'):
        counter, text = 10, '10'.rjust(3)
        save_image = True
    
    if save_image:
        i += 1
        name = str(i) + '.png'
        pg.image.save(Player_guess_image, Saved_Image +"\\" + name ) 
        guessEngine = np.random.randint(0, 3)
        guessPlayer = PredictionImage(Saved_Image +"\\"+ name)
        winner = ShowGameResult(guessEngine, guessPlayer)
        Load_Player_Image = pg.image.load((Saved_Image +"\\"+ name))
        Load_Player_Image = pg.transform.scale(Load_Player_Image, (450, 400))
        Load_Player_Image = pg.transform.rotate(Load_Player_Image, 270)
        
     
    #Set GUI
    Com = font_Computer.render("COMPUTER : ", True, red)
    screen.blit(Com, coor_Computer)
    Pla = font_Computer.render(": PLAYER ", True, red)
    screen.blit(Pla, coor_Player)
    Com_Score = font_Computer.render(str(Computer_Score) , True, blue)
    screen.blit(Com_Score, coor_Score_Computer)
    Play_Score = font_Computer.render(str(Player_Score) , True, blue)
    screen.blit(Play_Score, coor_Score_Player)
    screen.blit(Start_Button, coor_Start_Button)
    
    Computer_guess_image = pg.image.load(List_image[guessEngine])
    Computer_guess_image = pg.transform.scale(Computer_guess_image, (450, 400))
    Computer_guess_image = pg.transform.rotate(Computer_guess_image, 90)
    screen.blit(Computer_guess_image, coor_Image_Computer)
    
    screen.blit(font_CountDown.render(text, True, green), coor_CountDow)
    
    if winner == 1:
        Computer_color = red
        Player_color = green
        if save_image:
            Player_Score += 1
            check_count = False
            
    elif winner == 2:
        Computer_color = green
        Player_color = red
        if save_image:
            Computer_Score +=1
            check_count = False
    elif winner == 0:
        Computer_color = blue
        Player_color = blue 
        if save_image:
            check_count = False 
    if check_count == False and i != 0:
        screen.blit(Load_Player_Image, coor_Image_Player)
    else:
        screen.blit(Player_guess_image, coor_Image_Player)
           
    DrawBoxesAroundImage(Computer_color, Player_color)
    Winner = font_Computer.render(Message[winner] , True, red)
    screen.blit(Winner, coor_Winner)
    if ( Player_Score < Computer_Score and Computer_Score == 5):
        screen = pg.display.set_mode((700, 400), pg.RESIZABLE)
        caption = pg.display.set_caption("Kéo Búa Bao")
        screen.fill(white)
        screen.blit(font_End.render(Message[2], True, red), (180, 50))
        screen.blit(Exit_Image, coor_exit)
        screen.blit(Replay_Image, coor_replay)
        
    if (Computer_Score < Player_Score and Player_Score == 5):
        screen = pg.display.set_mode((700, 400), pg.RESIZABLE)
        caption = pg.display.set_caption("Kéo Búa Bao")
        screen.fill(white)
        screen.blit(font_End.render(Message[1], True, red), (180, 50))
        screen.blit(Exit_Image, coor_exit)
        screen.blit(Replay_Image, coor_replay)
        
    clock.tick(60)
    pg.display.flip()
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
pg.quit()

