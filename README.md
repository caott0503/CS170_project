# project-fa19
CS 170 Fall 2019 Project

### How to run?
```bash
python solver.py --all inputs
```
or
```bash
python3 solver.py --all inputs
```

# FINAL REPORT

441 words right now

The report should be a summary of how your algorithm works, what other methods you tried along the way, and what computing resources you used (e.g. AWS, instructional machines, etc.). Your final report should be at least 400 words, and no more than 1000 words long. You will also submit the code for your solver, along with a README containing precise instructions on how to run it. 


Essentially, we implemented the strategies outlined in the initial reports, including a naive baseline that simply drops all students off at “Soda” - starting car location - which works surprisingly well on some inputs as we visualized some of them selectively. Then, we decided to go a little deeper, which involves a more advanced baseline that solves a TSP based on all homes. This is done by viewing only a subgraph of the original graph consisting of only the homes and starting location, and then use the all pairs Dijkstra’s result to fake an edge between any pair of homes even if there isn’t one. We then continue working on this path by randomly selecting a subset of homes to run our fakeTSP on. The random selection is done simply through random.random and setting a seed initially. The TSP solver we use is developed by Google.

Note: due to the large portion of grades allotted to solving our own inputs, we put extra hyper parameters and tried different seeds to find the best outputs we can find on our own inputs, and then insert a special check to return our own “optimal” solution directly if the input matches with our input’s pattern.

Afterwards, we implemented k-clustering for homes and then picking the center of each cluster to run this fakeTSP. The code follows from the idea in textbook, and after running it for a while, we discovered that this is more or less similar to randomly selecting a subset of all homes and fine-tuning the selectivity.

Being stuck on a local minimum, we decided to use some method to further improve our results. The one thing we found was simulated annealing. It was difficult to define the transition probabilities, so we decided to just randomly select pairs and see if it improves anything. This doesn’t help too much, so we implemented general TSP from an online paper. We always compare results with previous ones and change them only if we’ve got an improvement.

We used Google Cloud Platform for about an hour or so, and discovered that it didn’t help with our efficiency too much. The main problem was that our Python kept giving a segmentation fault, so we wrote a script to basically continue from where it left off from the original inputs. Then, we could finish the inputs rather quickly. Lastly, we visualize inputs that always gives us a segfault, visualize it online, and basically do a special manual solve on each of them - there’s about 10-20 of them, mostly consisting of fully-connected graphs or star-like graphs, and both of which are very easy to figure out the optimum. These are also specially detected/conditioned to directly return the optimum we’ve found. In cases where it’s just fully-connected or star-like graphs, we basically ran the optimum solver for these two specific types of graphs on all inputs and compare with previous solutions to see which one’s better.
