# Tournament Seeding

This is a little script to automate the task of seeding fencers in a tournament according to predefined rules.

Seeding usually works like this:
- Define a number of pools you want to seed.
- Define how many fencers should be in each pool.
- Seed the first fencer of the list into the first pool, the second fencer in the second pool and so on.
- When all pools have one fencer, return to the first pool, then to the second and so on. This is called round-robin.
- Continue untill all fencers are maped to a pool.

Usually pools consist of 6 or 7 fencers, but theoretically every number of fencers > 3 can work.
