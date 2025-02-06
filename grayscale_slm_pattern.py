import cv2
import numpy as np
from screeninfo import get_monitors

# *  This script can be used for SLM calibration


def display_image_with_keyboard_control(screen_id=0):
    """
    Displays a full-screen window with a movable and resizable square controlled via keyboard inputs.

    Keyboard Controls:
        - 'W' / 'w': Move Up by 10 / 2 pixels
        - 'S' / 's': Move Down by 10 / 2 pixels
        - 'A' / 'a': Move Left by 10 / 2 pixels
        - 'D' / 'd': Move Right by 10 / 2 pixels
        - 'I' / 'i': Move Up by 2 pixels
        - 'K' / 'k': Move Down by 2 pixels
        - 'J' / 'j': Move Left by 2 pixels
        - 'L' / 'l': Move Right by 2 pixels
        - '=' / '+' : Increase square size by 10 pixels (side length)
        - '-' / '_' : Decrease square size by 10 pixels (side length)
        - 'T' / 't' : Increase grayscale value by 5 (up to 255)
        - 'G' / 'g' : Decrease grayscale value by 5 (down to 0)
        - 'Esc'     : Exit the application

    Args:
        screen_id (int): Index of the monitor to display the window on.
                         Defaults to 0 (primary monitor).
    """
    # Retrieve available monitors
    try:
        monitors = get_monitors()
        if not monitors:
            raise ValueError("No monitors detected.")
    except Exception as e:
        print(f"An error occurred while retrieving monitors: {e}")
        return

    # Validate screen_id
    if screen_id < 0 or screen_id >= len(monitors):
        print(
            f"Error: screen_id {screen_id} is out of range. Available monitors: {len(monitors)}"
        )
        return

    # Get the specified screen's properties
    screen = monitors[screen_id]
    width, height = screen.width, screen.height

    # Define the grayscale variable
    calibrate_reflective_slm_value = 0  # Initial grayscale value (0-255)

    # Initialize square properties at the center of the screen
    x_center, y_center = width // 2, height // 2
    half_side = 200  # Initial half side length of the square

    # Define window properties
    window_name = "Projector Control - Square"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, screen.x, screen.y)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Define movement and size increments
    large_step = 10  # Movement step for 'w', 'a', 's', 'd'
    small_step = 2  # Movement step for 'i', 'j', 'k', 'l'
    size_step = 10  # Size increment/decrement step
    min_half_side = 5  # Minimum half side length to prevent inversion

    # Define grayscale adjustment step and limits
    grayscale_step = 1
    max_grayscale = 255
    min_grayscale = 0

    while True:
        # Create a gray canvas
        canvas = np.full(
            (height, width, 3), calibrate_reflective_slm_value, dtype=np.uint8
        )

        # Calculate top-left and bottom-right points of the square
        top_left = (x_center - half_side, y_center - half_side)
        bottom_right = (x_center + half_side, y_center + half_side)

        # Ensure the square stays within the canvas boundaries
        top_left = (max(0, top_left[0]), max(0, top_left[1]))
        bottom_right = (
            min(width - 1, bottom_right[0]),
            min(height - 1, bottom_right[1]),
        )

        # Draw the grayscale square on the canvas
        # Since OpenCV uses BGR, set all channels to the grayscale value
        square_color = (calibrate_reflective_slm_value,) * 3
        cv2.rectangle(canvas, top_left, bottom_right, square_color, -1)

        # Display the grayscale value on the top-left corner
        text = f"Grayscale Value: {calibrate_reflective_slm_value}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        # Determine text color based on grayscale value for contrast
        if calibrate_reflective_slm_value > 128:
            font_color = (0, 0, 0)  # Black text for lighter squares
        else:
            font_color = (255, 255, 255)  # White text for darker squares
        thickness = 2
        text_position = (10, 30)  # Position near the top-left corner
        cv2.putText(
            canvas,
            text,
            text_position,
            font,
            font_scale,
            font_color,
            thickness,
            cv2.LINE_AA,
        )

        # Display the canvas
        cv2.imshow(window_name, canvas)

        # Wait for a key press for 10ms
        key = cv2.waitKey(10) & 0xFF  # Mask to get last 8 bits

        # Handle key presses for movement
        if key == ord("w"):
            y_center = max(half_side, y_center - large_step)
        elif key == ord("s"):
            y_center = min(height - half_side, y_center + large_step)
        elif key == ord("a"):
            x_center = max(half_side, x_center - large_step)
        elif key == ord("d"):
            x_center = min(width - half_side, x_center + large_step)
        elif key == ord("i"):
            y_center = max(half_side, y_center - small_step)
        elif key == ord("k"):
            y_center = min(height - half_side, y_center + small_step)
        elif key == ord("j"):
            x_center = max(half_side, x_center - small_step)
        elif key == ord("l"):
            x_center = min(width - half_side, x_center + small_step)
        # Handle key presses for grayscale adjustment
        elif key == ord("t"):
            # Increase grayscale value
            calibrate_reflective_slm_value = min(
                max_grayscale, calibrate_reflective_slm_value + grayscale_step
            )
        elif key == ord("g"):
            # Decrease grayscale value
            calibrate_reflective_slm_value = max(
                min_grayscale, calibrate_reflective_slm_value - grayscale_step
            )
        # Handle key presses for resizing
        elif key == ord("=") or key == ord("+"):
            half_side += size_step // 2
            # Ensure the square does not exceed canvas boundaries
            half_side = min(
                half_side, x_center, y_center, width - x_center, height - y_center
            )
        elif key == ord("-") or key == ord("_"):
            half_side = max(min_half_side, half_side - size_step // 2)
        elif key == 27:  # ESC key
            print("Exiting the application.")
            break

        # Optional: Print the current state (commented out to reduce console clutter)
        # print(f"Center: ({x_center}, {y_center}), Half Side: {half_side}, Grayscale: {calibrate_reflective_slm_value}")

    # Clean up and close the window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Specify the monitor index (0 for primary monitor)
    display_image_with_keyboard_control(screen_id=0)
