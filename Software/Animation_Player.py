import pygame
import os
import time
import atexit
from .Servo import send_to_arduino

class AnimationPlayer:
    def __init__(self):
        self.animations = {}
        self.current_animation = 'idle'
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 100  # ms per frame
        self.running = False
        self.screen = None
        self.default_frame = None
        
        # Initialize pygame
        self._init_pygame()
        self.load_animations()
        atexit.register(self.stop)

    def _init_pygame(self):
        try:
            pygame.init()
            # Use software surface for maximum compatibility
            self.screen = pygame.display.set_mode((320, 240), pygame.SWSURFACE)
            pygame.display.set_caption('AssistAI Animations')
            pygame.mouse.set_visible(False)  # Hide mouse cursor
            self.clock = pygame.time.Clock()
            
            # Create default frame
            self.default_frame = pygame.Surface((320, 240))
            self.default_frame.fill((50, 50, 70))  # Dark blue background
            font = pygame.font.SysFont('Arial', 20)
            text = font.render('AssistAI', True, (255, 255, 255))
            self.default_frame.blit(text, (120, 110))
        except Exception as e:
            print(f"Pygame initialization error: {str(e)}")
            raise

    def load_animations(self):
        anim_dirs = ['idle', 'talking', 'listening', 'thinking']
        base_path = os.path.join(os.path.dirname(__file__), 'animations')
        
        for anim_name in anim_dirs:
            self.animations[anim_name] = []
            anim_path = os.path.join(base_path, anim_name)
            
            if os.path.exists(anim_path):
                try:
                    # Get all image files sorted numerically
                    frames = sorted(
                        [f for f in os.listdir(anim_path) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))],
                        key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
                    )

                    
                    for frame_file in frames:
                        frame_path = os.path.join(anim_path, frame_file)
                        try:
                            frame = pygame.image.load(frame_path)
                            # Convert based on image type
                            if frame.get_bytesize() == 1:
                                frame = frame.convert()
                            else:
                                frame = frame.convert_alpha()
                            frame = pygame.transform.scale(frame, (320, 240))
                            self.animations[anim_name].append(frame)
                        except Exception as e:
                            print(f"Error loading {frame_path}: {str(e)}")
                            self.animations[anim_name].append(self.default_frame)
                except Exception as e:
                    print(f"Error loading animation {anim_name}: {str(e)}")
                    self.animations[anim_name].append(self.default_frame)
            else:
                print(f"Animation directory not found: {anim_path}")
                self.animations[anim_name].append(self.default_frame)

    def play_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.current_frame = 0
            try:
                send_to_arduino(animation_name)
            except Exception as e:
                print(f"Error sending to Arduino: {str(e)}")
            return True
        print(f"Animation {animation_name} not found")
        return False

    def update(self):
        if not self.running or not self.animations.get(self.current_animation):
            return
            
        now = time.time() * 1000  # Current time in ms
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            
            anim_frames = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(anim_frames)
            self._update_display()

    def _update_display(self):
        try:
            self.screen.fill((0, 0, 0))  # Clear screen
            frame = self.animations[self.current_animation][self.current_frame]
            self.screen.blit(frame, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)  # Cap at 60 FPS
        except Exception as e:
            print(f"Display update error: {str(e)}")

    def start(self):
        self.running = True
        try:
            while self.running:
                self.update()
                # Handle pygame events to prevent freezing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()
                time.sleep(0.01)  # Small delay to reduce CPU usage
        except Exception as e:
            print(f"Animation loop error: {str(e)}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if pygame.get_init():
            pygame.quit()