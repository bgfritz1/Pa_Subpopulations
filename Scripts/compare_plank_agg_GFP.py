import os
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pdb 



def main():
    raw_image_dir = "./Data/Plank_Agg_AraGFP/"
    mask_dir = raw_image_dir + "imageJ_masks/"

    #Import the raw images and the masks as dictionaries 
    
    raw_images = read_in_images(raw_image_dir + "raw_data_tif/")
    mask_images = read_in_images(mask_dir)

    #Binarize imageJ masks and create dictionaries containing the masks for plank and aggregates

    agg_mask = invert_mask(mask_images, inverse=True)
    plank_mask = invert_mask(mask_images, inverse=False)

    ##MASK SANITY CHECK----------------------------------
    ##just going to plot a few
    ## If you want more, just add more rows
    # fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(10,10))
    # for axs, key in zip(ax, agg_mask.keys() ):
        
    #     axs[0].imshow(agg_mask[key])
    #     axs[1].imshow(plank_mask[key])

    # plt.tight_layout()
    # plt.show()
    ##----------------------------------------------------

    raw_plankmasked = {}
    raw_aggmasked = {}
           
    for image in raw_images:
        if image.startswith("agg"):
            raw_plankmasked[image] = apply_mask(raw_images[image], plank_mask[image])
            raw_aggmasked[image] = apply_mask(raw_images[image], agg_mask[image])

        else: 
            pass

    
    test_difference(plank_dict=raw_plankmasked,agg_dict=raw_aggmasked, threshold = 3000, 
                    replicate_names = ['agg_repA', 'agg_repB', 'agg_repC'])



    ##MASK SANITY CHECK #2----------------------------------
    ##just going to plot a few
    ## If you want more, just add more rows

    mask_example_fig(raw_images, agg_mask, raw_plankmasked, raw_aggmasked, 
                     threshold = 3000, rows = 1) #needs to be >1 row
    
    ##----------------------------------------------------
    plot_histogram(raw_plankmasked, 100, "plankmasked")
    plot_histogram(raw_aggmasked, 100, "aggmasked")

def invert_mask(mask_dictionary, inverse=False):
    """ 
    The masks created in ImageJ are such that they contain two possible values - 255 and 1.
    We want to binarize these to allow for multiplying the matrices against the original images.

    Then, we also want an inverse of the binarized mask. 
            
    """
    binary_dict = {}
    
    for mask in mask_dictionary: 
        image = mask_dictionary[mask]
        
        if inverse:
            binary = (image != 255)
        else:    
            binary = (image == 255)

        binary_dict[mask] = binary
        
    return(binary_dict)


def plot_mask_figure(image_dir):
    """
    This function makes a pyplot figure containing a grid of 
    all of the figures contained in the input directory

    The directory can ONLY contain image .tif files.  
    """
    images = os.listdir(image_dir)
    
    fig, ax = plt.subplots(nrows = 6, ncols = 5, figsize = (15,10))

    i = 0 
    for row in ax: 
        for subplot in row:
            image = io.imread(image_dir + images[i])
            subplot.imshow(image)
            i+=1

    plt.tight_layout()
    plt.show()


def mask_example_fig(raw_images,agg_mask,raw_plankmasked,raw_aggmasked, 
                     threshold, rows):
    plt.clf()

    if rows==1: #Takes the example from first image 
        key="agg_repC_01.tif"
        fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(15,5))
        ax[0].imshow(np.max(raw_images[key], axis=0) * 10 , cmap = 'Greys') #original
        ax[0].set_title('Original', fontdict={'fontsize':14})
        ax[1].imshow(agg_mask[key], cmap = 'binary') # plank mask 
        ax[1].set_title('Mask', fontdict={'fontsize':14})
        ax[2].imshow(np.max(raw_plankmasked[key], axis=0) > threshold, cmap = 'Greys') # plank masked
        ax[2].set_title('Masked: Planktonic', fontdict={'fontsize':14})
        ax[3].imshow(np.max(raw_aggmasked[key], axis=0) > threshold, cmap = 'Greys') # agg masked
        ax[3].set_title('Masked: Aggregate', fontdict={'fontsize':14})

    else: 
        fig, ax = plt.subplots(nrows=rows, ncols=4, figsize=(15,5*rows))
        threshold = 3000

        for axs, key in zip(ax, agg_mask.keys()):
            axs[0].imshow(np.max(raw_images[key], axis=0) * 10 , cmap = 'Greys') #original
            axs[0].set_title('Original', fontdict={'fontsize':14})
            axs[1].imshow(agg_mask[key], cmap = 'binary') # plank mask 
            axs[1].set_title('Mask', fontdict={'fontsize':14})
            axs[2].imshow(np.max(raw_plankmasked[key], axis=0) > threshold, cmap = 'Greys') # plank masked
            axs[2].set_title('Masked: Planktonic', fontdict={'fontsize':14})
            axs[3].imshow(np.max(raw_aggmasked[key], axis=0) > threshold, cmap = 'Greys') # agg masked
            axs[3].set_title('Masked: Aggregate', fontdict={'fontsize':14})
    
    fig.tight_layout()
    fig.suptitle('Example of Image Masking', fontsize=12)
    fig.savefig("./figures/plank_agg_example.png")


