import cv2
import face_recognition
import pickle
import os
from imutils import paths


class Facial_recognition:
    """
    Class for handling facial recognition functionality.

    """

    def __init__(self, data_dir="facial_data",
                 encodings_path="encodings.pickle",
                 detect_model="hog",):
        """
        Constructor for facial recognition.

        Args:
            data_dir (:obj:`str`, optional): Directory of where facial
                recognition data is stored. Default is "facial_data".
            encodings_path (:obj:`str`, optional): Path of file used to
                store face encodings. Default is "encodings.pickle".
            detect_model (:obj:`str`, optional): Model of detection used
                when encoding and recognizing faces. Default is "hog".

        """
        # Check if facial data directory exists, creating one if not
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        # Specify location of facial data
        self.__data_dir = data_dir
        # Specify file name of encodings storage
        self.__encodings_path = encodings_path
        # Specify detection method for facial detection
        self.__detect_model = detect_model

    def register_user(self, username):
        """
        Registers a user in the facial recognition database.
        First captures 10 images from user and writes them to file.
        Then encodes the images and stores encoding in a pickle file.

        Args:
            username (str): The username of the user that will be registered.

        """
        # Start up camera
        camera = self.get_camera()
        # Load prebuilt classifier for face detection
        face_detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
        # Capture face images until sufficent number is written
        img_count = 0
        while img_count <= 10:
            # Wait for user to press enter before capturing image
            key = input("Press enter to capture image %d" % (img_count + 1))
            # Capture frame
            ret, frame = camera.read()
            # If frame capture was not successful, try again
            if not ret:
                print("Capture failed, try again.")
                continue
            # Convert frame into grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Get all faces in frame
            faces = face_detector.detectMultiScale(gray_frame, 1.3, 5)
            # If there are not detected faces, try again
            if len(faces) == 0:
                print("No face detected, try again.")
            # Write faces to file
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                img_name = "%s/%d" % (self.__data_dir, img_count)
                cv2.imwrite(img_name, frame[y: y + h, x: x + w])
                img_count += 1
        # Release camera
        camera.release()
        # Do encoding of all images
        self.encode_images()

    def encode_images(self):
        """
        Encodes all existing images to a pickle file.

        """
        # Get a list of image paths
        imagePaths = list(paths.list_images(self.__data_dir))
        # Initialize encodings and names
        allEncodings = []
        allNames = []
        # Loop over image paths
        for(i, imagePath) in enumerate(imagePaths):
            # Get associated username for image
            name = imagePath.split(os.path.sep)[-2]
            # Load image and convert it from opencv to dlib RGB
            image = cv2.imread(imagePath)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Detect bounding boxes for each face in the image
            boxes = face_recognition.face_locations(rgb_image,
                                                    model=self.__detect_model)
            # Compute facial embedding for faces
            encodings = face_recognition.face_locations(rgb_image, boxes)
            # Add encodings to encoding list alongside associate username
            for encoding in encodings:
                allEncodings.append(encoding)
                allNames.append(name)
        # Dump facial encodings to pickle file
        data = {"encodings": allEncodings, "names": allNames}
        with open(self.__encodings_path, "wb") as encode_file:
            encode_file.write(pickle.dumps(data))

    def get_camera(self):
        """
        Starts, sets up and returns a variable to the camera for use

        Returns:
            A cv2 camera object that can be used for capturing images

        """
        # Start camera
        camera = cv2.VideoCapture(0)
        # Set width and height
        camera.set(3, 640)
        camera.set(4, 480)
        # Return camera object
        return camera
