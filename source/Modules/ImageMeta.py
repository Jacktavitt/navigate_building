class ImageDetectionMetadata():
    def __init__(self):
        self.contour_area = 0.0
        self.reference_area = 0.0
        self.image = None
        self.thresheld_image = None
        self.text = []
        self.pose_information = None
        self.source_image_location = ''
        self.plaque_image_location = ''
        self.other = {}

    def __repr__(self):
        # other stuff = ' ... '.join([str(k) + ': ' + str(v) for k,v in self.other.items()])
        return f"""
        countour area: {self.contour_area}
        reference area: {self.reference_area}
        plaque image location: {self.plaque_image_location}
        possible text: {', '.join([x for x in self.text])}
        pose information: {self.pose_information}
        source image location: {self.source_image_location}
        other stuff: {' ... '.join([str(k) + ': ' + str(v) for k,v in self.other.items()])}
        """
