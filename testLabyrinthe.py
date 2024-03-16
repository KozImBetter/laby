from Labyrinthe import Maze
"""
laby = Maze(5, 5)
#laby.empty()
for i in range(0, 5):
    for j in range(0, 4):
        laby.remove_wall((i, j), (i, j+1))

for i in range(0, 4):
    for j in range(0, 5):
        laby.remove_wall((i, j), (i + 1, j))

print(laby)
#laby.fill()
laby.add_wall((0, 0), (0, 1))
laby.add_wall((0, 1), (1, 1))
print(laby)

print(laby.get_contiguous_cells((0,1)))
print(laby.get_reachable_cells((0,1)))

laby = Maze(5, 5)
laby.empty()
laby.fill()
laby.remove_wall((0, 0), (0, 1))
laby.empty()
laby.add_wall((0, 0), (0, 1))
laby.add_wall((0, 1), (1, 1))
print(laby)
print(laby.get_walls())
print(laby.get_contiguous_cells((0,1)))
print(laby.get_reachable_cells((0,1)))

laby = Maze.gen_btree(4, 4)
print(laby)
"""

laby = Maze.gen_sidewinder(4, 4)
print(laby)