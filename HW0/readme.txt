Richard Kwant

To run a simulation of a population of bears, run hw1.py

Then, create an environment
>>>env = Env(simLength = 150)

run the simulation
>>>env.run()
the number of bears total, alive, dead, and alive at year 100 are returned

To run multiple simulations, the functions runSimulation and runGenderSimulation can be used.  Genealogy plotting can be accomplished after running and environment via randBearGenealogy, which shows all older ancesters of a random bear.
>>>env.randBearGenealogy()

the genealogy of all living bears can also be shown with showGraph
>>>env.showGraph()

1) 100 simulations were run.  The average number of bears alive after 100 years was 313, and the average number of bears alive after 150 years was 6277.  

2) For each value of P(male) from 0 to 0.5 with increments of 0.05, 100 simulations were run.  The lowest value of P(male) that produced a population with a living bear after 150 years was P(male) = 0.1.  

3) See the included image.  