# SE Segmentation

A segmentation model that takes an input image and assigns each pixel a label indicating if that pixel belongs, or does not belong, to a sexually explicit depiction.

<p align="center">
	<img src="https://raw.githubusercontent.com/vqmalic/se_seg/master/docs/img01.jpg">
	<em>From left to right: blurred original images, ground truth, SE segmentation output. Original images are blurred just to keep documentation SFW, output represents output when unblurred images are provided as input.</em>
</p>

This is, admittedly, a rather strange task. Online pornography represents a great wealth of visual material that may be used in machine learning, but the vast majority of existing efforts focus simply on designating a given image as a whole as sexually explicit (or "NSFW") for the purposes of filtering out undesriable images in applications. This model instead identifies the areas of an image that are sexually explicit, and those which are not. 

We developed this model as part of a larger effort to train unsupervised, semantically rich representations of pornographic images. Our first attempts at doing this were hampered by the varied and diverse "background sets" of pornographic imagery. Trained representations were just as likely to encode the color of the carpet or the grass and trees in the background as the explicit "human action" we were interested in. We therefore became interested in finding ways to isolate the sexually explicit parts of an image and came up with this. Although the task is niche, we're putting the model out there in case someone else might find it useful.


# The Concept of Sexual Explicitness

Sexual explicitness is an unavoidably subjective quality. The training data for this model was annotated with the following guidelines:

* Any depicted human designated as a *sexually explicit entity* (SEE) will have the entirety of their bodies, including clothing and paraphernelia, labeled as *sexually explicit*. 
* The following conditions designate a depicted human as SEE:
	1. If there is more than one person and they are engaging in any sexual activity (including but not limited coitus, oral sex, or the stimulation of genitals), all participants are considered SEEs.
	2. If a person is exposing any of their genitals or sexualized body parts (including penises, vaginas, breasts, or buttocks), they are considered an SEE. 
	3. If a person is attired or posed in a way that may reasonably construed as intimate or intending to arouse sexual interest, that person is considered an SEE. 
* If any object such as a dildo is being used for sexual stimulation, that object is considered an SEE. 

These guidelines serve mainly to filter out false positives or media irrelevant to the current research interests. A summarizing intuition would be to ask whether or not the actions, poses, or attire depicted would be acceptable in a public setting. For example, an image depicting a person in a bathing suit will be removed from the data due to point 3, as although some bathing suits expose much, wearing such attire is acceptable in the context of swimming. In contrast, an image depicting a person in lingerie or a "sexy outfit" will be included, even if such an outfit exposes as much as (or less than) a bathing suit, as conventionally such outfits are expected to be limited to intimate settings. Point 3 also includes images of individuals who may not be exposing genitals but are "posed" in suggestive ways, as in an image where an individual is highlighting their sexual parts to the camera in a way that would not be socially acceptable in a public setting. The condition of an SEE being "human" filters out animated pornography from the resulting dataset. Although sexually explicit animations do constitute a significant part of pornography, they were deemed beyond the scope of our current research goals.



