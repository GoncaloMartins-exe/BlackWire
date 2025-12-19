cmake_minimum_required(VERSION 3.16)

project(BlackWire VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(BlackWire
    src/main.cpp
    src/ui/MainWindow.h
    src/ui/MainWindow.cpp
    src/ui/MainWindow.ui
    src/resources/resources.qrc
)

target_include_directories(BlackWire PRIVATE src/ui)

target_link_libraries(BlackWire PRIVATE Qt6::Widgets)

if(WIN32)
    set_property(TARGET BlackWire PROPERTY WIN32_EXECUTABLE ON)
endif()

if(WIN32)
    add_custom_command(TARGET BlackWire POST_BUILD
        COMMAND ${Qt6_DIR}/../../../bin/windeployqt.exe $<TARGET_FILE:BlackWire>
        COMMENT "A copiar DLLs do Qt..."
    )
endif()