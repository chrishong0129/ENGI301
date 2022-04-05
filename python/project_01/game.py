"""
--------------------------------------------------------------------------
People Counter
--------------------------------------------------------------------------
License:   
Copyright 2022 Chris Hong

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

He's a Keeper: ENGI301 Project 1

Use the following hardware components to make a programmable combination lock:  
  - HT16K33 Display
  - Arcade Button x 5
  - Red LED
  - Green LED
  - Buzzer
  - 3D printed button enclosure x 5
    - Suction cups x 5
  
  
Requirements:
  - 3 second countdown when game starts
  - Each game is consist of 20 rounds
    - Buzzer rings 
    - One of the 5 Buttons light up randomly
    - Display time until user hits Button
  - Display average time once the game is over
  - Each button fit into 3D printed enclosure
    - Enclosure must be equipped with suction cups to attach to mirrors/smooth surfaces

Uses:
  - time library in order to keep track of time taken to hit button
  - random library to randomize each round
  - ht16k33 display library developed in class
  - buzzer library developed in class
"""

import time
import random

import Adafruit_BBIO.GPIO as GPIO

import ht16k33 as HT16K33
import buzzer_music as BUZZER
# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# GPIO output state
LOW                          = "0"
HIGH                         = "1"

CLEAR_DIGIT                 = 0x7F
# ------------------------------------------------------------------------
# GPIO / ADC access library
# ------------------------------------------------------------------------
import os

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class Game():
    """ KeepingGame """
    button_0   = None
    button_1   = None
    button_2   = None
    button_3   = None
    button_4   = None
    button_5   = None
    led_1      = None
    led_2      = None
    led_3      = None
    led_4      = None
    led_5      = None
    buzzer     = None
    red_led    = None
    green_led  = None
    display1    = None
    
    # assign each button/buzzer/e
    def __init__(self, button_0="P2_2", 
                       button_1="P2_8", led_1="P2_10",
                       button_2="P2_5", led_2="P2_7",
                       button_3="P2_18", led_3="P2_20",
                       button_4="P2_22", led_4="P2_24",
                       button_5='P2_33', led_5='P2_35',
                       red_led="P2_6", green_led="P2_4",
                       buzzer="P2_1",i2c_bus=1, i2c_address=0x70):
        
        """ Initialize variables and set up display """
        self.button_0   = button_0      # gpio59
        
        self.button_1   = button_1      # gpio60
        self.led_1      = led_1         # gpio52
        self.button_2   = button_2      # gpio30
        self.led_2      = led_2         # gpio31
        self.button_3   = button_3      # gpio47
        self.led_3      = led_3         # gpio64
        self.button_4   = button_4      # gpio46
        self.led_4      = led_4         # gpio44
        self.button_5   = button_5      # gpio45
        self.led_5      = led_5         # gpio86
        self.buzzer     = BUZZER.BuzzerMusic(buzzer)      # PWM
        self.red_led    = red_led
        self.green_led  = green_led
        self.display1   = HT16K33.HT16K33(i2c_bus, i2c_address)
        
        self._setup()
        
        # LIST OF BUTTONS: ADD MORE ENTRIES AS I ADD MORE BUTTONS
        buttons_list = [self.button_1, self.button_2, self.button_3, self.button_4, self.button_5]
    
    # End def

    # SOME HELPER FUNCTIONS
    def _setup(self):
        """Setup the hardware components."""
        # setup pins in/out
        # need to add every pin to get rid of error
        GPIO.setup("P2_2", GPIO.IN)         # button 0
        GPIO.setup("P2_8", GPIO.IN)         # button 1 in
        GPIO.setup("P2_10", GPIO.OUT)       # led 1 out
        
        GPIO.setup("P2_5", GPIO.IN)         # button 2 in
        GPIO.setup("P2_7", GPIO.OUT)        # led 2 out
        
        GPIO.setup("P2_18", GPIO.IN)         # button 3 in
        GPIO.setup("P2_20", GPIO.OUT)        # led 3 out
        
        GPIO.setup("P2_22", GPIO.IN)         # button 4 in
        GPIO.setup("P2_24", GPIO.OUT)        # led 4 out
        
        GPIO.setup("P2_33", GPIO.IN)         # button 5 in
        GPIO.setup("P2_35", GPIO.OUT)        # led 5 out
        
        GPIO.setup("P2_4", GPIO.OUT)        # green led
        GPIO.setup("P2_6", GPIO.OUT)        # red led
        
        # In case buzzer is going for whatever reason
        self.buzzer.stop()
        # Initialize Display
        self.display1.clear()

    # End def

    def get_delay_time(self):
        """Randomly decide delay time between rounds"""
        # generate random number between 0.5 and 2.5
        delay_time = random.randrange(5, 25)
        delay_time = delay_time / 10
        return delay_time
    # End def
    
    def get_rand_button(self, buttons_list):
        """Randomly decide which button to light up"""
        # CHOOSE ONE BUTTON OUT OF LIST OF ALL BUTTONS
        rand_button = random.choice(buttons_list)
        return rand_button
    
    def sound_C5(self,sleep_time):
        """Turn on the buzzer for time seconds"""
        self.buzzer.play_note(523, sleep_time)
        self.buzzer.stop()
    # End def
    
    def sound_C6(self,sleep_time):
        """Turn on the buzzer for time seconds"""
        self.buzzer.play_note(1047, sleep_time)
        self.buzzer.stop()
    # End def


    def start_countdown_timer(self):
        """Start the countdown timer"""
        
        # Count 3
        # print("3")
        GPIO.output(self.red_led, GPIO.HIGH)
        self.display1.text("   3")
        self.sound_C5(0.3)
        GPIO.output(self.red_led, GPIO.LOW)
        time.sleep(0.7)
        
        # Count 2
        # print("2")
        GPIO.output(self.red_led, GPIO.HIGH)
        self.display1.text("   2")
        self.sound_C5(0.3)
        GPIO.output(self.red_led, GPIO.LOW)
        time.sleep(0.7)
    
        # Count 1
        # print("1")
        GPIO.output(self.red_led, GPIO.HIGH)
        self.display1.text("   1")
        self.sound_C5(0.3)
        GPIO.output(self.red_led, GPIO.LOW)
        time.sleep(0.7)
        
        # Count 0
        GPIO.output(self.green_led, GPIO.HIGH)
        self.display1.text("   0")
        self.sound_C6(0.3)
        GPIO.output(self.green_led, GPIO.LOW)
        time.sleep(0.7)
        
    # End def    
    
    def get_time_taken(self,rand_button):
        """Button press, copied from combo_lock.py"""
        """Records time between button lighting up and button being pressed"""
        start = time.time()
        
        # Nothing will happen until correct button is pressed
        while(GPIO.input(rand_button) == 1):
            time.sleep(0.02)
            
        time_taken = (time.time() - start)
        time_taken = int(time_taken * 100)
        return time_taken
        
    # End def
    
    def display_time_taken(self, time_taken):
        """Use display1 to show time taken to hit button (w 2 decimals)"""
        # since time_taken has two decimals
        if (time_taken > 9999):
            raise ValueError("Took too long...")
        else:
            self.display1.update_with_decimal(time_taken)
        
    # End def
    
    def light_rand_led(self,rand_button):
        """Light up LED corresponding to random button"""
        if rand_button == self.button_1:
            GPIO.output(self.led_1, GPIO.HIGH)
        elif rand_button == self.button_2:
            GPIO.output(self.led_2, GPIO.HIGH)
        elif rand_button == self.button_3:
            GPIO.output(self.led_3, GPIO.HIGH)
        elif rand_button == self.button_4:
            GPIO.output(self.led_4, GPIO.HIGH)
        else:
            GPIO.output(self.led_5, GPIO.HIGH)
    # End def
    
    def reset_led_all(self):
        """turn off all button LEDs"""
        GPIO.output(self.led_1, GPIO.LOW)
        GPIO.output(self.led_2, GPIO.LOW)
        GPIO.output(self.led_3, GPIO.LOW)
        GPIO.output(self.led_4, GPIO.LOW)
        GPIO.output(self.led_5, GPIO.LOW)
    # End def
    
    
    # ANYTHING ELSE? SEE IF I NEED ANY MORE FUNCTIONS
    
    def one_round(self,buttons_list):
        '''define one round'''
        # wait for a random amount of time
        delay_time = self.get_delay_time()
        time.sleep(delay_time)
        
        # choose one of the buttons randomly
        rand_button = self.get_rand_button(buttons_list)
        
        # ring buzzer
        self.sound_C5(0.2)
        
        # light up corresponding led
        self.light_rand_led(rand_button)
        
        # get time it took
        time_taken = self.get_time_taken(rand_button)       # this will be a decimal 
        print(time_taken)
        self.reset_led_all()
        
        # display on hex display
        self.display1.update_with_decimal(time_taken)
        
        # return time it took
        return time_taken
        # return right/wrong
        
    # End def

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Game Start")
    number_of_rounds = 20
    # instantiate game
    game = Game()
    buttons_list = [game.button_1, game.button_2, game.button_3, game.button_4, game.button_5]
    # 3s countdown
    game.start_countdown_timer()
    # create empty list
    time_log = [None] * number_of_rounds
    
    for i in range(number_of_rounds):
        time_taken = game.one_round(buttons_list)
        # log time taken for each round
        time_log[i] = time_taken
        
    av_time = sum(time_log) / len(time_log) 
    
    # Display average time
    game.display1.update_with_decimal(int(av_time))
    
    print('')
    print('Average Time: ' + str(av_time / 100) + 's')
    print('Game Completed')