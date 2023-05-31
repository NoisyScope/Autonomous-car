import cv2
import time

# Path to the video file
video_path = 'vid1.mp4'  # Replace with the actual path to your video file

# Create a VideoCapture object to read from the video file
cap = cv2.VideoCapture(video_path)

# Define the region of interest coordinates (x, y, width, height)
roi_x = 0
roi_y = 300
roi_width = 1280
roi_height = 300

# Define the y-coordinate of the horizontal line
line_y = roi_y + roi_height // 2  # Adjust the line position as needed

# Define the physical distance between the two vertical contours in centimeters
physical_distance_cm = 60

while True:
    # Read the current frame from the video file
    ret, frame = cap.read()

    # Check if the video has reached the end
    if not ret:
        break

    # Get the region of interest from the frame
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width].copy()

    # Convert the region of interest to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale ROI to extract white regions
    _, thresholded = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)

    # Find contours of white regions
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter vertical contours based on a minimum width threshold
    min_contour_width = 10
    vertical_contours = [cnt for cnt in contours if cv2.boundingRect(cnt)[2] >= min_contour_width]

    # Draw vertical contours on the ROI
    cv2.drawContours(roi, vertical_contours, -1, (0, 255, 0), 2)

    # Calculate the pixel distance between the two vertical contours
    if len(vertical_contours) >= 2:
        contour1_x = cv2.boundingRect(vertical_contours[0])[0]
        contour2_x = cv2.boundingRect(vertical_contours[1])[0]
        pixel_distance = abs(contour2_x - contour1_x)
        cv2.putText(roi, f"Pixel Distance: {pixel_distance}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Calculate the conversion factor from pixels to centimeters
        conversion_factor = physical_distance_cm / pixel_distance

        # Calculate the physical distance between the two vertical contours in centimeters
        physical_distance = conversion_factor * pixel_distance
        cv2.putText(roi, f"Physical Distance: {physical_distance:.2f} cm", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Calculate the middle point between the contours
        middle_point_x = (contour1_x + contour2_x) // 2
        cv2.circle(roi, (middle_point_x, line_y), 5, (0, 0, 255), -1)

        # Calculate the center of the image along the x-axis
        image_center_x = roi_width // 2

        # Calculate the difference between the middle point and the center of the image along the x-axis
        difference_x = middle_point_x - image_center_x

        cv2.putText(roi, f"Difference X: {difference_x}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Draw a horizontal line to indicate the pixels being measured
    cv2.line(roi, (0, line_y), (roi_width, line_y), (255, 0, 0), 2)

    # Display the original frame and the ROI with vertical contours, pixel distance, line, middle point, and physical distance
    cv2.imshow('Original Frame', frame)
    cv2.imshow('ROI with Vertical Contours and Line', roi)
    time.sleep(0.4)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the windows
cap.release()
cv2.destroyAllWindows()