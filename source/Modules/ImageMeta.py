import numpy
import re

with open('/home/johnny/Documents/navigate_building/source/assets/images_with_plaques.txt') as f:
    LIST_OF_POSITIVES = f.read().split('\n')


class ImageDetectionMetadata():
    headers = ['label', 'parsed_text', 'found_contour_area', 'ref_contour_area', 'source_image_location', 'image_has_plaque', 'plaque_found', 'text_matched', 'text_missed', 'text_misread']

    def __init__(self):
        self.contour_area = numpy.nan
        self.reference_area = numpy.nan
        self.image = None
        self.thresheld_image = None
        self.text = []
        self.pose_information = None
        self.source_image_location = ''
        self.plaque_image_location = ''
        self.label = None
        self.correct_text = False
        self.other = {}

    def __repr__(self):
        return f"""
        countour area: {self.contour_area}
        reference area: {self.reference_area}
        plaque image location: {self.plaque_image_location}
        possible text: {', '.join([x for x in self.text])}
        pose information: {self.pose_information}
        source image location: {self.source_image_location}
        other stuff: {' ... '.join([str(k) + ': ' + str(v) for k,v in self.other.items()])}
        """

    def to_list(self):
        """
        creates explicitly-ordered list of elements in the object
        """
        has_plaque = True if self.source_image_location in LIST_OF_POSITIVES else False
        plaque_found = True if self.contour_area > 0 else False
        self.label = [x.replace('-', '') for x in re.findall(r"-[0-9,a-z]*-", self.source_image_location)]
        matched = list(set(self.text) & set(self.label))
        missed = list(set(self.label) - set(self.text))
        misread = list(set(self.text) - set(self.label))
        meta_list = [
            self.label,
            self.text,
            self.contour_area,
            self.reference_area,
            self.source_image_location,
            has_plaque,
            plaque_found,
            matched,
            missed,
            misread
        ]
        return meta_list
