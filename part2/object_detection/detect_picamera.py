# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TF Lite to detect objects with the Raspberry Pi camera."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import signal
import sys

from annotation import Annotator

import numpy as np
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

STOP_SIGN_ID = 12
DETECT_THRESHOLD = 0.4


def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels


def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor

# Returns if stop sign detected, also the boxes[i] object
def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  for i in range(count):
    if scores[i] >= threshold and classes[i] == STOP_SIGN_ID:
        return True
  return False


def annotate_objects(annotator, results, labels):
  """Draws the bounding box and label for each object in the results."""
  for obj in results:
    # Convert the bounding box figures from relative coordinates
    # to absolute coordinates based on the original resolution
    ymin, xmin, ymax, xmax = obj['bounding_box']
    xmin = int(xmin * CAMERA_WIDTH)
    xmax = int(xmax * CAMERA_WIDTH)
    ymin = int(ymin * CAMERA_HEIGHT)
    ymax = int(ymax * CAMERA_HEIGHT)

    # Overlay the box, label, and score on the camera preview
    annotator.bounding_box([xmin, ymin, xmax, ymax])
    annotator.text([xmin, ymin],
                   '%s\n%.2f' % (labels[obj['class_id']], obj['score']))

camera = None;
     

## Catches SIGINT and remove camera window
def signal_handler(sig, frame):
    print("interrupted, removing camera instance")
    global camera
    camera.stop_preview()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Vision:
  def __init__(self):
    self.interpreter = Interpreter("detect.tflite")
    self.interpreter.allocate_tensors()
    _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']

    self.camera = picamera.PiCamera(
      resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30)
    self.camera.start_preview()
    self.camera.preview.alpha = 127
  
  def scanStopSign(self):
    stream = io.BytesIO()
    for _ in self.camera.capture_continuous(
        stream, format='jpeg', use_video_port=True):
      stream.seek(0)
      image = Image.open(stream).convert('RGB').resize(
          (self.input_width, self.input_height), Image.ANTIALIAS)
      stopSignDetected = detect_objects(self.interpreter, image, DETECT_THRESHOLD)
      if stopSignDetected:
            print("detected stopsign")
            return True

      stream.seek(0)
      stream.truncate()

    def __del__():
      self.camera.stop_preview()
      self.camera.close()

if __name__ == '__main__':
  vis = Vision()
  vis.scanStopSign()
  del vis