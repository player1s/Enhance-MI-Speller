import pygame
import time
import sys

# Initialize Pygame
pygame.init()

# Define window dimensions
screen = pygame.display.Info()
width, height = screen.current_w, screen.current_h-50

# Set up the window display
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("EEG Test Program")

# Define cross dimensions
SHAPE_WIDTH = 50
SHAPE_HEIGHT = 50

# Define three different color sets for the cross
COLOR_SET_1 = [(255, 0, 0), (0, 255, 0), (255, 0, 0)]

# Define the time intervals for color changes
COLOR_SET_1_DURATION = 3
COLOR_SET_2_DURATION = 4

# Initialize the current color set index and color index
current_color_set_index = 0
current_color_index = 0

# Define font for timer
font = pygame.font.SysFont(None, 48)

# Define start time
start_time = time.time()

# define times for the 10sec activity
changeTimes = [0, 6]

def drawLegend(legend_x, legend_y, color, message):
    pygame.draw.rect(window, color, pygame.Rect(legend_x, legend_y, SHAPE_WIDTH, SHAPE_HEIGHT))

    legend_text = font.render(message, True, (255, 255, 255))
    window.blit(legend_text, (legend_x + 60, legend_y))

drawLegend(10, 60, (255, 0, 0), " 0 - 6 = prep")
drawLegend(10, 120, (0, 255, 0), " 6 - 10 = imagine")

# Draw the cross in the center of the window
def draw_cross(color):
    cross_x = width // 2 - SHAPE_WIDTH // 2
    cross_y = height // 2 - SHAPE_HEIGHT // 2
    pygame.draw.rect(window, color, pygame.Rect(cross_x, cross_y, SHAPE_WIDTH, SHAPE_HEIGHT))

# Update the window display
pygame.display.flip()

color = COLOR_SET_1[0]

# setting order to display the trials with
ORDER = [0, 1, 2, 1, 0, 2, 2, 0, 1]
nextUp = ""

setActivityListMI = ["Right", "Left", "Rest"]
setActivityListIGEP = ["Sour", "Salty", "Rest"]
setActivityListCombo = ["Right Sour", "Left Salty", "Rest"]
sets = [setActivityListMI, setActivityListIGEP, setActivityListCombo]
selection = 0
currentActivityIndex = 0
start_time = time.time()

def select(selection, start_time):
    while selection == 0:
        # create next up section
        guide_text = font.render("Press 1 for MI, 2 for flavors, 3 for combo", True, (255, 255, 255))

        # Display guide text on screen
        window.blit(guide_text, (width // 2 - 250, height // 2 - height // 4))
        
        # Update the window display
        pygame.display.flip()

        #reset guide text
        window.blit(pygame.Surface((800, 50)), (width // 2 - 250, height // 2 - height // 4))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    selection = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selection = 1
                    start_time = time.time()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    selection = 2
                    start_time = time.time()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    selection = 3
                    start_time = time.time()
    return start_time, selection


    

# Run the game loop
while True:
    color_set = COLOR_SET_1
    duration3sec = COLOR_SET_1_DURATION
    duration4sec = COLOR_SET_2_DURATION 

    
    # Calculate time elapsed since start of program
    elapsed_time = int(time.time() - start_time)  
    
    # there is a mess with currentactivity index, make sure the system jumps to the next labelset good
    currentActivityIndex = elapsed_time // 10

    if currentActivityIndex == 9:
        selection = 0
        currentActivityIndex = 0
    
    start_time, selection = select(selection, start_time)

    if selection == 1:
        currentSetIndex = 0

    elif selection == 2:
        currentSetIndex = 1

    elif selection == 3:
        currentSetIndex = 2

    nextUp = sets[currentSetIndex][ORDER[currentActivityIndex]]

    if (elapsed_time % 10) == 0:
        color = color_set[0]
    
    elif (elapsed_time % 10) == 6:
        color = color_set[1]
    
    # Draw the cross in the current color
    draw_cross(color)

    # Convert time to string and render text
    time_text = font.render(str(elapsed_time % 10), True, (255, 255, 255))

    # Display time on screen
    window.blit(time_text, (width // 2 - 5, height // 2 + height // 4))

    # create next up section
    guide_text = font.render("Imagine: " + nextUp, True, (255, 255, 255))

    # Display guide text on screen
    window.blit(guide_text, (width // 2 - 100, height // 2 - height // 4))

    # create trial section
    guide_text = font.render("Trial: " + str(currentActivityIndex+1) + " / " + str(len(ORDER)), True, (255, 255, 255))

    # Display trial text on screen
    window.blit(guide_text, (10, 10))

    # Update the window display
    pygame.display.flip()

    #reset timer
    window.blit(pygame.Surface((50, 50)), (width // 2 - 5, height // 2 + height // 4))
    #reset guide text
    window.blit(pygame.Surface((400, 50)), (width // 2 - 100, height // 2 - height // 4))
    #reset trial text
    window.blit(pygame.Surface((250, 50)), (10, 10))

    

    # Check for button press to terminate program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                selection = 0