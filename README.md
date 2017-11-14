# FakeBach
A Markov-chain based music generator.

_Created by Bhairav Chidambaram_

## Can a computer be creative?

Inspired by _MathGen_ and various poetry generators, I started this project to understand if the same Markov chains behind these generative systems could power music composition. Music presents a unique challenge, as there is a very sharp dividing line between "noise" and "music" -- the human ear is very picky about what it calls music.

## Usage

Modules Required
- [music21](http://web.mit.edu/music21/)

Once music21 is installed, simply clone this repo and run attempt4.py. A ~1 min sample will automatically be generated and played as a midi file.

## Technical Details

The project uses a custom Markov-chain implementation (see markov.py). The Markov matrix records transition probabilities from the current state to the next item in the sequence. My implementation allows us to define the current state as any number of the previous items in the sequence -- this is referred to as the order of the Markov-chain.

In order to generate the music itself, both the notes and rhythm are first encoded as sequences and "learned" by a Markov matrix. Then the matrix is used to generate music by sampling random numbers to determine which transition to take from the current state, i.e. which note or rhythm sequence to append.

## Etc.

First I recommend listening to Generated/sample4.midi. For more details about this project's progression, see the full writeup "FakeBach writeup.pdf".
