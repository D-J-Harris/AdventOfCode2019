# AdventOfCode2019
Solutions for the Advent of Code 2019 edition (https://adventofcode.com/2019).
Solutions are my own, learning points from observing code on the challenge subreddit are outlined below. 

## Learning Points
* Day 3 - Finding an approach that uses less sparse memory storage would be better here, in particular ordering was not important so sets would have been good, alternatively the use of dictionaries to store coordinate points.

* Day 4 - Scanning solution worked well, also a fan of str -> list techniques found online. This would make ordering or 'contains 2 of this digit' conditions much more simple.

* Day 7 - Use of multiple independent 'IntCode' systems meant I was forced to go down the class route, and refactoring took some time. However this has been useful practice and comparing against online methods has bee good for learning, especially thinking about schedulers/queues for future problems.
