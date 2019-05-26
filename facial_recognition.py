# Acknowledgement:
# The code for this class is adapted from facial recognition
# code from the week 9 tutorial by Mathew Bolger
import cv2
import face_recognition
import pickle
import os
import time
import imutils
from imutils import paths
from imutils.video import VideoStream


class FacialRecognition:
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
        # Specify location of facial data
        self.__data_dir = data_dir
        # Specify file name of encodings storage
        self.__encodings_path = encodings_path
        # Specify detection method for facial detection
        self.__detect_model = detect_model

    def recognize_user(self):
        """
        Recognizes an individual with a webcam and returns their username.
        Requires that a user has registered with facial recognition.

        Returns:
            If user is recognized, returns their username as a string.
            If user is recognized as unknown too many times, returns None.

        """
        # Load registered faces encodings file
        data = pickle.loads(open(self.__encodings_path, "rb").read())
        # Initialize video stream and wait for it to warm up
        vs = VideoStream(src=0).start()
        time.sleep(2)
        # Loop over video stream and look for faces in the video stream
        unknown_count = 0
        while True:
            # Capture frame
            frame = vs.read()
            # Convert frame from BGR to RBG
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize frame for faster processing
            rgb_frame = imutils.resize(frame, width=240)
            # Get bounding boxes for each face in the frame
            boxes = face_recognition.face_locations(rgb_frame,
                                                    model=self.__detect_model)
            # Compute facial embeding for faces
            encodings = face_recognition.face_encodings(rgb_frame, boxes)
            # Initialize names list for frame
            names = []
            # Check each encoding for matches to existing encodings
            for encoding in encodings:
                matches = face_recognition.compare_faces(
                    data["encodings"], encoding)
                name = "Unknown"
                # Check if there is a match
                if True in matches:
                    # Find all matching indexes and initialize dictionary for
                    # number of times a face in the encoded frame is matched
                    matchedIndexes = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # Loop over matched indexes and count face recognitions
                    for i in matchedIndexes:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                    # Determine recognized face with largest count of
                    # recognitions or "votes"
                    name = max(counts, key=counts.get)
                # Update name list
                names.append(name)
            # Check each name in names list
            for name in names:
                # If they are named as unknown, increment the unknown counter
                if name is "Unknown":
                    unknown_count += 1
                # If they are as any other user, immediately return that user
                else:
                    vs.stop()
                    return name
            # If unknown count has reached the limit, simply return None
            if unknown_count >= 10:
                vs.stop()
                return None

    def register_user(self, username):
        """
        Registers a user in the facial recognition database.
        First captures 10 images from user and writes them to file.
        Then encodes the images and stores encoding in a pickle file.

        Args:
            username (str): The username of the user that will be registered.

        """
        # Start up camera
        camera = self.__get_camera()
        # Load prebuilt classifier for face detection
        face_detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
        # Create folder for images
        folder = "%s/%s" % (self.__data_dir, username)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # Capture face images until sufficent number is written
        img_count = 0
        while img_count < 10:
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
                img_path = "%s/%d.jpg" % (folder, img_count)
                cv2.imwrite(img_path, frame[y: y + h, x: x + w])
                img_count += 1
        # Release camera
        camera.release()
        # Do encoding of all images
        print("Please wait for encoding to complete...")
        self.encode_images()

    def encode_images(self):
        """
        Encodes all existing images to a pickle file.
        Name of encoding file is defined on initialization.

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
            encodings = face_recognition.face_encodings(rgb_image, boxes)
            # Add encodings to encoding list alongside associate username
            for encoding in encodings:
                allEncodings.append(encoding)
                allNames.append(name)
        # Dump facial encodings to encodings file
        data = {"encodings": allEncodings, "names": allNames}
        with open(self.__encodings_path, "wb") as encode_file:
            encode_file.write(pickle.dumps(data))

    def __get_camera(self):
        """
        Starts, sets up and returns a variable to the camera for use.

        Returns:
            A cv2 camera object that can be used for capturing images.

        """
        # Start camera
        camera = cv2.VideoCapture(0)
        # Set width and height
        camera.set(3, 640)
        camera.set(4, 480)
        # Return camera object
        return camera

