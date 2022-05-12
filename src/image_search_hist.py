"""
Image seach using colour histogram comparisons
"""

# Import the relevant packages
 # base tools
import os, sys
import glob
from operator import itemgetter
import re
import pandas as pd
 # data analysis
import numpy as np
 # image processing
import cv2
 # plotting
import matplotlib.pyplot as plt

def hist_comp():
    # Take a user-defined image from the folder
    # get directory path
    directory_path = os.path.join("in", "flowers")
    
    # filenames
    filenames = os.listdir(directory_path)
    
    # joined paths to images in the directory
    joined_paths = []
    # image names in the directory
    image_names = []
    
    for file in filenames:
        # if that file is not a jpg, do nothing
        if not file.endswith(".jpg"):
            pass
        else:
            input_path = os.path.join(directory_path, file)
            joined_paths.append(input_path)
            image_names.append(file)
    
    # sort filenames and filepaths
    joined_names = sorted(image_names)
    joined_paths = sorted(joined_paths)
    
    # user-defined image – I chose the image at index 231, i.e. image_0232.jpg
    image_path = joined_paths[231]
    image_name = joined_names[231]
    
    # read the image
    image = cv2.imread(image_path)
    
    # print image name and path
    print(f"Image name: {image_name},\nImage path: {image_path}")
    
    # Calculate distance scores between the target image and all other images
    # save the histogram for target image
    hist1 = cv2.calcHist([image],
                         [0,1,2], # use all channels
                         None, # no masks
                         [8,8,8], # each channel uses a bin of 8
                         [0,256, 0,256, 0,256]) # ranges of values possible for each channel
    hist1_norm = cv2.normalize(hist1, hist1, # normalising hist1 relative to itself
                               0,255, # ranges (note! different indexing)
                               cv2.NORM_MINMAX)
    
    # list of paths to all other images than the target
    comp_list = []
    for path in joined_paths:
        if not path == image_path:
            comp_list.append(path)
    
    # comparison list with the filepaths, file names, and distance scores for all images
    hist_comparison = []
    
    for path in comp_list:
        comp_path = path
        # get name
        comp_name = re.sub('.*\/', '', comp_path)
        # read image
        comp_img = cv2.imread(comp_path)
        # create histogram
        hist2 = cv2.calcHist([comp_img],
                             [0,1,2],
                             None,
                             [8,8,8],
                             [0,256, 0,256, 0,256])
        # normalise histogram
        hist2_norm = cv2.normalize(hist2, hist2,
                                   0,255, 
                                   cv2.NORM_MINMAX)
        # compare to hist1 (target image)
        hist_comp = cv2.compareHist(hist2_norm, hist1_norm, cv2.HISTCMP_CHISQR)
        # append filepaths, file names, and distance scores to list
        hist_comparison.append((comp_path, comp_name, hist_comp))
    
    # sort the comparison list by distance score
    compar_sorted = sorted(hist_comparison, key=itemgetter(2))
    
    # list of the three most similar images
    top_3 = compar_sorted[0:3]
    
    # list of filenames for the target and top three images
    top_names = [image_name]
    for tup in top_3:
        top_names.append((tup[1]))
    
    # convert colours from BGR (OpenCV) to RGB (matplotlib)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im1 = top_3[0][0]
    im1r = cv2.cvtColor(cv2.imread(im1), cv2.COLOR_BGR2RGB)
    im2 = top_3[1][0]
    im2r = cv2.cvtColor(cv2.imread(im2), cv2.COLOR_BGR2RGB)
    im3 = top_3[2][0]
    im3r = cv2.cvtColor(cv2.imread(im3), cv2.COLOR_BGR2RGB)
    
    # make a list of the images
    picturelist = [imageRGB, im1r, im2r, im3r]
    
    # make a list of the distance scores
    hist_list = [0]
    for tup in top_3:
        hist_list.append(tup[2])
    
    # round distance scores for plotting
    hist_list_round = [round(num, 3) for num in hist_list]
    
    # Create and save a plot of the four images
    # figure with 2 rows and 2 columns
    fig, ax = plt.subplots(2,2)
    # target image in row 1, colum 1
    ax[0,0].imshow(picturelist[0])
    # add title with name and distance score
    ax[0,0].title.set_text(f"Target image, {top_names[0]}")
    # most similar image in row 1, column 2
    ax[0,1].imshow(picturelist[1])
    # add title with name and distance score
    ax[0,1].title.set_text(f"Dist. for {top_names[1]}: {hist_list_round[1]}")
    # second most similar image in row 2, column 1
    ax[1,0].imshow(picturelist[2])
    # add title with name and distance score
    ax[1,0].title.set_text(f"Dist. for {top_names[2]}: {hist_list_round[2]}")
    # third most similar image in row 2, column 2
    ax[1,1].imshow(picturelist[3])
    # add title with name and distance score
    ax[1,1].title.set_text(f"Dist. for {top_names[3]}: {hist_list_round[3]}")
    # add distance between subplots
    fig.tight_layout(pad=0.5)
    # save figure
    fig.savefig("out/hist_similar_images.png")
    
    # Save results as CSV
    # create a dataframe with the image names and transpose to make each image a column
    output_df = pd.DataFrame(top_names, ["Target image", "Most similar", "Second most similar", "Third most similar"])
    output_transp = output_df.transpose()
    
    # save the CSV
    output_transp.to_csv(os.path.join("out", "hist_similar_images.csv"), encoding = "utf-8")

def main():
    hist_comp()
   
    
if __name__=="__main__":
    main()