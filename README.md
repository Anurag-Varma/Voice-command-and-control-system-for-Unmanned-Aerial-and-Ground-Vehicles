# Voice-command-and-control-system-for-Unmanned-Aerial-and-Ground-Vehicles
Voice command and control system for Unmanned Aerial and Ground Vehicles


Speech/Voice is the expression used to communicate between two humans. 
Speech is becoming a major source for controlling IOT Devices. Speech has become a major challenge to control IOT devices using commands. 
The technology of UAV/UGV is picking up, controlling of these devices is done through a joystick which has certain actions and can be controlled only within a range. Previously, Conventional Models like Hidden Markov Model is used for Speech recognition. 
There are many limitations of this model such as it is computationally expensive, takes longer time to compute, amount of data required to train the model is large, it takes trial and error method into consideration, etc. 
There is a requirement to develop a system with high performance and high accuracy. Communicating speech over network is also a major challenge. For this, we use Virtual Private Network (VPN – Zero Tier) which allows to communicate over a large range over internet. 
To overcome the limitations of HMM, a Deep Learning Model is developed with better performance and high accuracy. The Deep Learning Model for Speech/Voice Recognition using Attention Recurrent Neural Network (AttRNN) is developed. 
The development of Deep Learning Model for Speech Recognition has achieved an accuracy of 94.5%. 
The training, testing and validation for the DL Model is carried out using Google Speech Command Dataset V2 which consists of 35-word recognition voices for 35 different commands with each voice audio file of 1 second long. 
Since there is requirement of only certain commands, we use 24 of them for the training and testing the model.  This DL model provides good performance which can convert voice commands into certain actions. 
In this paper, we discuss the integration of DL Model with UAV/UGV devices for controlling using speech-based command. The advantage of integration of DL Model and UAV/UGV device enables us to control the device using voice-based command through cellular module with unlimited range. 
A voice command is given through a microphone of Laptop/Mobile which recognizes the command and hence the action is performed by the device.
