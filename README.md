# A Non-Invasive Interpretable NAFLD Diagnostic Method Combining TCM Tongue Diagnosis
This is the project of the paper "A Non-Invasive Interpretable NAFLD Diagnostic Method Combining TCM Tongue Diagnosis", this paper can be get:https://arxiv.org/abs/2309.02959.

## Abstract

Non-alcoholic fatty liver disease (NAFLD) is a clinicopathological syndrome characterized by hepatic steatosis resulting from the exclusion of alcohol and other identifiable liver-damaging factors. It has emerged as a leading cause of chronic liver disease worldwide. Currently, the conventional methods for NAFLD detection are expensive and not suitable for users to perform daily diagnostics. To address this issue, this study proposes a non-invasive and interpretable NAFLD diagnostic method. This method involves extracting patients' non-invasive physiological indicators (e.g., Height, Weight, BMI, etc.) and tongue features, which are subsequently integrated using a fusion network referred to as SelectorNet. \textbf{SelectorNet can autonomously learn to process different features, providing attention scores for different attributes from the network for each case.} The experimental results show that the proposed method achieves an accuracy of 77.22\% using only non-invasive data, and it also provides compelling interpretability matrices. This study contributes to the early diagnosis of NAFLD and the intelligent advancement of TCM tongue diagnosis.

## Method

This method requires only the tongue im- age along with readily obtainable physiological indicators to diagnose NAFLD. Apart from the calculable indicators, the required user-provided indicators are only Gender, Age, Height, Weight, Waist Circumference, and Hip Circumference. Initially, the patient’s tongue image is automatically seg- mented. Subsequently, the segmented tongue image undergoes two modes of feature extraction: one involves custom-defined disease relevance feature extraction methods based on prior research experience, while the other employs a ResNet34 pre-trained on ImageNet21k to generate features, thereby preventing the loss of latent disease-related features. Finally, the custom-extracted tongue image features are concatenated with the patient’s physiological indicators as input to Selec- torNet. Meanwhile, the features derived from ResNet34 are fused in the final stage of SelectorNet to yield the ultimate diagnostic result.

<p align="center">
    <img src="https://github.com/cshan-github/SelectorNet/blob/main/0.jpg" width="600" height="300">
  
<p align="center">
    <img src="https://github.com/cshan-github/SelectorNet/blob/main/1.jpg" width="500" height="600">

<p align="center">
    <img src="https://github.com/cshan-github/SelectorNet/blob/main/2.jpg" width="800" height="600">

## Result 

<p align="center">
    <img src="https://github.com/cshan-github/SelectorNet/blob/main/result.jpg" width="800" height="400">

## DataSet

Due to concerns regarding patient privacy, we cannot disclose patient information and tongue images publicly.

## Project Description

**1.Tongue Segmentation**

This paper uses TongueSAM as the tongue segmentation tool, and you can obtain the model and pre-trained model from [here](https://github.com/cshan-github/TongueSAM).

**2.Feature Exaction**

The pre-trained ResNet34 used in the paper is sourced from [here](https://github.com/WZMIAOMIAO/deep-learning-for-image-processing/tree/master/pytorch_classification/Test5_resnet), and their project provides both the model and pre-trained models.

The tongue coat and tongue body segmentation method used in the article is ```./split_body_coat.py```, and an example of the segmentation is shown in the following figure.

<p align="center">
    <img src="https://github.com/cshan-github/SelectorNet/blob/main/3.jpg" width="500" height="200">

For the color feature extraction and morphological feature extraction of tongue images, basic image processing algorithms are employed, treating the images as arrays for calculation. Further elaboration on these methods is not provided here.

For the texture features, Contrast (CON), Angular Second Moment (ASM), Entropy (ENT), and Mean (MEAN), this study employs a feature extraction approach based on the skimage library. We utilized a pre-trained YOLOX model to extract the remaining texture features.
