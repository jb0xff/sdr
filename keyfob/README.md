# Mitsubishi Keyfob Hacking

## Introduction
While browsing youtube for CCC content the video of Samy Kumkar popped up 
[Link](https://www.youtube.com/watch?v=iSSRaIU9_Vc&t=1s&ab_channel=SamyKamkar).
He describes how he is hacking Garage Doors with a Matel device. This got my intrest started and 
after faling down the rabbit hole I had ordered an hackRF one and some other parts.

## My "old" car and his keyfob

As I did not have a garage door I was looking at my keyfob of my Mitsubshi Lancer built in the year 2001. I still own this car to date.
The Keyfob identified as an _G8D-525M-A Automotive Security Transmitter_. The FCC Page gives a first insight into this 
keyfob [Link](https://fccid.io/OUCG8D-525M-A). After setting up my hackRF I captured the first signals on ~433Mhz. Besides that I did not have much of an idea how to go forward from here.

## Mobile Communication and GNU Radio
After watching most of Micheal Ossmans SDR Video Series [Link](https://greatscottgadgets.com/sdr/) I knew I had
to dive into GNU Radio Companion. At the same I started a module at my university called _Mobile Communications_
which influenced and/or fueld my intrest in this field even more.

## Analysing the Signal

Sofar I knew that the keyfob was transmitting at 433Mhz. After reading allong I learned that the signal form
I recorded using _SDRConsole_ and hackRF one, points towards a FSK modulated singal. Identified by symetrical
singal shape with two peaks.

Derived from that information is started googling how one would extract information from a signal using GRC. 
I found this tutorial by _eapbg_ [Link](https://www.youtube.com/watch?v=enLbgn1qBS4&t=2545s&ab_channel=eapbg).
With his help I assume I was able to decode the signal from the keyfob: 



