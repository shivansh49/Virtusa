from django.shortcuts import render
from django.http import HttpResponse
import xgboost
from .models import product,products,product3
import pandas as pd
import numpy as np
import pickle
import dill
def front(request):
    return render(request,'front.html')
def index(request):
    return render(request,'index.html')
def data(request):
    li = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    return render(request,'datavisuals.html',{'s':li})
def sentiment(request):
    return render(request,'sentiment.html')
def tweets(request):
    if request.method=="POST":
        a = str(request.POST["data"])
        b = int(request.POST["no"])
    import sys, tweepy, csv, re
    from textblob import TextBlob
    import matplotlib.pyplot as plt

    consumerKey = 'zPcVn71EB4TcDTMzvXbMc9V97'
    consumerSecret = 'yt2N4JT08IRcOvhT5YLlvOTqX7kK0CxkpBhS1ZwS7Wi8VBS3YQ'
    accessToken = 'AAAAAAAAAAAAAAAAAAAAAPLYHwEAAAAAYy8m%2B81vtMqOCUw9k9bT8Af2wVA%3DzTSogzA6Tjjgcz8dquXBGhrFMMcAgMubHZOP96VliVKJuXSMWK'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    api = tweepy.API(auth)
    tweets = tweepy.Cursor(api.search, q=a, lang="en").items(b)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    def percent(part, whole):
        return 100 * float(part) / float(whole)

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        if (analysis.sentiment.polarity == 0):
            neutral = neutral + 1
        elif (analysis.sentiment.polarity < 0.00):
            negative = negative + 1
        elif (analysis.sentiment.polarity > 0.00):
            positive = positive + 1

    positive = percent(positive, b)
    negative = percent(negative, b)
    neutral = percent(neutral, b)
    positive = format(positive, '.2f')
    negative = format(negative, '.2f')
    neutral = format(neutral, '.2f')

    output = "How people are reacting on " + a + " by analyzing " + str(b) + " tweets."

    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'gold', 'red']
    return render(request,'sentimentvisuals.html',{'sizes':sizes,'colors':colors,'output':output})
def train(request):
    if request.method=="POST":
        a = int(request.POST['age'])
        b = float(request.POST['bmi'])
        a = float((80-a)/60)
        b = float((30-b)/14)
        print(a,b)
        p = predict2(a, 0.292587, b, 1.300904, 0.328952, 1.409188, 1.055792, 1.654873, 2.889897, 2.768141, 1.327529,
                    2.528115, 2.040771, 2.804618, 2.830720, 2.967599, 0.049275, 0.190465, 0.097775, 0.054496)
        return render(request, 'train.html', {'data': p})
def predict2(Ins_Age, Wt, BMI, Employment_Info_3, Product_Info_4,
            InsuredInfo_6, Insurance_History_2, Medical_History_4,
            Medical_History_6,
            Medical_History_13, Medical_History_16, Medical_History_23,
            Medical_History_30,
            Medical_History_33, Medical_History_39, Medical_History_40,
            Medical_Keyword_3,
            Medical_Keyword_15, Medical_Keyword_23, Medical_Keyword_48):
    with open('templates/xgb_model.pkl', 'rb') as xgb_model:
        model = pickle.load(xgb_model)
    data = [Product_Info_4, Ins_Age, Wt, BMI, Employment_Info_3, InsuredInfo_6, Insurance_History_2,
            Medical_History_4,
                    Medical_History_6, Medical_History_13, Medical_History_16, Medical_History_23, Medical_History_30,
                    Medical_History_33, Medical_History_39, Medical_History_40, Medical_Keyword_3, Medical_Keyword_15,
                    Medical_Keyword_23, Medical_Keyword_48]
    df = pd.DataFrame(columns=['Product_Info_4', 'Ins_Age', 'Wt', 'BMI', 'Employment_Info_3', 'InsuredInfo_6',
                                   'Insurance_History_2', 'Medical_History_4', 'Medical_History_6',
                                   'Medical_History_13',
                                   'Medical_History_16', 'Medical_History_23', 'Medical_History_30',
                                   'Medical_History_33',
                                   'Medical_History_39', 'Medical_History_40', 'Medical_Keyword_3',
                                   'Medical_Keyword_15',
                                   'Medical_Keyword_23', 'Medical_Keyword_48'])
    df.loc[0] = data
    return model.predict(df)[0]

def clustering(request):
    if request.method=="POST":
        age_cat = request.POST["dropdown"]
        region = request.POST["dropdown1"]
        no_of_children = int(request.POST["children"])
        gender = request.POST["radio"]
        weight_condition = request.POST["rad"]
        smoker = request.POST["ra"]
    test_l = [0] * 16
    test_l[0] = no_of_children
    if age_cat == "Elder":
        test_l[1], test_l[2], test_l[3] = 1, 0, 0
    if age_cat == "Senior Adult":
        test_l[1], test_l[2], test_l[3] = 0, 1, 0
    if age_cat == "Young Adult":
        test_l[1], test_l[2], test_l[3] = 0, 0, 1
    if weight_condition == "Normal Weight":
        test_l[4], test_l[5], test_l[6], test_l[7] = 1, 0, 0, 0
    if weight_condition == "Obese":
        test_l[4], test_l[5], test_l[6], test_l[7] = 0, 1, 0, 0
    if weight_condition == "Overweight":
        test_l[4], test_l[5], test_l[6], test_l[7] = 0, 0, 1, 0
    if weight_condition == "Underweight":
        test_l[4], test_l[5], test_l[6], test_l[7] = 0, 0, 0, 1
    if gender == "male":
        test_l[8], test_l[9] = 0, 1
    if gender == "female":
        test_l[8], test_l[9] = 1, 0
    if smoker == "no":
        test_l[10], test_l[11] = 0, 1
    if smoker == "yes":
        test_l[10], test_l[11] = 1, 0
    if region == "northeast":
        test_l[12], test_l[13], test_l[14], test_l[15] = 1, 0, 0, 0
    if region == "northwest":
        test_l[12], test_l[13], test_l[14], test_l[15] = 0, 1, 0, 0
    if region == "southeast":
        test_l[12], test_l[13], test_l[14], test_l[15] = 0, 0, 1, 0
    if region == "southwest":
        test_l[12], test_l[13], test_l[14], test_l[15] = 0, 0, 0, 1
    with open('templates/kmeans_clustering.pkl', 'rb') as xgb_model:
        model = pickle.load(xgb_model)
    cluster = model.predict([test_l])[0]
    if cluster==0:
        dests = product.objects.all()
        return render(request, 'product.html',{'cluster':cluster,'dests':dests})
    elif cluster==1:
        dests = products.objects.all()
        return render(request, 'product.html',{'cluster':cluster,'dests':dests})
    else:
        dests = product3.objects.all()
        return render(request, 'product.html',{'cluster':cluster,'dests':dests})
