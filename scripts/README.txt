This document includes all python code that is used to preprocess raw video datasets, retina-based augmentation, and data balance.
After preprocessing, the dataset can be used to YOLOv5 model training and test and implement different training strategies we designed.

video extractor --- convert video dataset to frames, convert annotation to YOLOv5 format, split training set, test set, and validation set.

Retienx augmentation --- includes différent retiens-bases auxgmentation methods, autoMSRCR is we chosen.

Data balance --- calculate instance number of each class, select classes that need increase. Implement file, shear, rotation, and HSV adjust to augment minority class, at the same time process label boxes and annotation.

Notice: to test scripts need to rewrite the dataset path.