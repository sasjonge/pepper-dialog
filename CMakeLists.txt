cmake_minimum_required(VERSION 2.8.3)
project(dialogsystem)

### Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
)

catkin_package(
)

catkin_install_python(PROGRAMS ./nodes/rpc_server.py
                               ./nodes/sphinx_asr.py
                               ./nodes/gstreamer_sphinx.py
                               ./nodes/speechRecognizer.py
                               ./nodes/nao_speech.py 
                               ./nodes/dialogManager.py
                               ./nodes/netparamupdater.py
                               ./nodes/dialogCoreServerManager.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
