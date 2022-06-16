import pygame
import random
import mutagen 
import os
import sys
import serial
import time
import eyed3
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData
from interfaz4 import *
from pygame.locals import *
from pygame import mixer
import RPi.GPIO as GPIO
import serial
from PyQt5 import QtGui, QtCore
#libreriar para la oled
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from board import SCL, SDA
import busio
import adafruit_ssd1306

pygame.mixer.init()
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

negro = 0,0,0
blanco = 255,255,255
width=800
height=600
#OLED
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

global cancion_actual
    
global i

Canciones = []
Canciones.insert(0,"(1)   arctic-monkeys-do-i-wanna-know-official-video.mp3")
Canciones.insert(0,"(2)   bruno-mars-locked-out-of-heaven-official-music-video.mp3")
Canciones.insert(0,"(3)   coldplay-adventure-of-a-lifetime-official-video.mp3")
Canciones.insert(0,"(4)   blackway-black-caviar-whats-up-danger-spider-man-into-the-spider-verse-official-audio.mp3")
Canciones.insert(0,"(5)   yesterday-remastered-2009.mp3")
Canciones.insert(0,"(6)   the-weeknd-the-hills-official-video.mp3")
Canciones.insert(0,"(7)   the-weeknd-blinding-lights-official-audio.mp3")
Canciones.insert(0,"(8)   the-rare-occasions-notion.mp3")
Canciones.insert(0,"(9)   the-chain-2004-remaster.mp3")
Canciones.insert(0,"(10)  the-beatles-help.mp3")
Canciones.insert(0,"(11)  the-beatles-eleanor-rigby-from-yellow-submarine.mp3")
Canciones.insert(0,"(12)  the-all-american-rejects-gives-you-hell-official-music-video.mp3")
Canciones.insert(0,"(13)  tame-impala-the-less-i-know-the-better-official-audio.mp3")
Canciones.insert(0,"(14)  stressed-out-by-twenty-one-pilots-lyrics.mp3")
Canciones.insert(0,"(15)  starboy.mp3")
Canciones.insert(0,"(16)  simple-plan-jet-lag-ft-natasha-bedingfield-official-video.mp3")
Canciones.insert(0,"(17)  siames-the-wolf-official-animated-music-video.mp3")
Canciones.insert(0,"(18)  sheppard-geronimo-international-version-official-music-video.mp3")
Canciones.insert(0,"(19)  she-loves-you-remastered-2009.mp3")
Canciones.insert(0,"(20)  shawn-mendes-stitches-lyrics.mp3")
Canciones.insert(0,"(21)  sebastian-yatra-tacones-rojos-official-video.mp3")
Canciones.insert(0,"(22)  sebastian-yatra-myke-towers-pareja-del-ano.mp3")
Canciones.insert(0,"(23)  sam-smith-how-do-you-sleep-official-video.mp3")
Canciones.insert(0,"(24)  sam-smith-diamonds.mp3")
Canciones.insert(0,"(25)  rixton-me-and-my-broken-heart-official-video.mp3")
Canciones.insert(0,"(26)  queen-killer-queen-top-of-the-pops-1974.mp3")
Canciones.insert(0,"(27)  queen-dont-stop-me-now-official-video.mp3")
Canciones.insert(0,"(28)  queen-crazy-little-thing-called-love-official-video.mp3")
Canciones.insert(0,"(29)  queen-bohemian-rhapsody-official-video-remastered.mp3")
Canciones.insert(0,"(30)  queen-another-one-bites-the-dust-official-video.mp3")
Canciones.insert(0,"(31)  post-malone-swae-lee-sunflower-spider-man-into-the-spider-verse.mp3")
Canciones.insert(0,"(32)  portugal-the-man-feel-it-still-official-music-video.mp3")
Canciones.insert(0,"(33)  panic-at-the-disco-high-hopes-official-video.mp3")
Canciones.insert(0,"(34)  panda-los-malaventurados-no-lloran-letra.mp3")
Canciones.insert(0,"(35)  onerepublic-secrets-official-music-video.mp3")
Canciones.insert(0,"(36)  nice-guys-finish-last.mp3")
Canciones.insert(0,"(37)  mrkitty-after-dark.mp3")
Canciones.insert(0,"(38)  mr-blue-sky.mp3")
Canciones.insert(0,"(39)  moves-like-jagger-maroon-5-ft-cristina-aguilera-sub-espanol.mp3")
Canciones.insert(0,"(40)  miley-cyrus-prisoner-official-video-ft-dua-lipa.mp3")
Canciones.insert(0,"(41)  michael-jackson-chicago-audio.mp3")
Canciones.insert(0,"(42)  michael-jackson-billie-jean-official-video.mp3")
Canciones.insert(0,"(43)  michael-jackson-bad-shortened-version.mp3")
Canciones.insert(0,"(44)  maroon-5-this-summers-gonna-hurt-like-a-motherfr-clean-official-music-video.mp3")
Canciones.insert(0,"(45)  maroon-5-this-love-official-music-video.mp3")
Canciones.insert(0,"(46)  maroon-5-one-more-night-official-music-video.mp3")
Canciones.insert(0,"(47)  maroon-5-misery-official-music-video.mp3")
Canciones.insert(0,"(48)  maroon-5-love-somebody-official-music-video.mp3")
Canciones.insert(0,"(49)  maroon-5-give-a-little-more-official-music-video.mp3")
Canciones.insert(0,"(50)  maroon-5-feelings-traducida-al-espanol.mp3")
Canciones.insert(0,"(51)  maroon-5-dont-wanna-know-ft-kendrick-lamar-audio.mp3")
Canciones.insert(0,"(52)  maroon-5-doing-dirt-traduccion-al-espanol.mp3")
Canciones.insert(0,"(53)  maroon-5-animals-lyrics.mp3")
Canciones.insert(0,"(54)  magic-rude-official-video.mp3")
Canciones.insert(0,"(55)  luis-miguel-culpable-o-no-mienteme-como-siempre-video-con-letra.mp3")
Canciones.insert(0,"(56)  lp-lost-on-you-live.mp3")
Canciones.insert(0,"(57)  los-bunkers-bailando-solo-video-oficial.mp3")
Canciones.insert(0,"(58)  lil-nas-x-jack-harlow-industry-baby-official-video.mp3")
Canciones.insert(0,"(59)  knaan-wavin-flag-coca-cola-celebration-mix.mp3")
Canciones.insert(0,"(60)  knaan-bang-bang-ft-adam-levine.mp3")
Canciones.insert(0,"(61)  kanye-west-flashing-lights-ft-dwele.mp3")
Canciones.insert(0,"(62)  jvke-this-is-what-falling-in-love-feels-like-official-video.mp3")
Canciones.insert(0,"(63)  justin-timberlake-sexyback-official-video-ft-timbaland.mp3")
Canciones.insert(0,"(64)  john-newman-love-me-again.mp3")
Canciones.insert(0,"(65)  james-blunt-youre-beautiful-official-music-video-4k.mp3")
Canciones.insert(0,"(66)  in-your-pocket.mp3")
Canciones.insert(0,"(67)  imagine-dragons-x-jid-enemy-from-the-series-arcane-league-of-legends.mp3")
Canciones.insert(0,"(68)  imagine-dragons-bones-official-music-video.mp3")
Canciones.insert(0,"(69)  hotel-california-2013-remaster.mp3")
Canciones.insert(0,"(70)  harry-styles-watermelon-sugar-official-video.mp3")
Canciones.insert(0,"(71)  harry-styles-golden-official-video.mp3")
Canciones.insert(0,"(72)  harry-styles-adore-you-official-video.mp3")
Canciones.insert(0,"(73)  green-day-meet-me-on-the-roof-official-music-video-starring-gaten-matarazzo.mp3")
Canciones.insert(0,"(74)  green-day-graffitia-official-audio.mp3")
Canciones.insert(0,"(75)  green-day-fire-ready-aim-official-audio.mp3")
Canciones.insert(0,"(76)  green-day-father-of-all-official-music-video.mp3")
Canciones.insert(0,"(77)  green-day-american-idiot-official-music-video.mp3")
Canciones.insert(0,"(78)  gorillaz-feel-good-inc-official-video.mp3")
Canciones.insert(0,"(79)  gilbert-osullivan-alone-again-naturally.mp3")
Canciones.insert(0,"(80)  george-michael-careless-whisper-official-video.mp3")
Canciones.insert(0,"(81)  fall-out-boy-centuries-official-music-video.mp3")
Canciones.insert(0,"(82)  eminem-without-me-official-music-video.mp3")
Canciones.insert(0,"(83)  elton-john-rocket-man-official-music-video.mp3")
Canciones.insert(0,"(84)  elton-john-im-still-standing.mp3")
Canciones.insert(0,"(85)  ed-sheeran-justin-bieber-i-dont-care-official-music-video.mp3")
Canciones.insert(0,"(86)  ed-sheeran-bad-habits-official-video.mp3")
Canciones.insert(0,"(87)  dnce-cake-by-the-ocean.mp3")
Canciones.insert(0,"(88)  declan-mckenna-british-bombs-official-video.mp3")
Canciones.insert(0,"(89)  confetti-ghost-official-audio.mp3")
Canciones.insert(0,"(90)  coldplay-viva-la-vida-official-video.mp3")
Canciones.insert(0,"(91)  childish-gambino-me-and-your-mama-official-audio.mp3")
Canciones.insert(0,"(92)  charlie-puth-attention-official-video.mp3")
Canciones.insert(0,"(93)  capital-cities-safe-and-sound-official-music-video.mp3")
Canciones.insert(0,"(94)  cant-stop-the-feeling-from-dreamworks-animations-trolls-official-video.mp3")
Canciones.insert(0,"(95)  calvin-harris-the-weeknd-over-now-official-video.mp3")
Canciones.insert(0,"(96)  calvin-harris-feels-official-video-ft-pharrell-williams-katy-perry-big-sean.mp3")
Canciones.insert(0,"(97)  bruno-mars-runaway-baby-official-audio-video-hd.mp3")
Canciones.insert(0,"(98)  beat-it.mp3")
Canciones.insert(0,"(99)  adele-oh-my-god-official-video.mp3")
Canciones.insert(0,"(100) a-flock-of-seagulls-i-ran-so-far-away-video.mp3")
Canciones_2 = []
for a in range(99):
    Canciones_2.append(str(a))
    
