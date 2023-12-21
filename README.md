# MRC-FarmBots

## Demo

<img src="https://github.com/omar-basheer/MRC-Farmbots/blob/main/mrc_demo.gif" width="1170" height="440"/>

Note: Video sped up for demo purposes

## Overview
This repository contains the codebase for the robotic farm project. The project involves the development of an autonomous robotic system capable of navigating a farm space, collecting fruits, and executing tasks assigned by a central server.

## Features
* Open-Loop Control: The clients use an open-loop control mechanism to navigate through the farm space, executing predefined sequences of movements and turns.

* Client-Server Communication: The server communicates with multiple clients, assigning tasks based on the farm's state and the clients' real-time positions.

* Dynamic Task Assignment: The server dynamically assigns tasks to clients, considering factors such as distance, fruit availability, and the clients' statuses.

## Requirements
Python
Pybricks MicroPython for EV3 robots

## Getting Started
Clone the repository.

Install the necessary dependencies. 

Run the server script on the central unit.

Run the client scripts on the robotic units.

## Usage
Customize farm space, fruit locations, and grid size in the server script.

Modify client behavior, movement sequences, and task execution in the client script.

Ensure Bluetooth connections are established between the server and clients.
