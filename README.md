# pathfinder
No, not the D&D setting. This is my sketch for a direction-generating system for ADA-compliant buildings.

It is (generally) divised into 3 parts:

SLAM : using Monocular SLAM, build a map of a space, with each image (in ROSbag?) corresponding to a pose.

ImageComprehension : Go through (bagged?) images and pick out those that contain an ADA-compliant room marker,
including stars and exits.

DirectionHandling : Given a start room and a finish room, generate human-comprehensible, non-metric directions.
Ideally, these will be optimized for blind and vision-impaired users. 