def read_in_images(image_folder):
    #Create a dictionary where the key is the filename and the value is the image
    images = {}

    for image in os.listdir(image_folder):  
        image_name = image
        image_data = io.imread(image_folder + image)
        images[image_name] = image_data
    return(images)

def apply_mask(raw_image,mask):
    """This will apply a binary mask to each slice in a confocal stack.
    """
    n_slices = raw_image.shape[0]
    masked_image = np.ndarray(shape = raw_image.shape, dtype='uint16')


    for confocal_slice in range(0,n_slices):
        section = raw_image[confocal_slice, :, :]
        masked_slice = np.multiply(section, mask) 
        masked_image[confocal_slice, :, :] = masked_slice
        
        #print("PixelSum Before: " + str(raw_image[confocal_slice, :, :].sum()))
        #print("PixelSum After: " + str(masked_image[confocal_slice, :, :].sum()))
    
    return(masked_image)

def test_difference(agg_dict, plank_dict, replicate_names, threshold):
    """ 
    This function will test the differences between the plank masked and agg-masked images.
    The inputs are the agg_masked raw dictionary and the plank_masked raw dictionary, where the
    keys are the same between the two dictionaries.

    Input: 
        agg_dict - a dictionary containing the agg-masked images
        plank_dict - a dictionary containing the plank-masked images
        replicate_names - a list containing an identifier for the biological replicates in the keys of the
                          agg and plank dictionaries. Such as:
                          replicate_names = ['agg_repA', 'agg_repB', 'agg_repC']                                                

    1. Flatten the images (including all slices) into a 1-dimensional array.
    2. Threshold all of the pixel values by a certain threshold. 
    3. For each image, calculate the mean and median of pixel values
    4. Take the difference of the mean or median value between plank/agg from a single tech replicate
    5. Average across all tech reps for a certain biological replicate. ??
    6. Calculate the diff.
    """
       
    if agg_dict.keys() != plank_dict.keys():
        print("Error: Keys don't match between the dictionaries. Stopping.")
        exit(1)
    
    mean_differences = []

    all_diffs = []
    all_diffs.append(["sample", "difference", "plank_mean", "plank_median","plank_count", "agg_mean", "agg_median", "agg_count"])

    for bio_rep in replicate_names:
        techrep_diff = []

        #look for keys that match the bio replicate
        for key in agg_dict.keys():
            
            if bio_rep in key:
                #Calculate stats for plank/agg of the technical replicate
                plank = desc_stats_image(plank_dict[key], threshold)
                agg = desc_stats_image(agg_dict[key], threshold)

                #calculate the difference in mean pixel intensity 
                #between plank/agg of the same tech.replicate
                
                difference = plank[0]-agg[0]
                techrep_diff.append(difference)              
                
                all_diffs.append([bio_rep, difference,plank[0],plank[1], plank[2], agg[0],agg[1],agg[2]])

        #Calcuklate the mean of the differences for each bio. replicate
        mean_differences.append(np.mean(techrep_diff))

    #Export the difference data
    all_diffs = np.vstack(all_diffs)

    np.savetxt("./Data/Plank_Agg_AraGFP/diffs.csv", all_diffs, delimiter=",", fmt="%s")

    #Now we can run a one-sample t-test to decide if the mean difference is > 0

    print(stats.ttest_1samp(mean_differences, 0))


def desc_stats_image(image, threshold):
    """ This function will calculate some stats about an image.
        The image should be a numpy array (z,x,y).
        It will first flatten the image, threshold the pixels, 
        and then calculate the mean and median pixel values.

        return: 
            (mean, median, count)
    """
    flatten = image.flatten()
    thresholded = flatten[flatten > threshold]
    mean = np.mean(thresholded)
    median = np.median(thresholded)
    count = len(thresholded)
    results = (mean, median, count)
    return(results)

def plot_histogram(dict, threshold, name):
    vals = []
    for key in dict:
            flatten = dict[key].flatten()
            thresholded = flatten[flatten > threshold]
            vals.append(thresholded)
    vals = np.hstack(vals)

    plt.clf()
    plt.hist(vals, bins = 999, range = [0,5000])
   # plt.show()

    plt.savefig(f"./figures/hist_{name}_thresh{threshold}.png")

if __name__ == "__main__":
    main()
