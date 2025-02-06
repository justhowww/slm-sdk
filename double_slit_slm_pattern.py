import cv2
import numpy as np
import screeninfo


def display_double_slit_with_keyboard_control(screen_id):
    # Get the size and position of the specified screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height

    # Initial position: center between the two slits
    x_offset, y_offset = 852, height // 2  # You may adjust these values as needed

    # Slit properties
    slit_width = 5  # Width of each slit in pixels
    slit_height = height  # Height of each slit in pixels
    separation = 20  # Separation between the two slits in pixels

    window_name = "projector"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Create a blank canvas with a gray background
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 0

        # Calculate half of the separation for positioning the slits
        half_separation = separation // 2

        # Define top-left and bottom-right coordinates for the first slit
        top_left1 = (
            x_offset - half_separation - slit_width // 2,
            y_offset - slit_height // 2,
        )
        bottom_right1 = (
            x_offset - half_separation + slit_width // 2,
            y_offset + slit_height // 2,
        )

        # Define top-left and bottom-right coordinates for the second slit
        top_left2 = (
            x_offset + half_separation - slit_width // 2,
            y_offset - slit_height // 2,
        )
        bottom_right2 = (
            x_offset + half_separation + slit_width // 2,
            y_offset + slit_height // 2,
        )

        # Draw the two slits as filled white rectangles
        cv2.rectangle(canvas, top_left1, bottom_right1, (180, 180, 180), -1)
        cv2.rectangle(canvas, top_left2, bottom_right2, (180, 180, 180), -1)

        # Optional: Print the current center position and separation for debugging
        print(
            f"Center position (x_offset, y_offset): ({x_offset}, {y_offset}), Separation: {separation}"
        )

        # Display the canvas in the window
        cv2.imshow(window_name, canvas)

        # Wait for a key press for 10 ms
        key = cv2.waitKey(10)

        # Handle keyboard inputs to move the slits or adjust their properties
        if key == ord("w"):  # Move up
            y_offset = max(slit_height // 2, y_offset - 10)
        elif key == ord("s"):  # Move down
            y_offset = min(height - slit_height // 2, y_offset + 10)
        elif key == ord("a"):  # Move left
            x_offset = max(half_separation + slit_width // 2, x_offset - 10)
        elif key == ord("d"):  # Move right
            x_offset = min(width - half_separation - slit_width // 2, x_offset + 10)
        elif key == ord("i"):  # Smaller move up
            y_offset = max(slit_height // 2, y_offset - 2)
        elif key == ord("k"):  # Smaller move down
            y_offset = min(height - slit_height // 2, y_offset + 2)
        elif key == ord("j"):  # Smaller move left
            x_offset = max(half_separation + slit_width // 2, x_offset - 2)
        elif key == ord("l"):  # Smaller move right
            x_offset = min(width - half_separation - slit_width // 2, x_offset + 2)
        elif key == ord("="):  # Increase slit width
            slit_width += 1
            # Ensure the slits remain visible within the screen
            if slit_width > separation:
                slit_width = separation
        elif key == ord("-"):  # Decrease slit width
            slit_width = max(1, slit_width - 1)
        elif key == ord("o"):  # Increase separation
            # Check if increasing separation keeps slits within screen bounds
            if (x_offset + (half_separation + 1) + slit_width // 2) <= width:
                separation += 1
            else:
                print("Maximum separation reached.")
        elif key == ord("p"):  # Decrease separation
            separation = max(2, separation - 1)  # Minimum separation of 2 pixels
        elif key == 27:  # Escape key to exit
            break

    # Clean up and close the window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    screen_id = 0  # Change this if you have multiple monitors
    display_double_slit_with_keyboard_control(screen_id)
