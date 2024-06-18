import todos

#todos.addProject(0, 'Saluti nel mondo', [1, 2, 3])
items = todos.fetchProjectItems(1, 0)
for item in items:
    print(item)