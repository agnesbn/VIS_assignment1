"""
Image seach using colour histogram comparisons
"""

""" Import the relevant packages """
 # base tools
import os, sys
from operator import itemgetter
import re
 # argument parser
import argparse
 # data analysis
import numpy as np
import pandas as pd
 # image processing
import cv2
 # plotting
import matplotlib.pyplot as plt

""" Basic functions """
# create and save a plot of the four similar images
def image_plot(picturelist, top_names, hist_list_round, index):
    # figure with 2 rows and 2 columns
    fig, ax = plt.subplots(2,2)
    # target image in row 1, colum 1
    ax[0,0].imshow(picturelist[0])
    # add title with name and distance score
    ax[0,0].title.set_text(f"{top_names[0]}\nTarget image")
    # most similar image in row 1, column 2
    ax[0,1].imshow(picturelist[1])
    # add title with name and distance score
    ax[0,1].title.set_text(f"{top_names[1]}\nDist. score: {hist_list_round[0]}")
    # second most similar image in row 2, column 1
    ax[1,0].imshow(picturelist[2])
    # add title with name and distance score
    ax[1,0].title.set_text(f"{top_names[2]}\nDist. score: {hist_list_round[1]}")
    # third most similar image in row 2, column 2
    ax[1,1].imshow(picturelist[3])
    # add title with name and distance score
    ax[1,1].title.set_text(f"{top_names[3]}\nDist. score: {hist_list_round[2]}")
    # add distance between subplots
    fig.tight_layout(pad=0.5)
    # save figure
    fig.savefig(os.path.join("out", "all", f"img{(index+1):04}_similar_images.png"))
    # close current figure to save memory
    plt.close()

# save all results as csv
def save_csv(top_names):
    # create a dataframe with the image names
    output_df = pd.DataFrame(top_names,columns=["Target image", "Most similar", "Second most similar", "Third most similar"])
    # save the CSV
    output_df.to_csv(os.path.join("out", "all", f"img_similar_images.csv"), 
                     encoding = "utf-8",
                     index=False)

""" Histogram comparison function """
def hist_comp():
    # get directory path
    directory_path = os.path.join("in", "jpg")
    # filenames
    filenames = os.listdir(directory_path)
    # joined paths to images in the directory
    joined_paths = []
    # image names in the directory
    image_names = [] 
    # for files in list of filenames
    for file in filenames:
        # if a file does not end with .jpg, do nothing
        if not file.endswith(".jpg"):
            pass
        # otherwise
        else:
            # append path for each file to one list
            input_path = os.path.join(directory_path, file)
            joined_paths.append(input_path)
            # and append filename to another list
            image_names.append(file)
    # sort filenames and filepaths
    joined_names = sorted(image_names)
    joined_paths = sorted(joined_paths)
    # get list of histograms
    print("[INFO] Creating histograms ...")
    hist_list = []
    for i in range(0,1360):
        image_path = joined_paths[i]
        image_name = joined_names[i]
        image = cv2.imread(image_path)
        # saving the histogram and normalised histogram for the target image
        hist = cv2.calcHist([image],
                            [0,1,2],
                            None,
                            [8,8,8],
                            [0,256, 0,256, 0,256])
        hist_norm = cv2.normalize(hist, hist,
                              0,255,
                                  cv2.NORM_MINMAX)
        hist_list.append((image_path, image_name, hist_norm))
    # compare all histograms
    print("[INFO] Comparing histograms ...")
    comparisons = []
    for h in hist_list:
        path1 = h[0]
        name1 = h[1]
        hist1 = h[2]
        v = []
        for c in hist_list:
            if c[1] != name1:
                path2 = c[0]
                name2 = c[1]
                hist2 = c[2]
                hist_comp = cv2.compareHist(hist2, hist1, cv2.HISTCMP_CHISQR)
                v.append((path2, name2, hist_comp))
        # sort the list by distance score
        compar_sorted = sorted(v, key=itemgetter(2))
        # get only top three most similar images
        comparisons.append(((path1, name1),compar_sorted[0:3]))
    # get relevant values    
    il = []
    hl = []
    tn = []
    for t in comparisons:
        # load images
        im1 = cv2.cvtColor(cv2.imread(t[0][0]), cv2.COLOR_BGR2RGB)
        im2 = cv2.cvtColor(cv2.imread(t[1][0][0]), cv2.COLOR_BGR2RGB)
        im3 = cv2.cvtColor(cv2.imread(t[1][1][0]), cv2.COLOR_BGR2RGB)
        im4 = cv2.cvtColor(cv2.imread(t[1][2][0]), cv2.COLOR_BGR2RGB)
        # make list of loaded images
        image_list = [im1, im2, im3, im4]
        il.append((image_list))
        # get list of rounded distance scores
        hist_list = [0, t[1][0][2], t[1][1][2], t[1][2][2]]    
        hist_list_round = [round(num, 3) for num in hist_list]
        hl.append((hist_list_round))
        # make list of names of top images
        top_names = [t[0][1], t[1][0][1], t[1][1][1], t[1][2][1]]
        tn.append((top_names))
    return (il, hl, tn)
    
""" Main function """    
def main():
    (il, hl, tn) = hist_comp()
    print("[INFO] Saving histogram plots ...")
    i = 0
    for im, h, t in zip(il, hl, tn):
        image_plot(im, t, h, i)
        print(f"[INFO] {i+1}/1360 complete")
        i += 1
    save_csv(tn)
    return print("[INFO] COMPLETE!")

    
if __name__=="__main__":
    main()
