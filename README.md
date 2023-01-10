## Code to Reproduce Analysis 

Author: Blaine Fritz 

This repository provides all of the code and data 
to reproduce the analysis and figures presented in the mansuscript, 
*Differentially tolerant and metabolically distinct subpopulations 
in shaken batch cultures of Pseudomonas aeruginosa*. This manuscript has been 
submitted to the journal, Biofilm, in January 2023. 

### Prereqs

To reproduce the analysis, you will need to have conda or miniconda installed. 
You'll also need R/Rstudio to run the R scripts, as well as the required packages
installed (listed in the scripts)

### To reproduce the analysis: 

1. Clone the git repository to desired local location. 

`git clone git@github.com:bgfritz1/Pa_Subpopulations.git`

2. Navigate to the `/path/to/Pa_Subpopulations` where you cloned the repository. 

3. Create the conda environment 

`conda env create -f ./Scripts/compare_plank_agg_GFP.yaml`

4. Activate the conda environment 

`conda activate compare_plank_agg_GFP`

5. Run the analysis of the planktonic/aggregate GFP analysis. 

`python ./Scripts/compare_plank_Agg_GFP.py`

6. To rerun the other analysis and generate the figures, open RStudio and make sure that you're working
directory is set to `/path/to/Pa_Subpopulations`.

7. In RStudio, open the markdown file `./Project_notebook.Rmd`. Ensure that all of the appropriate 
packages are installed. CLick "Run -> Restart R and Run all Chunks". This should run the entire analysis without errors.

8. Generated figures will be outputted to `./figures/`. 


### R environment

I was able to run the analysis with the following R environment 

	R version 4.2.2 (2022-10-31 ucrt)
	Platform: x86_64-w64-mingw32/x64 (64-bit)
	Running under: Windows 10 x64 (build 19045)
	
	Matrix products: default
	
	locale:
	[1] LC_COLLATE=English_United States.utf8  LC_CTYPE=English_United States.utf8    LC_MONETARY=English_United States.utf8 LC_NUMERIC=C                          
	[5] LC_TIME=English_United States.utf8    
	
	attached base packages:
	[1] stats     graphics  grDevices utils     datasets  methods   base     
	
	other attached packages:
	 [1] ggpubr_0.4.0       lsmeans_2.30-0     magick_2.7.3       tidyr_1.2.1        cowplot_1.1.1      knitr_1.41         psych_2.2.9        multcompView_0.1-8 multcomp_1.4-20   
	[10] TH.data_1.1-1      MASS_7.3-58.1      survival_3.4-0     mvtnorm_1.1-3      emmeans_1.8.2      plyr_1.8.8         ggplot2_3.4.0     
	
	loaded via a namespace (and not attached):
	 [1] zoo_1.8-11         tidyselect_1.2.0   xfun_0.35          purrr_0.3.5        splines_4.2.2      lattice_0.20-45    carData_3.0-5      colorspace_2.0-3   vctrs_0.5.1       
	[10] generics_0.1.3     utf8_1.2.2         rlang_1.0.6        pillar_1.8.1       glue_1.6.2         withr_2.5.0        DBI_1.1.3          lifecycle_1.0.3    ggsignif_0.6.4    
	[19] munsell_0.5.0      gtable_0.3.1       codetools_0.2-18   coda_0.19-4        labeling_0.4.2     parallel_4.2.2     fansi_1.0.3        broom_1.0.1        Rcpp_1.0.9        
	[28] xtable_1.8-4       backports_1.4.1    scales_1.2.1       abind_1.4-5        farver_2.1.1       mnormt_2.1.1       rstatix_0.7.0      dplyr_1.0.10       grid_4.2.2        
	[37] cli_3.4.1          tools_4.2.2        sandwich_3.0-2     magrittr_2.0.3     tibble_3.1.8       car_3.1-1          pkgconfig_2.0.3    ellipsis_0.3.2     Matrix_1.5-1      
	[46] estimability_1.4.1 assertthat_0.2.1   rstudioapi_0.14    R6_2.5.1           nlme_3.1-160       compiler_4.2.2```
