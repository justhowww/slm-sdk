from PIL import Image
import cv2
import numpy as np


def repeat_image(
    image_path,
    target_width,
    target_height,
    output_path=None,
    x_offset=0,
    y_offset=0,
    scale=1,
    foundamental_size=0,
):
    """
    Repeats a grayscale image to fit a target size in both x and y directions, with an optional offset.

    Args:
        image_path (str): Path to the input image.
        target_width (int): Target width of the output image.
        target_height (int): Target height of the output image.
        output_path (str, optional): Path to save the resulting image. If None, the image will be displayed.
        x_offset (int): Horizontal offset to shift the center of the image after repeating.
        y_offset (int): Vertical offset to shift the center of the image after repeating.

    Returns:
        None
    """
    # Load the image
    image = Image.open(image_path)  # Convert to grayscale

    # Convert image to a NumPy array
    image_array = np.array(image)
    original_height, original_width = image_array.shape
    original_height, original_width = int(original_height*scale), int(original_width*scale)
    image_array = cv2.resize(
                image_array,
                (original_height, original_width),
                interpolation=cv2.INTER_CUBIC,
            )

    # Calculate the number of repeats needed
    repeat_x = -(-target_width // original_width)  # Ceiling division
    repeat_y = -(-target_height // original_height)  # Ceiling division
    if repeat_x % 2 == 0:
        repeat_x += 1
    if repeat_y % 2 == 0:
        repeat_y += 1

    # Repeat the image using NumPy's tile function
    repeated_array = np.tile(image_array, (repeat_y, repeat_x))

    # Apply offsets by rolling the repeated array
    repeated_array = np.roll(
        repeated_array, shift=y_offset - target_height // 2, axis=0
    )  # Vertical shift
    repeated_array = np.roll(
        repeated_array, shift=x_offset - target_width // 2, axis=1
    )  # Horizontal shift
    # Crop to the target size
    cropped_array = repeated_array[
        repeated_array.shape[0] // 2
        - target_height // 2 : repeated_array.shape[0] // 2
        + target_height // 2
        + 1,
        repeated_array.shape[1] // 2
        - target_width // 2 : repeated_array.shape[1] // 2
        + target_width // 2
        + 1,
    ]

    # Convert the cropped array back to an image
    repeated_image = Image.fromarray(cropped_array)

    # Save or display the resulting image
    if output_path:
        repeated_image.save(output_path)
        print(f"Repeated image saved to {output_path}")
    else:
        cropped_array = np.stack((cropped_array,) * 3, axis=-1)

        return cropped_array


# Example usage
if __name__ == "__main__":
    # Input parameters
    input_image_path = "./optical_interpolation_pattern/remapped_mask.png"  # Replace with your input image path
    output_image_path = "./optical_interpolation_pattern/repeated_remapped_mask.png"  # Replace with your output image path or None
    target_width = 1920  # Target width of the output image
    target_height = 1080  # Target height of the output image
    x_offset, y_offset = (1066, 510)  # Dynamically calculate based on screen size
    # x_offset, y_offset = (0, 0)  # Dynamically calculate based on screen size

    repeat_image(
        input_image_path,
        target_width,
        target_height,
        output_image_path,
        x_offset,
        y_offset,
    )
