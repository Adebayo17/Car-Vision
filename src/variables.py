# variables

# Configuration de la webcam
cam_id = 0
cam_width = 640
cam_height = 480


HOST = "localhost"
PORT = 1883


topicsPublished = ["/mycar/ultrason/front/distance",
                    "/mycar/ultrason/front/velocity",
                    "/mycar/ultrason/back/distance",
                    "/mycar/ultrason/back/velocity",
                    "/mycar/camera_img",
                    "/mycar/direction"
                    ]
messagesReceived = {}
topicsSubscribed = ["/mycar/mode", "/mycar/direction"]

directions = ["front", "back", "right", "left", "stop"]
modes = ["manuel", "automatic"]

