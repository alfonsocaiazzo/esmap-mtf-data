** Create the database to upload on the site **
** 9 datasets 

******************************************************************
**     		 Honduras MTF Household Survey                      **
**                                                              **
**                                                              **
**  Country: Honduras	YEAR:  2017    		    	            **
**                                                              **
**  Program Name:  Honduras_public_datasets.do     		        **
**                                                              **
**  Input Data Sets: "$clean" & "$reshape"                      **
**                                                              **
**  Description: Public Honduras MTF database     			    **
**                                                              **
**  Household: HH		    			                        **
**                                                              **
**  Program first written: May 20, 2020 (Lidia)	                **
**  Program last modified:                                      **
**                                                              **
******************************************************************

clear all
set more off

global UPI "550946"
global user "C:\Users\WB$UPI\WBG\Elisa Portale - 1_mtf_energy_global_survey"

global clean "$user\10_Data synchronization\9_Honduras\Data\clean"
global reshape "$user\10_Data synchronization\9_Honduras\Data\clean\reshape"
global do "$user\10_Data synchronization\9_Honduras\Dofiles"

* 1) MTF_HN17_HH_clean.dta
use "$clean\MTF_HN17_HH_clean", clear

order parentid1, first

label define sf_any 1 "Yes" 0 "No", modify
la values sf_any sf_any

codebook, c

save "$public\MTF_HN17_HH_clean", replace

* 2) MTF_HN17_C_solar_clean
use "$clean\MTF_HN17_C_solar_clean", clear

codebook, c

save "$public\MTF_HN17_C_solar_clean", replace

* 3) MTF_HN17_I_ALL
use "$clean\MTF_HN17_I_ALL", clear

order parentid1, first
order idhh-factor, after(parentid1)

codebook, c

save "$public\MTF_HN17_I_ALL", replace

* 4) MTF_HN17_F_clean

use "$clean\MTF_HN17_F_clean", clear

codebook, c 

save "$public\MTF_HN17_G_clean", replace

* 5) MTF_HN17_G_clean

use "$clean\MTF_HN17_G_clean", clear

codebook, c 

save "$public\MTF_HN17_G_clean", replace

* 6) MTF_HN17_H_clean.dta
use "$clean\MTF_HN17_H_clean.dta", clear

order parentid1, first
order idhh-factor, after(parentid1)
// Variable h012 = "En los últimos 7días, ¿qué cantidad consumió su hogar?" It cannot be negative. Negative values recoded as zeros.
recode h012 -5 = 0
recode h012 -4 = 0

codebook, c
save "$public\MTF_HN17_H_clean", replace

* 7) MTF_HN17_N (Dataset taken from "$reshape" because it contained more variables)
use "$reshape\MTF_HN17_N", clear

codebook, c

save "$reshape\MTF_HN17_N", replace

* 8) MTF_HN17_P (Dataset taken from "$reshape" because not available in the "$clean" folder)
use "$reshape\MTF_HN17_P", clear

codebook, c

save "$reshape\MTF_HN17_P", replace

* 9) MTF_HN17_Q (Dataset taken from "$reshape" because not available in the "$clean" folder)
use "$reshape\MTF_HN17_Q", clear

codebook, c

save "$public\MTF_HN17_Q", replace

