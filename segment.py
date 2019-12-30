import argparse
import sys
import os
import numpy as np
import wget

from tqdm import tqdm
from keras.models import load_model
from segmentation_models.losses import bce_jaccard_loss
from PIL import Image

parser = argparse.ArgumentParser(description="Arguments for SE Seg.")
parser.add_argument("--input_dir",
		help="Path to directory containing images to segment."
	)
parser.add_argument("--output_dir",
		help="Path to directory to write outputs."
	)
parser.add_argument("--output_type",
		default="se",
		help="Comma separated string to indicate output type. 'se' to show se/mask nse, 'nse' to show nse/mask se, 'mask' to output binary mask. Defaults to 'se'."
	)
parser.add_argument("--mask_color",
		default="127,127,127",
		help="Comma separated string for RGB value of mask. Defaults to 127,127,127. Supply 'random' for mask to be random colors."
	)
parser.add_argument("--threshold",
		default=None,
		type=int,
		help="Value between 0 and 100 for thresholding binary mask. Defaults to 50. Supply 'False' for no threshold - value will indicate opacity."
	)

args = parser.parse_args()
output_type = set(args.output_type.split(","))
random = False
if args.mask_color == "random":
	random = True
else:
	rgb = [int(x) for x in args.mask_color.split(",")]

if not os.path.exists('checkpoint'):
	os.makedirs('checkpoint')

if not os.path.exists('checkpoint/checkpoint.hdf5'):
	choice = input("Model checkpoint not found. Download it? [Y/n]")
	if choice == "Y":
		wget.download("https://www.qalaymiqan.com/se_seg/checkpoint.hdf5", 'checkpoint/checkpoint.hdf5')
	else:
		sys.exit()

path = "checkpoint/checkpoint.hdf5"
print("Loading model...")
model = load_model(path)
print("Model loaded.")

print("Segmenting images...")
for path in tqdm(os.listdir(args.input_dir)):
	path = os.path.join(args.input_dir, path)
	name = path.split("/")[-1]
	name = name.split(".")[0]

	img = Image.open(path).convert('RGB')
	arr = np.array(img.resize((256, 256)))
	pred = model.predict(np.array([arr]))[0].reshape((256, 256))
	pred *= 255
	pred = pred.astype("uint8")
	pred = Image.fromarray(pred)
	pred = pred.resize((img.width, img.height), Image.BICUBIC)

	if args.threshold:
		t = 255 * (args.threshold/100)
		pred = np.array(pred)
		pred[pred > t] = 255
		pred[pred <= t] = 0
		pred = Image.fromarray(pred)

	if "mask" in output_type:
		pred.save(os.path.join(args.output_dir, "{}_pred.png".format(name)))

	if "nse" in output_type:
		nse = img.copy()
		if random:
			add = np.random.randint(0, 256, size=(img.height, img.width, 3))
		else:
			add = np.dstack((
					np.full((img.height, img.width), rgb[0]),
					np.full((img.height, img.width), rgb[1]),
					np.full((img.height, img.width), rgb[2])
				))
		add = Image.fromarray(add.astype("uint8"))
		nse.paste(add, (0, 0), pred)
		nse.save(os.path.join(args.output_dir, "{}_nse.png".format(name)))

	if "se" in output_type:
		pred = np.array(pred).astype("int16")
		pred -= 255
		pred = -pred
		pred = pred.astype("uint8")
		pred = Image.fromarray(pred)

		se = img.copy()
		if random:
			add = np.random.randint(0, 256, size=(img.height, img.width, 3))
		else:
			add = np.dstack((
					np.full((img.height, img.width), rgb[0]),
					np.full((img.height, img.width), rgb[1]),
					np.full((img.height, img.width), rgb[2])
				))
		add = Image.fromarray(add.astype("uint8"))
		se.paste(add, (0, 0), pred)
		se.save(os.path.join(args.output_dir, "{}_se.png".format(name)))

print("Done. Segmentation results written to {}.".format(args.output_dir))