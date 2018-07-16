# Dude, where's my class?
This is my sketch for a direction-generating system for ADA-compliant buildings. The goal is to provide a simple interface to people with visual impairment that will provide them with human-comprehensible, non-metric (i.e., 'Go straight 4 doors, then turn left' instead of 'Proceed 23 meters, then turn west') directions to help them get to where they need to be.

It is (generally) divided into 3 parts:

SLAM : using Monocular SLAM, build a map of a space, with each image corresponding to a pose.

ImageComprehension : Go through images and pick out those that contain an ADA-compliant room marker,
including stairs and exits. Generate an adjecency list, with each node as a spot in the hallway. Can have rooms, other nodes, or exits/stairwells to North, South, East, or West.

DirectionHandling : Given a start room and a finish room, generate human-comprehensible, non-metric directions. At first, the nearest beginning room must be provided.


## Getting Started

Not ready for a release yet :^(
 

## Authors

* **John Feilmeier** - *Coding and research* - [Jacktavitt](https://github.com/jacktavitt)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


* **Billie Thompson** - *README template* - [PurpleBooth](https://github.com/PurpleBooth)
*[Excellent template](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/8254b53ab8dcb18afc64287aaddd9e5b6059f880/README-Template.md)

  
