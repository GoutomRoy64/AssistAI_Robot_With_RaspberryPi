import pygame
import os
import time
import threading
from itertools import cycle

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
IMAGE_PATH = "images"  # Folder where your animation frames are
BACKGROUND_COLOR = (24, 28, 46) # Dark blue background
FRAME_RATE = 10  # Frames per second for the animation

# --- Globals ---
screen = None
faces = {}  # Will store lists of images, e.g., {'idle': [img1, img2, ...]}
current_state = 'idle'
current_frame = None # This will hold the surface of the frame to be drawn
animation_thread = None
stop_event = threading.Event()

def _animation_logic_loop():
    """
    The background loop that selects the next frame for the current animation state.
    It does NOT draw to the screen.
    """
    global current_state, current_frame
    
    clock = pygame.time.Clock()
    face_iterators = {state: cycle(frames) for state, frames in faces.items()}
    
    active_iterator = face_iterators.get(current_state, cycle([pygame.Surface((1,1))]))
    last_state = current_state

    while not stop_event.is_set():
        # Check if the state has changed
        if current_state != last_state:
            active_iterator = face_iterators.get(current_state, cycle([pygame.Surface((1,1))]))
            last_state = current_state
            
        # Get the next frame and store it in the global variable
        try:
            current_frame = next(active_iterator)
        except StopIteration:
            continue # Skip if iterator is empty
        
        # Control the animation speed
        clock.tick(FRAME_RATE)

def update_display():
    """
    This function should be called from the main loop.
    It handles drawing the current frame and processing events.
    """
    if not screen or current_frame is None:
        return

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Calculate center position and draw the current face frame
    rect = current_frame.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(current_frame, rect)
    
    # Update the display
    pygame.display.flip()
    
    # Process pygame events to keep the window responsive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_event.set() # Signal thread to stop
            pygame.quit()
            exit()

def init_display():
    """Initializes pygame, loads all animation frames, and starts the logic thread."""
    global screen, faces, animation_thread, current_frame
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AssistAI Face")

    states = ['idle', 'listening', 'talking', 'thinking']
    for state in states:
        faces[state] = []
        i = 0
        while True:
            filepath = os.path.join(IMAGE_PATH, f"{state}_{i}.png")
            if not os.path.exists(filepath):
                break
            try:
                img = pygame.image.load(filepath).convert_alpha()
                faces[state].append(img)
                print(f"[Display] Loaded {filepath} for state '{state}'")
            except pygame.error as e:
                print(f"[Display ERROR] Could not load image {filepath}: {e}")
            i += 1
        
        if not faces[state]:
            print(f"[Display WARNING] No frames found for state '{state}'. Using placeholder.")
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((255, 0, 255))
            faces[state].append(placeholder)

    # Set the very first frame to avoid a blank screen on start
    current_frame = faces['idle'][0]

    # Start the animation logic thread
    stop_event.clear()
    animation_thread = threading.Thread(target=_animation_logic_loop, daemon=True)
    animation_thread.start()

def set_face_state(state='idle'):
    """Sets the current animation state for the face."""
    global current_state
    if state in faces:
        current_state = state
    else:
        print(f"[Display WARNING] Unknown state '{state}'. Defaulting to 'idle'.")
        current_state = 'idle'

def shutdown_display():
    """Signals the animation thread to stop."""
    print("[Display] Shutting down display thread...")
    stop_event.set()
    if animation_thread:
        animation_thread.join(timeout=1)
