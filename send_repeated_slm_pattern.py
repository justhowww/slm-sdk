import cv2
import numpy as np
import screeninfo
from repeat_pattern import repeat_image


def display_image_with_keyboard_control(screen_id, image_path, circular_wrapping=False):
    """
    Displays an image on the specified screen with keyboard controls to move, resize, and flip the image.
    Optionally enables circular wrapping when shifting the image.

    Parameters:
    - screen_id (int): The index of the monitor to display the image on.
    - image_path (str): Path to the image file.
    - circular_wrapping (bool): If True, enables circular wrapping of the image around screen edges.
    """
    # Get the size and position of the screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height

    # Load the image
    # original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    x_offset, y_offset = 819, 439  # Dynamically calculate based on screen size

    # Get original image dimensions
    original_image = repeat_image(
        image_path, width, height, x_offset=x_offset, y_offset=y_offset
    )
    if original_image is None:
        print(f"Error: Unable to load image from {image_path}")
        return
    original_h, original_w = original_image.shape[:2]
    # Initial center position (dynamically set to screen center)

    # Initial deltas[delta_index]
    deltas = [0.7, 1, 1.4]
    delta_index = 2

    # Flip state flags
    flip_horizontal = False
    flip_vertical = False

    window_name = "projector"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, screen.x, screen.y)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    status = "image"  # Start with a blank canvas

    while True:

        # Set display as mask or blank
        if status == "image":
            canvas = repeat_image(
                image_path,
                width,
                height,
                x_offset=x_offset,
                y_offset=y_offset,
                scale=deltas[delta_index],
            )
        else:
            canvas = (
                np.ones((height, width, 3), dtype=np.uint8) * 180
            )  # Gray background

        # Optional: Print the current position, size, and flip status for debugging
        print(
            f"Offset (x_offset, y_offset): ({x_offset}, {y_offset}), "
            f"Delta Size: {deltas[delta_index]}, "
            f"Flip Horizontal: {flip_horizontal}, Flip Vertical: {flip_vertical}, "
        )

        # Display the canvas in the window
        cv2.imshow(window_name, canvas)

        # Wait for a key press for 10 ms
        key = cv2.waitKey(10) & 0xFF  # Mask to get the last 8 bits

        # * Logic Control
        # Handle keyboard inputs to move the image or adjust its size
        if key == ord("w"):  # Move up
            y_offset -= 10
        elif key == ord("s"):  # Move down
            y_offset += 10
        elif key == ord("a"):  # Move left
            x_offset -= 10
        elif key == ord("d"):  # Move right
            x_offset += 10
        elif key == ord("i"):  # Smaller move up
            y_offset -= 1
        elif key == ord("k"):  # Smaller move down
            y_offset += 1
        elif key == ord("j"):  # Smaller move left
            x_offset -= 1
        elif key == ord("l"):  # Smaller move right
            x_offset += 1

        elif key == ord("="):  # Increase size
            # Increase deltas[delta_index]
            delta_index = delta_index + 1 if delta_index < len(deltas) - 1 else 0
            print(f"change delta to {deltas[delta_index]}")

        elif key == ord("-"):  # Decrease size
            # Prevent deltas[delta_index] from making the image too small
            delta_index = delta_index - 1 if delta_index > 0 else len(deltas) - 1
            print(f"change delta to {deltas[delta_index]}")

        elif key == ord("f"):  # Toggle horizontal flip
            flip_horizontal = not flip_horizontal
            print(f"Horizontal Flip set to: {flip_horizontal}")
        elif key == ord("g"):  # Toggle vertical flip
            flip_vertical = not flip_vertical
            print(f"Vertical Flip set to: {flip_vertical}")

        elif key == ord(" "):  # Toggle between image and blank
            if status == "image":
                status = "blank"
            else:
                status = "image"
        elif key == 27:  # Escape key to exit
            break

        # If circular wrapping is enabled, keep offsets within screen bounds
        x_offset %= width
        y_offset %= height

    # Clean up and close the window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    screen_id = 0

    # Replace with your actual image path
    # image_path = "./optical_interpolation_pattern/symmetric_phase_pattern.png" # cifar nn
    # image_path = "./optical_interpolation_pattern/zero_insertion/remapped_mask_v3.png" # cifar zero insertion
    # image_path = "./optical_interpolation_pattern/imagenet_nn/remapped_mask.png" # imagenet nn
    image_path = "./optical_interpolation_pattern/imagenet_zero_insertion/remapped_mask.png"  # imagenet zero insertion

    # Set circular_wrapping to True to enable wrapping
    display_image_with_keyboard_control(screen_id, image_path, circular_wrapping=True)
