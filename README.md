# Assignment 1 – Image search
The portfolio for __Visual Analytics S22__ consists of 4 projects (3 class assignments and 1 self-assigned project). This is the __first assignment__ in the portfolio.


## 1. Contribution
The initial assignment was made partly in collaboration with others from the course, but the final code is my own. I made several adjustments to the code since I first handed it in during the course.

## 2. Assignment description
When we were first assigned the assignment, the assignment description was as follows:

For this assignment, you will write a small Python program to compare image histograms quantitively using Open-CV and the other image processing tools you've already encountered. Your script should do the following:

- Take a user-defined image from the folder
- Calculate the "distance" between the colour histogram of that image and all of the others.
- Find which 3 image are most "similar" to the target image.
- Save an image which shows the target image, the three most similar, and the calculated distance score.
- Save a CSV which has one column for the filename and three columns showing the filenames of the closest images in descending order.

## 3. Methods


## 4. Usage
Put the flower-data into the `in` folder.

Before running the script, run the following in the Terminal:
```
pip install --upgrade pip
pip install opencv-python scikit-learn tensorflow tensorboard tensorflow-hub pydot scikeras[tensorflow-cpu]
sudo apt-get update
sudo apt-get -y install graphviz
```
Then, from the `VIS_assignment1` directory, run:
```
python src/image_search_hist.py --image_index {INDEX}
```
`{INDEX}` represents a user-defined argument. Here, you can write any number from 0–1359 and it will index your target image.

## 5. Discussion of results
When I ran the code, I put in `231` as my target image index. The results can be seen in the `out` folder. The output files are:
- `hist_similar_images_indx231.csv`: A CSV with a row for the name of the target image and then three rows for the top three most similar images to the target image.
- `hist_similar_images_indx231.png`: An image of the target image and its three most similar images with their respective distance scores.

As you can tell if you look at the output, the method was relatively sucessful in my case. The flowers that were identified as the most similar to my target image do indeed seem to be of the same species as my target flower. I did find, however, that it did not work as well with all images, as it did for `image_0232`. If you put in `600`, for example, it seems as though all flowers on the pictures are of different species. It higlights the weakness of this type of method. As it only pick up on colous distributions, it fails to take into consideration other relevant factors like shape.

Thus, for this type of task a more advanced method would be beneficiary, e.g. using a pretrained model, like VGG16, to do feature extraction for all images and then using a nearest neighbour algorithm to find the images with less "distance", like what we did in Session 11.
