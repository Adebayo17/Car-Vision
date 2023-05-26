# variables
# mqtt id
HOST = "localhost"
PORT = 1883


topicsPublished = ["/mycar/ultrason/front/distance",
                    "/mycar/ultrason/front/velocity",
                    "/mycar/ultrason/back/distance",
                    "/mycar/ultrason/back/velocity",
                    "/mycar/camera_img",
                    "direction"
                    ]
messagesReceived = {
     'mode':'',
     'direction':''
}
topicsSubscribed = ["mode", "direction"]

directions = ["front", "back", "right", "left", "stop"]
modes = ["manuel", "automatic"]

