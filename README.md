# Assignment 1 – Image search
The portfolio for __Visual Analytics S22__ consists of 4 projects (3 class assignments and 1 self-assigned project). This is the __first assignment__ in the portfolio.


## 1. Contribution
The initial assignment was made partly in collaboration with others from the course, but the final code was made by me(???)
Code in utils folde is Ross'...


## 2. Assignment description
This assignment was assigned by Ross, and the assignment description was as follows:

For this assignment, you will write a small Python program to compare image histograms quantitively using Open-CV and the other image processing tools you've already encountered. Your script should do the following:

- Take a user-defined image from the folder
- Calculate the "distance" between the colour histogram of that image and all of the others.
- Find which 3 image are most "similar" to the target image.
- Save an image which shows the target image, the three most similar, and the calculated distance score.
- Save a CSV which has one column for the filename and three columns showing the filenames of the closest images in descending order.

## 3. Methods
Initially, when the assignment was handed in as part of the course, I used calculations of distances between colour histograms to calculate similary between images. However, as we have later been introduced to more advanced methods of calculating similarity, I have provided both my original code (with some corrections) and a script using a pretrained model to do nearest neighbours learning on the data. I would recommend using the second code.

## 4. Usage
Before running the script, run the following in the Terminal:
```
pip install --upgrade pip
pip install opencv-python scikit-learn tensorflow tensorboard tensorflow-hub pydot scikeras[tensorflow-cpu]
sudo apt-get update
sudo apt-get -y install graphviz
```


## 5. Discussion of results



