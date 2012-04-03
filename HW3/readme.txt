Unfortunately for me the image processing was really taxing my computer.  My computer ended up freezing right when it was almost done.  I'll let it run over night and see if I can get some results though!

I did this object-orientedly.  Create an image classifier object to do basically everything

a=ImageClassifier()
#read the data in from files
a.readData('50_categories', 'tr_smaller.csv', 'te_smaller_kpod.csv', frac=3)

#or the following does it from scratch
a.importData(directory)

#train the estimator
a.trainSearch()

#test it
a.testEstimator()