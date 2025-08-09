# Tournament Seeding

This is a little script to automate the task of seeding fencers in a tournament according to predefined rules.

Seeding usually works like this:
- Define a number of pools you want to seed.
- Define how many fencers should be in each pool.
- Seed the first fencer of the list into the first pool, the second fencer in the second pool and so on.
- When all pools have one fencer, return to the first pool, then to the second and so on. This is called round-robin.
- Continue untill all fencers are maped to a pool.

Usually pools consist of 6 or 7 fencers, but theoretically every number of fencers > 3 can work.

## Requirements
| **ID** | **Name**                       | **Description**                                                                                                                                                                                                                                                                          | **Status** |
| ------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| RQ1    | Read Excel file                | The names of the fencers should be read from an Excel list.                                                                                                                                                                                                                                      | DONE       |
| RQ2    | Variable pool parameters       | Users should be able to set the number and size of the pools.                                                                                                                                                                                                                                    | DONE       |
| RQ2.1  | Validate parameters            | When users enter parameters for the pools, it should be checked (validated) whether all fencers can be assigned to a pool.                                                                                                                                                                       | DONE       |
| RQ3    | Print pools                    | When a user has called the program, the configuration of the pool should be printed on the screen. One name should be listed per line and the pools should be visually separated by slashes to be able to transfer the names to an Excel list.                                                  | TODO       |
| RQ4    | Write pools to a file          | The configuration of the pool should be written to a text file so that the names can be easily transferred.                                                                                                                                                                                      | TODO       |
| RQ5    | Implement Seeding: RoundRobin  | The pools should be seeded like the round robin algorithm (first fencer -> first round, second fencer -> second round, ...).                                                                                                                                                                                      | Done       |
| RQ6    | Implement Seeding: Blockwise   | The pools should be seeded blockwise (first n fencers in round one, second n fencers in round two, ...).                                                                                                                                                                                      | DONE       |
#### Additional information
- The excel file in this directory was created under windows, as creating it under linux did not encode it directly. Please don't delete.
