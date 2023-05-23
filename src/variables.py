HOST = "localhost"
PORT = 1883

topicsPublished = ["/mycar/ultrason/front/distance",
                    "/mycar/ultrason/front/velocity",
                    "/mycar/ultrason/back/distance",
                    "/mycar/ultrason/back/velocity",
                    "/mycar/camera_img",
                    "/mycar/direction"
                    ]
topicsSubscribed = ["/mycar/direction",
                    "/mycar/state",
                    "/mycar/mode"
                    ]

directions = ["front", "back", "right", "left"]
direction = ""

modes = ["manual", "automatic"]
mode = modes[0]
