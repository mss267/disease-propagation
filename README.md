# disease-propagation

A program to simulate the propagation of disease. Takes inputs of:

* Population immunisation probability.
* Vaccine efficacy.
* Disease mortality rate.

then simulates the spread of the disease in a population of 25x25 individuals represented by a grid. The simulation is run 50 times to output the mean fraction and standard deviation of infection rates within:

* The vaccinated population.
* The unvaccinated population.
* The total population.

Also output are histograms representing each of the above, and the 50 lattices produced by the simulation.
