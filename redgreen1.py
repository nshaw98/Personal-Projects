#!/usr/bin/env python
import pygame
import sys
import random

screen_width = 640
screen_height = 480
screen_size = screen_width, screen_height
press_events = pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN

screen = None

def write_text(screen, text, color, big):
	if big:
		height = int(screen.get_height() / 5)
		up = screen.get_height() / 2
	else:
		height = int(screen.get_height() / 12)
		up = screen.get_height() - ( screen.get_height() / 24 )
	font = pygame.font.Font( None, height)
	rend = font.render( text, 1, color)
	textpos = rend.get_rect(
		centerx = screen.get_width() / 2,
		centery = up
	)

	screen.blit( rend, textpos)

def timed_wait(time_to_wait, event_types_that_cancel):
	"""
	Wait for time_to_wait, but cancel if the relevant event happens.
	Return True if cancelled, or False if we waited the full time.
	"""

	event_types_that_cancel = pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN
	
	
	finished_waiting_event_id = pygame.USEREVENT + 1
	pygame.time.set_timer( finished_waiting_event_id, time_to_wait)
	# in two seconds, make up an event

	try:
		pygame.event.clear()
	
		pressed = False # so far, no key has been pressed..
		waiting = True
		while waiting:
			evt = pygame.event.wait()
			if is_quit( evt ):
				quit()
			elif evt.type in event_types_that_cancel:
				waiting = False
				pressed = True # because they pressed a key.
			elif evt.type == finished_waiting_event_id:
				waiting = False
	finally:
		pygame.time.set_timer( finished_waiting_event_id, 0)

	return pressed


def start():
	global screen
	pygame.init()
	screen = pygame.display.set_mode( screen_size, pygame.FULLSCREEN )
	

def quit():
	pygame.quit()
	sys.exit()

def ready_screen(go_number, correct):
	screen.fill(pygame.Color( "black" ) )
	white = pygame.Color("white")
	write_text(screen, "Ready?", white, True)
	
	go_number_str = "Turn: %d    Score: %d" % ((go_number + 1), correct) # brackets needed so that it's treated as list
	
	write_text( screen, go_number_str, pygame.Color("white"), False)

	pygame.display.flip()

def wait():
	time_to_wait = random.randint( 1500, 3000) # Between 1.5 and 3 seconds
	timed_wait( time_to_wait, () )

def is_quit( evt ):
    return (
        evt.type == pygame.QUIT or
         ( 
              evt.type == pygame.KEYDOWN and 
              evt.key == pygame.K_ESCAPE
         )
    )

def shape_wait():
	"""
	Wait while we display a shape. Returns True if a key was pressed or false otherwise
	"""
	return timed_wait(2000, press_events) # 2 secs

def tick():
	color = pygame.Color( "green" )
	w = screen.get_width() / 2
	h = screen.get_height() / 4
	points = (
		( w - w/5, h - h/9 ),
		( w      , h + h/5 ),
		( w + w/3, h - h/3 ),
	)

	screen.fill( pygame.Color( "black" ) )
	pygame.draw.lines( screen, color, False, points, 20 )
	

def cross():
	color = pygame.Color( "red")
	w = screen.get_width() / 2
	h = screen.get_height() / 4
	left = w - w/3
	right = w + w/3
	top = h - h/3
	bottom = h + h/3

	start1 = left, top
	end1 = right, bottom
	
	start2 = left, bottom
	end2 = right, top

	screen.fill( pygame.Color( "black" ) )
	pygame.draw.line( screen, color, start1, end1, 20 )
	pygame.draw.line( screen, color, start2, end2, 20 )
	


def green_success():
	tick()
	green = pygame.Color( "green")
	white = pygame.Color( "white")
	write_text( screen, "Well done!", green, True)
	write_text( screen, "You pressed on the green circle!", white, False )
	pygame.display.flip()
	timed_wait(2000, press_events) # 2 secs

def green_failure():
	cross()
	red = pygame.Color( "red")
	white = pygame.Color( "white")
	write_text( screen, "Bad luck!", red, True)
	write_text( screen, "Press on the green circle!", white, False )
	pygame.display.flip()
	timed_wait(2000, press_events)

def red_success():
	tick()
	green = pygame.Color( "green")
	white = pygame.Color( "white")
	write_text( screen, "Well done!", green, True)
	write_text( screen, "You didn't press on red!", white, False )
	pygame.display.flip()
	timed_wait(2000, press_events)

def red_failure():
	cross()
	red = pygame.Color( "red")
	white = pygame.Color( "white")
	write_text( screen, "Bad luck!", red, True)
	write_text( screen, "Red means don't press anything!", white, False )
	pygame.display.flip()
	timed_wait(2000, press_events)


def green_shape():
	green = pygame.Color( 'green')
	center = ( int(screen.get_width() /2), int(screen.get_height() / 2) )
	radius = int(screen.get_height() / 3)

	screen.fill( pygame.Color( 'white' ) )
	pygame.draw.circle( screen, green, center, radius, 0)

	write_text(screen, "Press any key!", pygame.Color( "black"), False)

	pygame.display.flip()

	pressed = shape_wait()
	
	if pressed:
		green_success()
		return 1
	else:
		green_failure()
		return 0
def red_shape():
	red = pygame.Color( 'red')
	height = 2 * ( screen.get_height() / 3 )
	left = ( screen.get_width() / 2 ) - ( height / 2)
	top = screen.get_height() / 6

	screen.fill( pygame.Color( "white" ) )
	
	pygame.draw.rect( screen, red, (left, top, height, height), 0) # two heights becuase its a square

	write_text(screen, "Don't press!", pygame.Color( "black"), False) # false means write small at the bottom of the screen

	pygame.display.flip()

	pressed = shape_wait()
	
	if pressed:
		red_failure()
		return 0
	else:
		red_success()
		return 1

def shape():
	GREEN = 0
	RED = 1
	shape = random.choice( [GREEN, RED] )# chooses one and puts answer into shape

	if shape == GREEN:
		return green_shape()
	else:
		return red_shape()

def end(correct):
	print("You got %d correct answers" % correct) # subs number of corrects ans in
	screen.fill(pygame.Color( "black" ))
	white = pygame.Color( "white")
	write_text( screen, "Thanks for playing!", white, True)
	msg = "Final Score: %d   Press a key to exit" % correct
	write_text( screen, msg, white, False)
	
	pygame.display.flip()

	pygame.event.clear()
	timed_wait(0, press_events) # 0 means wait forever

# We start from here

start()

correct = 0

for i in range(10):

	ready_screen(i,correct)

	wait()

	correct += shape() # gives back an answer for score

end(correct) # prints answer
    