def update_state():
    global state , current_time , m , s ,pos_time
    pos_time = pygame.mixer.music.get_pos()

    s = pos_time // 1000
    m, s = divmod(s, 60)
    m, s = int(m), int(s)
    

class Ui_MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    
            
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.serAct)
        self.timer.start(500)
        
        global cancion_actual
        
        for a in Canciones:
            numero = 0
            self.listWidget.insertItem(numero,a)
            numero +=1    
        
        self.listWidget.setCurrentRow(0)
        self.lineEdit.setReadOnly(True)    
        self.pushButton.clicked.connect(self.Siguiente)
        self.pushButton_2.clicked.connect(self.Atras)
        self.pushButton_3.clicked.connect(self.play_Stop)
        self.pushButton_4.clicked.connect(self.Aleatorio)
        self.i=0
        self.pushButton_5.clicked.connect(self.Reiniciar)
        self.listWidget.itemClicked.connect(self.It)
        self.sl = self.horizontalSlider
          
    def Siguiente(self):
        global cancion_actual
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        cancion_actual = self.listWidget.currentItem().text()[6:]
        cancion_reproducir = (cancion_actual)
        pygame.mixer.music.load(cancion_reproducir)
        pygame.mixer.music.play()
        update_state()
        self.label_7.setText(f"{m:02}:{s:02}")
        cancion_reproducir_2 = cancion_actual
        audio = mutagen.File(cancion_reproducir_2)
        total_length = audio.info.length
        tm, ts = divmod(total_length+10, 60)
        tm, ts = int(tm), int(ts)
        self.label_8.setText(f"{tm:02}:{ts:02}")
        self.sl.setMinimum(0)
        self.sl.setMaximum(total_length)
        self.sl.setValue(pos_time/1000)
        print(total_length)
        print(pos_time/1000)
        parametros = eyed3.load(cancion_actual)
        self.lineEdit.setText(parametros.tag.artist)
        self.lineEdit_2.setText(parametros.tag.title)
        self.lineEdit_3.setText(parametros.tag.album)
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        padding = 15
        shape_width = 10
        top = 0
        bottom = height-padding
        x = padding
        font = ImageFont.load_default()
        draw.text((x, top),parametros.tag.artist,  font=font, fill=255)
        draw.text((x, top+10),parametros.tag.title, font=font, fill=255)
        draw.text((x, top+20),parametros.tag.album, font=font, fill=255)
        disp.image(image)
        disp.show()
        
    def Atras(self):
        global cancion_actual
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        cancion_actual = self.listWidget.currentItem().text()[6:]
        cancion_reproducir = (cancion_actual)
        pygame.mixer.music.load(cancion_reproducir)
        pygame.mixer.music.play()
        update_state()
        self.label_7.setText(f"{m:02}:{s:02}")
        cancion_reproducir_2 = cancion_actual
        audio = mutagen.File(cancion_reproducir_2)
        total_length = audio.info.length
        tm, ts = divmod(total_length+10, 60)
        tm, ts = int(tm), int(ts)
        self.label_8.setText(f"{tm:02}:{ts:02}")
        self.sl.setMinimum(0)
        self.sl.setMaximum(total_length)
        self.sl.setValue(pos_time/1000)
        print(total_length)
        print(pos_time/1000)
        parametros = eyed3.load(cancion_actual)
        self.lineEdit.setText(parametros.tag.artist)
        self.lineEdit_2.setText(parametros.tag.title)
        self.lineEdit_3.setText(parametros.tag.album)
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        padding = 15
        shape_width = 10
        top = 0
        bottom = height-padding
        x = padding
        font = ImageFont.load_default()
        draw.text((x, top),parametros.tag.artist,  font=font, fill=255)
        draw.text((x, top+10),parametros.tag.title, font=font, fill=255)
        draw.text((x, top+20),parametros.tag.album, font=font, fill=255)
        disp.image(image)
        disp.show()
    
    def play_Stop(self):
        self.status = pygame.mixer.music.get_busy() 
        if self.status:
            pygame.mixer.music.pause()
        if not self.status:
            pygame.mixer.music.unpause()
        self.status = not self.status   
        
    def Aleatorio(self):
        global cancion_actual
        var = random.randrange(0,12)
        self.listWidget.setCurrentRow(var)
        cancion_actual = self.listWidget.currentItem().text()[6:]
        cancion_reproducir = (cancion_actual)
        pygame.mixer.music.load(cancion_reproducir)
        pygame.mixer.music.play()
        update_state()
        self.label_7.setText(f"{m:02}:{s:02}")
        cancion_reproducir_2 = cancion_actual
        audio = mutagen.File(cancion_reproducir_2)
        total_length = audio.info.length
        tm, ts = divmod(total_length+10, 60)
        tm, ts = int(tm), int(ts)
        self.label_8.setText(f"{tm:02}:{ts:02}")
        self.sl.setMinimum(0)
        self.sl.setMaximum(total_length)
        self.sl.setValue(pos_time/1000)
        print(total_length)
        print(pos_time/1000)
        parametros = eyed3.load(cancion_actual)
        self.lineEdit.setText(parametros.tag.artist)
        self.lineEdit_2.setText(parametros.tag.title)
        self.lineEdit_3.setText(parametros.tag.album)                          
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        padding = 15
        shape_width = 10
        top = 0
        bottom = height-padding
        x = padding
        font = ImageFont.load_default()
        draw.text((x, top),parametros.tag.artist,  font=font, fill=255)
        draw.text((x, top+10),parametros.tag.title, font=font, fill=255)
        draw.text((x, top+20),parametros.tag.album, font=font, fill=255)
        disp.image(image)
        disp.show()
        
    def Reiniciar(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play()
        
    def It(self):
        cancion_actual = self.listWidget.currentItem().text()[6:]
        cancion_reproducir = (cancion_actual)
        pygame.mixer.music.load(cancion_reproducir)
        pygame.mixer.music.play()
        update_state()
        self.label_7.setText(f"{m:02}:{s:02}")
        cancion_reproducir_2 = cancion_actual
        audio = mutagen.File(cancion_reproducir_2)
        total_length = audio.info.length
        tm, ts = divmod(total_length+10, 60)
        tm, ts = int(tm), int(ts)
        self.label_8.setText(f"{tm:02}:{ts:02}")
        self.sl.setMinimum(0)
        self.sl.setMaximum(total_length)
        self.sl.setValue(pos_time/1000)
        print(total_length)
        print(pos_time/1000)
        parametros = eyed3.load(cancion_actual)
        if parametros.tag.artist == None:
            self.lineEdit.setText("NONE")
        if parametros.tag.title == None:
            self.lineEdit.setText("NONE")
        if parametros.tag.album == None:
            self.lineEdit.setText("NONE")
        else:
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        padding = 14
        shape_width = 10
        top = 0
        bottom = height-padding
        x = padding
        font = ImageFont.load_default()
        draw.text((x, top),parametros.tag.artist,  font=font, fill=255)
        draw.text((x, top+10),parametros.tag.title, font=font, fill=255)
        draw.text((x, top+20),parametros.tag.album, font=font, fill=255)
        disp.image(image)
        disp.show()
    
    def serAct(self):
        z=0
        op=''
        decena=''
        centena=''
        ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate= 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,timeout=1)
        counter=0
        y=0
        contador=0
        print('Entre')
        while z!=1:
            String=ser.readline().decode('utf-8').rstrip()
            if String!='':
                op=String
                print(String)
                z=1
        if op== 'A':
            self.Atras()
        if op== 'B':
            self.play_Stop()
        if op== 'C':
            self.Siguiente()
        if op== 'D':
            self.Reiniciar()
        if op== '#':
            self.Aleatorio()
        if op=='*':
            while y!=1:
                String2=ser.readline().decode('utf-8').rstrip()
                if String2!='':
                    centena=String2
                    print(centena)
                    y=1
                    while contador!=1:
                        String3=ser.readline().decode('utf-8').rstrip()
                        if String3!='':
                            decena=String3
                            print(String3)
                            contador=1
                            String4=centena+decena
                            print(String4)
                            valor = int(String4)
                            valor = valor-1
                            self.listWidget.setCurrentRow(int(valor))
                            cancion_actual = self.listWidget.currentItem().text()[6:]
                            cancion_reproducir = (cancion_actual)
                            pygame.mixer.music.load(cancion_reproducir)
                            pygame.mixer.music.play()
                            update_state()
                            self.label_7.setText(f"{m:02}:{s:02}")
                            cancion_reproducir_2 = cancion_actual
                            audio = mutagen.File(cancion_reproducir_2)
                            total_length = audio.info.length
                            tm, ts = divmod(total_length+10, 60)
                            tm, ts = int(tm), int(ts)
                            self.label_8.setText(f"{tm:02}:{ts:02}")
                            self.sl.setMinimum(0)
                            self.sl.setMaximum(total_length)
                            self.sl.setValue(pos_time/1000)
                            print(total_length)
                            print(pos_time/1000)
                            parametros = eyed3.load(cancion_actual)
                            self.lineEdit.setText(parametros.tag.artist)
                            self.lineEdit_2.setText(parametros.tag.title)
                            self.lineEdit_3.setText(parametros.tag.album)                          
                            width = disp.width
                            height = disp.height
                            image = Image.new('1', (width, height))
                            draw = ImageDraw.Draw(image)
                            padding = 15
                            shape_width = 10
                            top = 0
                            bottom = height-padding
                            x = padding
                            font = ImageFont.load_default()
                            draw.text((x, top),parametros.tag.artist,  font=font, fill=255)
                            draw.text((x, top+10),parametros.tag.title, font=font, fill=255)
                            draw.text((x, top+20),parametros.tag.album, font=font, fill=255)
                            disp.image(image)
                            disp.show()     
            
        if op== '9':
            i= 9
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)       
            

        if op== '8':
            i= 8
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '7':
            i= 7
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '6':
            self.i= 6
            self.listWidget.setCurrentRow(int(i)-1)
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '5':
            i= 5
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '4':
            i= 4
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '3':
            i= 3
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '2':
            i= 2
            self.listWidget.setCurrentRow(int(i)-1)
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
        if op== '1':
            i= 1
            self.listWidget.setCurrentRow(int(i))
            cancion_actual = self.listWidget.currentItem().text()[6:]
            cancion_reproducir = (cancion_actual)
            pygame.mixer.music.load(cancion_reproducir)
            pygame.mixer.music.play()
            parametros = eyed3.load(cancion_actual)
            self.lineEdit.setText(parametros.tag.artist)
            self.lineEdit_2.setText(parametros.tag.title)
            self.lineEdit_3.setText(parametros.tag.album)
            
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()