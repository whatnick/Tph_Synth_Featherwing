EESchema Schematic File Version 4
LIBS:Tph_Synth_Featherwing-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 6 6
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L adafruit_featherwing:ADAFRUIT_FEATHERWING MS1
U 1 1 5DECFEA6
P 4790 3370
F 0 "MS1" H 4790 3370 45  0001 C CNN
F 1 "ADAFRUIT_FEATHERWING" H 4790 3370 45  0001 C CNN
F 2 "featherwing:adafruit_featherwing" H 4790 3370 50  0001 C CNN
F 3 "" H 4790 3370 50  0001 C CNN
	1    4790 3370
	1    0    0    -1  
$EndComp
Text HLabel 6390 1870 1    50   Output ~ 0
F_SCL
Text HLabel 6490 1870 1    50   Output ~ 0
F_SDA
$Comp
L power:GND #PWR06
U 1 1 5DECF2D0
P 5290 3570
F 0 "#PWR06" H 5290 3320 50  0001 C CNN
F 1 "GND" H 5295 3397 50  0000 C CNN
F 2 "" H 5290 3570 50  0001 C CNN
F 3 "" H 5290 3570 50  0001 C CNN
	1    5290 3570
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR07
U 1 1 5DECF43D
P 5090 3570
F 0 "#PWR07" H 5090 3420 50  0001 C CNN
F 1 "+3V3" H 5105 3743 50  0000 C CNN
F 2 "" H 5090 3570 50  0001 C CNN
F 3 "" H 5090 3570 50  0001 C CNN
	1    5090 3570
	-1   0    0    1   
$EndComp
Text HLabel 5590 1870 1    50   Output ~ 0
VUSB
Text HLabel 5390 1870 1    50   Output ~ 0
VBAT
$EndSCHEMATC
