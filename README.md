# SE Segmentation

A segmentation model that takes an input image and assigns each pixel a label indicating if that pixel belongs, or does not belong, to a sexually explicit depiction.

<p align="center">
	<img src="https://raw.githubusercontent.com/vqmalic/se_seg/master/docs/img01.jpg">
	<br>
	<em>From left to right: blurred original test images, ground truth, SE segmentation output. Original images are blurred just to keep documentation SFW, output column shows output when unblurred images are provided as input.</em>
</p>

This is, admittedly, a rather strange task. Online pornography represents a great wealth of visual material that may be used in machine learning, but the vast majority of existing efforts focus simply on designating a given image as a whole as sexually explicit (or "NSFW") for the purposes of filtering out undesirable images in applications. This model instead identifies the areas of an image that are sexually explicit, and those which are not. 

We developed this model as part of a larger effort to train unsupervised, semantically rich representations of pornographic images. Our first attempts at doing this were hampered by the varied and diverse "background sets" of pornographic imagery. Trained representations were just as likely to encode the color of the carpet or the grass and trees in the background as the explicit "human action" we were interested in. We therefore became interested in finding ways to isolate the sexually explicit parts of an image and came up with this. Although the task is niche, we're putting the model out there in case someone else might find it useful.

**SE Seg is not a skin segmenter.** Skin segmenters only find skin, so the resulting masks will not capture clothing, hair, eyes, or teeth. Once a person is identified as sexually explicit in an image, SE Seg will segment out the entire person, clothes, hair, and all, to the best of its ability given the available training data. 

## Usage

### Requirements

* tensorflow-gpu==1.12.0
* segmentation-models==0.2.0
* Keras==2.2.4
* numpy==1.16.1
* Pillow==5.4.1
* tqdm==4.31.1
* wget==3.2

I'm immensely greatful to Github user [qubvel](https://github.com/qubvel) for their library [Segmentation Models](https://github.com/qubvel/segmentation_models). It's a fantastic tool and SE Seg is basically an out of the box usage of it with a specific dataset. 

### Command Line Example

```
python segment.py \
--input_dir inputs \
--output_dir outputs \
--output_type se,nse \
--mask_color 255,0,0 \
--threshold 50
```

This segments all images in the directory `inputs`. Results are written to the directory `outputs`. Each image will result in two outputs: one showing the sexually explicit parts of the images while masking the non-sexually explicit parts (se) and one with the mask reversed (nse). The mask color is red (255,0,0). The model's predictions are binarized using a threshold of 50: any pixel assigned an SE confidence of 50 or higher will be labeled SE, any pixel with a score lower than 50 will be labeled NSE. 

* `--output_type` - a comma delimited string with the options `se`, `nse`, and `mask`. `se` reveals sexually explicit areas and masks non-sexually explicit areas, `nse` reveals non-sexually explicit areas and masks sexually explicit areas, and `mask` produces a black-and-white image where black indicates NSE and white indicates SE. Defaults to `se`.
* `--mask_color` - A comma delimited string of RGB values. if `se` or `nse` is an argument to `--output_type`, this determines the color of the areas that are masked. Defaults to `127,127,127`.  
* `--threshold` - An integer between 0 and 100. The model assigns scores to each pixel representing its confidence that the pixel is sexually explicit. `--threshold` determines the cutoff above which a pixel will be labeled SE. This argument can be omitted, in which case output types of `se` and `nse` will use the model output as an opacity mask and the `mask` output type will generate a grayscale image ranging from black (a score of 0) to white (a score of 100). 

<p align="center">
	<img src="https://raw.githubusercontent.com/vqmalic/se_seg/master/docs/img02.jpg">
	<br>
	<em>Original image, "se" output, "nse" output, "mask" output at mask_color=127,127,127 and threshold=50.</em>
</p>

<p align="center">
	<img src="https://raw.githubusercontent.com/vqmalic/se_seg/master/docs/img03.png">
	<br>
	<em>"se" output with mask_color=127,127,127 at no threshold (opacity map), threshold=25, threshold=50, and threshold=75.</em>
</p>

## Model

SE Seg uses a UNET architecture with a 152-layer SE-ResNet pretrained on ImageNet as the backbone. During training, the encoder weights are frozen and only the decoder weights are updated. 

## Data

The training data consists of 806 manually annotated images. Model performance is validated on 202 manually annotated test images. The objective function is a combination of the Intersection over Union and the binary cross entropy when comparing the model output to the ground truth. 

## The Concept of Sexual Explicitness

Sexual explicitness is an unavoidably subjective quality. The training data for this model was annotated with the following guidelines:

* Any depicted human designated as a *sexually explicit entity* (SEE) will have the entirety of their bodies, including clothing and paraphernelia, labeled as *sexually explicit*. 
* The following conditions designate a depicted human as SEE:
	1. If there is more than one person and they are engaging in any sexual activity (including but not limited coitus, oral sex, or the stimulation of genitals), all participants are considered SEEs.
	2. If a person is exposing any of their genitals or sexualized body parts (including penises, vaginas, breasts, or buttocks), they are considered an SEE. 
	3. If a person is attired or posed in a way that may reasonably construed as intimate or intending to arouse sexual interest, that person is considered an SEE. 
* If any object such as a dildo is being used for sexual stimulation, that object is considered an SEE. 

These guidelines serve mainly to filter out false positives or media irrelevant to the current research interests. A summarizing intuition would be to ask whether or not the actions, poses, or attire depicted would be acceptable in a public setting. For example, an image depicting a person in a bathing suit will be removed from the data due to point 3, as although some bathing suits expose much, wearing such attire is acceptable in the context of swimming. In contrast, an image depicting a person in lingerie or a "sexy outfit" will be included, even if such an outfit exposes as much as (or less than) a bathing suit, as conventionally such outfits are expected to be limited to intimate settings. Point 3 also includes images of individuals who may not be exposing genitals but are "posed" in suggestive ways, as in an image where an individual is highlighting their sexual parts to the camera in a way that would not be socially acceptable in a public setting. The condition of an SEE being "human" filters out animated pornography from the resulting dataset. Although sexually explicit animations do constitute a significant part of pornography, they were deemed beyond the scope of our current research goals.

## Limitations

The training data for SE Seg was created manually and is relatively small compared to other deep learning training sets. As a result, the model relies heavily on pretraining on ImageNet for general visual concepts. Our qualitative evaluation of SE Seg on test images indicates that it can, for the most part, capture attire worn by people engaging in sexual activity, but it often misses colors, styles, or apparel that are rare and therefore missing from the training data. 

Imagery for the training data was randomly sampled from a wide variety of pornographic sources, so genres in the training data roughly reflect proportions in pornographic materials found online. Because of this, the data is likely highly biased in terms of representations of gender, body type, ethnicity, or apparel that is characteristic of less common genres. LGBTQ material is present in the training data, but in much smaller amounts compared to material aimed at heterosexual audiences. Biases and imbalances present in the training data may be reflected in SE Seg's outputs. 

