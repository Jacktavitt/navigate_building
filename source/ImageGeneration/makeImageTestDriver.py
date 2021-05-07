import DataGenerator
import CustomImage
import cv2
import numpy as np
import os
import argparse


def run(directory):
    IMAGE_CLASS = CustomImage.GeneratedImage
    IMG_GENR = DataGenerator.ImageGenerator(IMAGE_CLASS, size=(512,512,3),randSeed=42,plaqueSize=75,resolution=10)

    four_points = np.float32([(0,10),(510,10),(20,501),(499,510)])
    dest_points = np.float32([[0,0],[512,0],[0,512],[512,512]])
    skew_matrix = cv2.getPerspectiveTransform(four_points, dest_points)

    for n in range(16):
        image = IMG_GENR.make_true_image(num_randos=n).image
        spun_cw = cv2.warpAffine(
            image,
            cv2.getRotationMatrix2D((image.shape[0]/2, image.shape[1]/2), -10, 1),
            image.shape[:2],
            borderMode=cv2.BORDER_REPLICATE
        )
        spun_ac = cv2.warpAffine(
            image,
            cv2.getRotationMatrix2D((image.shape[0]/2, image.shape[1]/2), 10, 1),
            image.shape[:2],
            borderMode=cv2.BORDER_REPLICATE
        )
        skew = cv2.warpPerspective(image, skew_matrix, image.shape[:2])
        b_spun_cw = cv2.blur(spun_cw, (13,1))
        b_spun_ac = cv2.blur(spun_ac, (13,1))
        blur = cv2.blur(image, (13,1))
        b_skew = cv2.blur(skew, (13,1))

        for im, name in (
            (image, 'image'), (spun_ac, 'spun_ac'), (spun_cw, 'spun_cw'), (skew, 'skew'), (b_skew, 'b_skew'), (b_spun_ac, 'b_spun_ac'), (b_spun_cw, 'b_spun_cw'), (blur, 'blur')
        ):
            cv2.imwrite(os.path.join(directory, f"{n}_{name}.png"), im)

# good = IMAGE_CLASS.add_many(signList)
# good.show()
# cv2.imwrite('big_good_one_2.png', good.image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", required=True, help="where to save images")
    args = parser.parse_args()
    run(args.directory)
