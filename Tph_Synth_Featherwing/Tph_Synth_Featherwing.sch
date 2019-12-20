EESchema Schematic File Version 4
LIBS:Tph_Synth_Featherwing-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 6
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 1455 1955 1800 1095
U 5DCBF5A8
F0 "Boost_Converter" 50
F1 "boost_converter.sch" 50
F2 "VBAT" I L 1455 2305 50 
F3 "5V_OUT" O R 3255 2245 50 
F4 "VUSB" I L 1455 2720 50 
$EndSheet
$Sheet
S 3990 1915 1770 1095
U 5DCBF5D4
F0 "Negative Rail Generator" 50
F1 "negative_rail.sch" 50
F2 "5V" I R 5760 2130 50 
F3 "-5V" O R 5760 2655 50 
$EndSheet
$Sheet
S 6685 2925 1760 1095
U 5DCBF60B
F0 "Controlled Gain Output" 50
F1 "quad_opamp_gain.sch" 50
F2 "+5V" I L 6685 3100 50 
F3 "-5V" I L 6685 3255 50 
F4 "VA_out" O R 8445 3275 50 
F5 "VB_out" O R 8445 3460 50 
F6 "VC_out" O R 8445 3655 50 
F7 "IAC_out" O R 8445 3810 50 
F8 "VA_in" I L 6685 3450 50 
F9 "VB_in" I L 6685 3605 50 
F10 "VC_in" I L 6685 3760 50 
F11 "IAC_in" I L 6685 3925 50 
$EndSheet
$Sheet
S 3930 3930 1810 1185
U 5DCBF63F
F0 "DAC Based AC Generator" 50
F1 "dac_ac_gen.sch" 50
F2 "VOUTA" O R 5740 4185 50 
F3 "VOUTB" O R 5740 4385 50 
F4 "VOUTC" O R 5740 4580 50 
F5 "VOUTD" O R 5740 4805 50 
F6 "SCL" I L 3930 4360 50 
F7 "SDA" I L 3930 4670 50 
$EndSheet
$Sheet
S 1430 3965 1825 1185
U 5DECF7CD
F0 "Feathewing Headers" 50
F1 "featherwing.sch" 50
F2 "F_SCL" O R 3255 4255 50 
F3 "F_SDA" O R 3255 4490 50 
F4 "VBAT" O L 1430 4405 50 
F5 "VUSB" O L 1430 4120 50 
$EndSheet
$Comp
L Connector_Generic:Conn_01x04 J2
U 1 1 5DF7BE31
P 10020 3035
F 0 "J2" H 10100 3027 50  0000 L CNN
F 1 "Conn_01x04" H 10100 2936 50  0000 L CNN
F 2 "Connector_Molex:Molex_Nano-Fit_105314-xx04_2x02_P2.50mm_Horizontal" H 10020 3035 50  0001 C CNN
F 3 "~" H 10020 3035 50  0001 C CNN
	1    10020 3035
	1    0    0    -1  
$EndComp
$Comp
L Connector:AudioJack3 J1
U 1 1 5DF7C0C6
P 9955 4265
F 0 "J1" H 9675 4198 50  0000 R CNN
F 1 "AudioJack3" H 9675 4289 50  0000 R CNN
F 2 "Connector_Audio:Jack_3.5mm_CUI_SJ-3523-SMT_Horizontal" H 9955 4265 50  0001 C CNN
F 3 "~" H 9955 4265 50  0001 C CNN
	1    9955 4265
	-1   0    0    1   
$EndComp
Wire Wire Line
	9820 2935 8570 2935
Wire Wire Line
	8570 2935 8570 3275
Wire Wire Line
	8570 3275 8445 3275
Wire Wire Line
	8445 3460 8740 3460
Wire Wire Line
	8740 3460 8740 3035
Wire Wire Line
	8740 3035 9820 3035
Wire Wire Line
	9820 3135 8915 3135
Wire Wire Line
	8915 3135 8915 3655
Wire Wire Line
	8915 3655 8445 3655
Wire Wire Line
	9100 3810 8445 3810
Wire Wire Line
	9755 4165 9100 4165
Wire Wire Line
	9100 4165 9100 3810
$Comp
L power:GND #PWR08
U 1 1 5DF77235
P 9820 3235
F 0 "#PWR08" H 9820 2985 50  0001 C CNN
F 1 "GND" H 9825 3062 50  0000 C CNN
F 2 "" H 9820 3235 50  0001 C CNN
F 3 "" H 9820 3235 50  0001 C CNN
	1    9820 3235
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR09
U 1 1 5DF7740C
P 9755 4365
F 0 "#PWR09" H 9755 4115 50  0001 C CNN
F 1 "GND" H 9760 4192 50  0000 C CNN
F 2 "" H 9755 4365 50  0001 C CNN
F 3 "" H 9755 4365 50  0001 C CNN
	1    9755 4365
	1    0    0    -1  
$EndComp
Wire Wire Line
	6685 3450 5875 3450
Wire Wire Line
	5875 3450 5875 4185
Wire Wire Line
	5875 4185 5740 4185
Wire Wire Line
	6085 3605 6685 3605
Wire Wire Line
	6085 3605 6085 4385
Wire Wire Line
	5740 4385 6085 4385
Wire Wire Line
	6685 3760 6290 3760
Wire Wire Line
	6290 3760 6290 4580
Wire Wire Line
	6290 4580 5740 4580
Wire Wire Line
	5740 4805 6490 4805
Wire Wire Line
	6490 4805 6490 3925
Wire Wire Line
	6685 3925 6490 3925
Wire Wire Line
	6145 2655 6145 3255
Wire Wire Line
	6145 2655 5760 2655
Wire Wire Line
	6685 3255 6145 3255
Wire Wire Line
	6685 3100 6280 3100
Wire Wire Line
	6280 3100 6280 2130
Wire Wire Line
	6280 2130 5760 2130
Wire Wire Line
	3255 2245 3555 2245
Wire Wire Line
	3555 2245 3555 1350
Wire Wire Line
	3555 1350 6280 1350
Wire Wire Line
	6280 1350 6280 2130
Connection ~ 6280 2130
Wire Wire Line
	1430 4120 1165 4120
Wire Wire Line
	1165 4120 1165 2720
Wire Wire Line
	1165 2720 1455 2720
Wire Wire Line
	1455 2305 835  2305
Wire Wire Line
	835  2305 835  4405
Wire Wire Line
	835  4405 1430 4405
Wire Wire Line
	3930 4360 3460 4360
Wire Wire Line
	3460 4360 3460 4255
Wire Wire Line
	3460 4255 3255 4255
Wire Wire Line
	3255 4490 3470 4490
Wire Wire Line
	3470 4490 3470 4670
Wire Wire Line
	3470 4670 3930 4670
$Comp
L Graphic:Logo_Open_Hardware_Small LOGO1
U 1 1 5DFCD1ED
P 7385 6865
F 0 "LOGO1" H 7385 7140 50  0001 C CNN
F 1 "Logo_Open_Hardware_Small" H 7385 6640 50  0001 C CNN
F 2 "Symbol:OSHW-Logo2_7.3x6mm_SilkScreen" H 7385 6865 50  0001 C CNN
F 3 "~" H 7385 6865 50  0001 C CNN
	1    7385 6865
	1    0    0    -1  
$EndComp
$EndSCHEMATC
