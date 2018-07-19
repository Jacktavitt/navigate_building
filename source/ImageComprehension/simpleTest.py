import random
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed","-s", help="seed for randomness", type = int, required =True)
    parser.add_argument("--images","-i" ,help="how many images to make",type = int, required =True)
    parser.add_argument("--noise","-n" ,help="how much extra crap to put in the background",type = int, required =True)
    args=parser.parse_args()
    print("Did it work? Seed: {}, Images: {}, Noise: {}".format(args.seed, args.images, args.noise))