import pygame
import time
import threading

# Initialize Pygame mixer
pygame.mixer.init()

# Load the sound
arcadeSound = pygame.mixer.Sound("data/sounds/arcade.wav")
fanfareSound = pygame.mixer.Sound("data/sounds/fanfare.wav")

def wheel_nonblocking(sound1, sound2, total_time):
    fade_thread = threading.Thread(target=fade_sound_blocking, args=(sound1, sound2, total_time), daemon=True)
    fade_thread.start()

def fade_sound_blocking(sound1, sound2, total_time):
    """
    Play the sound for 'total_time' seconds and fade out over the last 3 seconds (or the whole time if less than 3 seconds).
    """
    # Determine the fade duration
    fade_duration = min(3, total_time)  # Fade out over the last 3 seconds (or the entire time if less than 3)

    # Play the sound
    sound1.play()

    # Start the fade-out process after (total_time - fade_duration) seconds
    # start_fade_time = time.time() + (total_time - fade_duration)
    # while time.time() < start_fade_time:
    #     # Play normally for the first (total_time - fade_duration) seconds
    #     pass
    time.sleep(total_time - fade_duration)

    # Fade out over the last 'fade_duration' seconds
    fade_steps = 100  # Number of steps for the fade-out
    initial_volume = sound1.get_volume()
    fade_increment = initial_volume / fade_steps

    for step in range(fade_steps):
        # Gradually decrease the volume
        current_volume = initial_volume - fade_increment * (step + 1)
        sound1.set_volume(max(0, current_volume))  # Ensure the volume doesn't go below 0
        time.sleep(fade_duration / fade_steps)  # Wait between steps
        
        if step == 90:
            sound2.play()

    # Stop the sound after fading out
    sound1.stop()

