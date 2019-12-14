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
S 1385 1895 1800 1095
U 5DCBF5A8
F0 "Boost_Converter" 50
F1 "boost_converter.sch" 50
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
F4 "5V" O R 3255 4725 50 
$EndSheet
$EndSCHEMATC
