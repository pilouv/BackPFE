# -*- coding: utf-8 -*-
"""PFExpert_clean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wfimqt7iLdWCJNEbAymTWSA05P_9hzwT
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip3 install face_recognition
# !pip install import-ipynb

import face_recognition
import numpy as np
import pandas as pd
import scipy
import pywt
from functools import reduce
import copy
import os
import cv2 as cv
from numpy.fft import fft2, ifft2
# from matplotlib import pyplot as plt
# from matplotlib.pyplot import imshow
from tqdm import tqdm
from glob import glob
from multiprocessing import cpu_count, Pool
from PIL import Image

# from google.colab import drive
# drive.mount('/content/drive')

# import sys
# sys.path.insert(0,'/content/drive/Shareddrives/PFEurovision/collabs')

from api import functionsPRNU as prnu
#import examplePRNU as exprnu

"""## Import dataset"""

path = "videos/atkdltyyen.mp4"

def cut_video_in_frames(path) :
  cap = cv.VideoCapture(path)
  print(cap)
  frames = []
  print('TATA:::: ',cap.isOpened())
  #cap.open(path)
  while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frames.append(frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
  cap.release()

  print('The number of frames saved: ', len(frames))
  return (frames)

def allocate_groups(LIST_FRAME,PADDING,NB_GROUP,NB_IMAGES,frames):
  frames_list = LIST_FRAME.copy()
  groups = []
  while len(frames_list) != 0 :
      random_groups = np.random.choice(frames_list,NB_IMAGES,replace=False)
      groups.append(list(random_groups))
      for i in (random_groups):
          frames_list.remove(i)
  # fig, axes = plt.subplots(NB_GROUP, NB_IMAGES, figsize=(15, 15))
  # axes = np.array(axes)
  # axes = axes.reshape(-1)
  compteur = 0

  frames_array = [[] for i in range(len(groups))]

  compteur_group = 0

  for group in groups:
      for i in group:
          frame = frames[i]
          face_locations = face_recognition.face_locations(frame)
          if len(face_locations) == 0:
              print(f'Could not find face in frame {i}')
              continue
          top, right, bottom, left = face_locations[0]
          frame_face = frame[top-PADDING:bottom+PADDING, left-PADDING:right+PADDING]
          frame_face = cv.resize(frame_face, dsize=(265, 265)) # A voir si coh??rent ou non !!!!! -> Sinon probl??me avec k = np.stack(k,0)
          # image = cv.cvtColor(frame_face, cv.COLOR_BGR2RGB)
          # axes[compteur].imshow(image)
          # axes[compteur].xaxis.set_visible(False)
          # axes[compteur].yaxis.set_visible(False)
          # axes[compteur].set_title(f'Frame {i}')
          compteur += 1
          frames_array[compteur_group].append(frame_face)
      compteur_group += 1
  # plt.grid(False)
  # plt.show()

  return (frames_array)

def main(path):
    print('-----------------------------------------------------------------------------------------------------------------------')
    print(path)

    LIST_FRAME = list(np.arange(start=0,stop=300,step=10))
    PADDING = 0
    NB_GROUP = 6
    NB_IMAGES = 5

    frames = cut_video_in_frames(path)

    frames_array = allocate_groups(LIST_FRAME,PADDING,NB_GROUP,NB_IMAGES,frames)

    k = []
    for device in frames_array:
        k += [prnu.extract_multiple_aligned(device, processes=cpu_count())]
    k = np.stack(k, 0)

    #print(k)
    #print(np.shape(k))

    # all_correlation_matrix = prnu.aligned_cc(k[0],k[1])['ncc']
    all_correlation_matrix = []
    for group in k :
        #tmp = []
        for prnuBis in k :
            if ((prnuBis != group).any()) :
                #tmp.append(prnu.aligned_cc(group,prnuBis)['ncc'])
                # tmp.append(np.corrcoef(group.ravel(),prnuBis.ravel()))
                all_correlation_matrix.append(prnu.aligned_cc(group,prnuBis)['ncc'])
    
    MM = np.mean(all_correlation_matrix)
    #MM = np.mean(np.array(all_correlation_matrix), axis=0)

    # print("Moyennes par groupe :",listeMoyenneMatrices)
    print("Moyenne g??n??rale :",MM)

    return MM

"""
# matrice1 = [[1,2,3],[1,2,3]]
# matrice2 = [[4,5,6],[4,5,6]]
# matrice3 = [[7,8,9],[7,8,9]]
# Matrice = [matrice1,matrice2,matrice3]

#listeMoyennesMatrices = lambda liste, x: list(map(lambda n:np.mean(np.array([n]),axis=0), liste))
 
#listeMoyennesMatrices = [np.mean(i) for i in zip(Matrice)]
listeMoyennesMatrices = np.mean(np.array(Matrice), axis=0)

#print(listeMoyennesMatrices)
print(listeMoyennesMatrices)

# CONTENT_PATH = '/content/drive/Shareddrives/PFEurovision/DeepFakeDetection/DeepfakeTIMIT/'
CONTENT_PATH = '/content/drive/Shareddrives/PFEurovision/DeepFakeDetection/test_prnu_original_fake/'

# list_originals = [CONTENT_PATH + 'originals_couple/' + x for x in os.listdir(CONTENT_PATH+'originals_couple/') if x.endswith('.mp4')]
# list_fakes = [CONTENT_PATH + 'fakes_couple/' + x for x in os.listdir(CONTENT_PATH+'fakes_couple/') if x.endswith('.mp4')]

originals = [CONTENT_PATH + 'originals_couple/1_atkdltyyen.mp4']
fakes = [CONTENT_PATH + 'fakes_couple/1_cksanfsjhc.mp4']

# list_fakes = [CONTENT_PATH+'/fakes/' + x for x in os.listdir(CONTENT_PATH+'/fakes/') if x.endswith('.mp4')]

# list_originals.sort()
# list_fakes.sort()

print("Originals :", originals)
print("Fakes :", fakes)

list_moyennes_originals = [main(video) for video in originals]
list_moyennes_fakes = [main(video) for video in fakes]

print('Moyennes originals :',list_moyennes_originals)
print('Moyennes fakes :',list_moyennes_fakes)

assert np.shape(list_moyennes_originals) == np.shape(list_moyennes_fakes)
print(np.shape(list_moyennes_originals))

w_test = scipy.stats.ttest_ind(list_moyennes_originals, list_moyennes_fakes, equal_var=False)

print(w_test)

list_moyennes_originals_ordered = list_moyennes_originals.copy()
list_moyennes_fakes_ordered = list_moyennes_fakes.copy()

# list_moyennes_originals_ordered.sort()
# list_moyennes_fakes_ordered.sort()

# list_moyennes_ordered = np.concatenate((list_moyennes_fakes_ordered,list_moyennes_originals_ordered))

barWidth = 0.5
r1 = range(len(list_moyennes_originals_ordered))
r2 = range(len(list_moyennes_fakes_ordered))
r2 = list(map(lambda x: x +barWidth, r2))
print(r2)
# r2 = [x + barWidth for x in r1]

# plt.bar(r1, list_moyennes_originals_ordered, width = barWidth, color = ['blue' for i in list_moyennes_originals_ordered], linewidth = 2)

# plt.figure(figsize=(15,7))
# plt.bar(r1, list_moyennes_originals_ordered, width = barWidth, color = ['darkblue' for i in list_moyennes_originals_ordered], linewidth = 2)
# plt.bar(r2, list_moyennes_fakes_ordered, width = barWidth, color = ['darkorange' for i in list_moyennes_fakes_ordered], linewidth = 4)
# plt.xticks([r + barWidth / 2 for r in range(len(list_moyennes_fakes_ordered))])
# plt.show()

"""