import cv2
import numpy as np
import screeninfo


def display_image_with_keyboard_control(screen_id):
    # Get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height

    # Initial position and radius of the circle
    x_offset, y_offset = 812, 512  # Start at the center of the screen
    radius = 50  # Initial radius of the circle

    window_name = "projector"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Create a blank canvas
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 180

        # Draw the circle at the current position
        cv2.circle(canvas, (x_offset, y_offset), radius, (255, 255, 255), -1)
        print("x_offset, y_offset: ", x_offset, y_offset)

        # Show the canvas
        cv2.imshow(window_name, canvas)

        # Wait for a key press
        key = cv2.waitKey(10)

        # Move circle or change radius based on key press
        if key == ord("w"):  # Up
            y_offset = max(0, y_offset - 10)
        elif key == ord("s"):  # Down
            y_offset = min(height, y_offset + 10)
        elif key == ord("a"):  # Left
            x_offset = max(0, x_offset - 10)
        elif key == ord("d"):  # Right
            x_offset = min(width, x_offset + 10)
        elif key == ord("i"):  # Up
            y_offset = max(0, y_offset - 1)
        elif key == ord("k"):  # Down
            y_offset = min(height, y_offset + 1)
        elif key == ord("j"):  # Left
            x_offset = max(0, x_offset - 1)
        elif key == ord("l"):  # Right
            x_offset = min(width, x_offset + 1)
        elif key == ord("="):  # Increase radius
            radius += 5
        elif key == ord("-"):  # Decrease radius
            radius = max(5, radius - 2)
        elif key == 27:  # Escape key
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    screen_id = 0
    display_image_with_keyboard_control(screen_id)
