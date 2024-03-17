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

laby = Maze.gen_sidewinder(4, 4)
print(laby)

laby = Maze.gen_fusion(15,15)
print(laby)

laby = Maze.gen_exploration(15,15)
print(laby)

laby = Maze.gen_wilson(12, 12)
print(laby)

laby = Maze(4,4)
laby.empty()
print(laby.overlay({
    (0, 0):'c',
    (0, 1):'o',
    (1, 1):'u',
    (2, 1):'c',
    (2, 2):'o',
    (3, 2):'u',
    (3, 3):'!'}))

laby = Maze.gen_fusion(15, 15)
solution = laby.solve_dfs((0, 0), (14, 14))
str_solution = {c:'*' for c in solution}
str_solution[( 0,  0)] = 'D'
str_solution[(14, 14)] = 'A'
print(laby.overlay(str_solution))
"""
laby = Maze.gen_exploration(15, 15)
solution = laby.solve_bfs((0, 0), (14, 14))
str_solution = {c:'*' for c in solution}
str_solution[( 0,  0)] = 'D'
str_solution[(14, 14)] = 'A'
print(laby.overlay(str_solution))