# GoodsGameOfLife
Display:
- There will be a grid containing cells which may be empty, or occupied by an organism. Different colors may be used to represent 
different species.
- If they can, organisms can move inside of the grid in a manner determined by their genetics.


Components of an organism:
- genotype will ultimately determine what the organisms eats, how much it needs to eat, its movement and sleeping patterns, and how
effective it is at obtaining food, whether or not it is a predator.
- genotype includes information for categorizing organisms (like how a human is a primate, mammal, etc.), or the category can be
determined by examining an individual's genotype and checking to see if it meets certain conditions.
- dietary portion of the genotype includes whether the organism is a carnivore, omnivore or herbivore, and how many calories the organism
needs to consume.
- genotype will include the weight of the organism
- certain features will be determined by a group of alleles rather than a single allele.
- the movement patterns of an organism can be determined by alleles that themselves determine something analogous to metabolism,
short and long distance speed, and stamina
- as the generations go on, categorization may change based on how different alleles have changed


User interface:
- the user can also determine how far ahead they want to jump with each iteration - one year,  one generation,
one hundred generations, etc.


Multilayered Evolution?


-- Evolve rules for the genotype, types of organisms, possibly environment?


Binary String Index Mappings:


0-11: size (weight)
12-14: number of cells that the organism can move by in one instance
-- 15-25: sleeping pattern, with a lower value indicating more frequent sleep, but in shorter bursts
15-16: herbivore, omnivore, or carnivore
17-19: vision, with a larger value indicating a greater field of view
20-24: this is basically intelligence. There will be a tree, the nature of which will depend on this subset of the string.
25-30: memory capacity




Decision Tree:


* The principles of crossover and mutation will be applied to an organism's tree, so the tree itself, not just the genotype, will be influenced by the parents' makeup.
* Perform a depth-first search, returning to the root when a terminal is reached.
* Part of the tree will be generated with the genotype, but the rest of it will be generated as the organism "grows up." This means that there is a possibility for an organism's "brain" to develop based on it's childhood experiences.
* Functions
   * CheckHunger
      * The base metabolic rate needs to be determined, and activity burns additional energy.
      * Sub-functions can consider additional details, like specific levels of hunger.
   * AttackPrey
      * The first approach is to just go straight ahead
      * A more advanced approach might be to observe the prey and make decisions based on the prey's attributes, such as how fast it is, stamina, etc.
      * Another advanced approach is to try to corner prey
   * Learning from experience (Reflection)
      * Trying to hunt a prey once, observing the behavior of the prey (like how fast it is, perhaps sleeping patterns, etc.) And remembering that experience
      * If prey was very fast, the organism might reason that it must not have great stamina, so it could attack in a different way next time
   * Possible recombination techniques
      * Possible technique #1
         * Establish the basic tree that all organism have in common
         * Initialize miss count to 0
         * Randomly select one of the nodes
         * Check if a potential child exists in the parents’ trees
         * If one potential child exists, insert that as a child and clear miss count
         * If multiple potential children exist, randomly select one to insert and clear miss count
         * Otherwise, increment the miss count
         * End if miss count exceeds limit, otherwise repeat
Additional notes:
* The “--” at the beginning means that I decided against including it
