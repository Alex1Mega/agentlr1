import random
from collections import deque

# Агент
class Rover:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.energy = 100
        self.explored = set()
        self.trajectory = [(0, 0)]
        self.goal = 30

    # Перцептор
    def perceive(self, env):
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        result = {}

        for name, (dx, dy) in directions.items():
            x = self.x + dx
            y = self.y + dy

            if not env.inside(x, y):
                result[name] = "boundary"
            elif env.grid[x][y] == "#":
                result[name] = "obstacle"
            else:
                result[name] = "free"

        return result

    # Активатор
    def move(self, direction, env):
        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        dx, dy = moves[direction]
        x = self.x + dx
        y = self.y + dy

        if not env.inside(x, y) or env.grid[x][y] == "#":
            return False

        self.x = x
        self.y = y
        self.energy -= 1

        self.explored.add((x, y))
        self.trajectory.append((x, y))

        return True

    # Вибір напрямку
    def choose_direction(self, env):
        perception = self.perceive(env)

        directions = []

        for direction in perception:
            if perception[direction] == "free":
                directions.append(direction)

        if not directions:
            return None

        # Спочатку вибираємо невідвідану клітину
        for direction in directions:
            moves = {
                "up": (-1, 0),
                "down": (1, 0),
                "left": (0, -1),
                "right": (0, 1)
            }

            dx, dy = moves[direction]
            position = (self.x + dx, self.y + dy)

            if position not in self.explored:
                return direction

        return random.choice(directions)

    # Перевірка завершення
    def need_return(self):
        return len(self.explored) >= self.goal or self.energy <= 20

    # Повернення на базу
    def return_base(self, env):
        start = (self.x, self.y)
        target = (0, 0)

        queue = deque([start])
        previous = {start: None}

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current = queue.popleft()

            if current == target:
                break

            for dx, dy in moves:
                x = current[0] + dx
                y = current[1] + dy

                if env.inside(x, y) and env.grid[x][y] != "#":
                    if (x, y) not in previous:
                        previous[(x, y)] = current
                        queue.append((x, y))

        if target not in previous:
            return

        path = []
        current = target

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        for x, y in path[1:]:
            self.x = x
            self.y = y
            self.energy -= 1
            self.trajectory.append((x, y))


# Середовище
class Environment:
    def __init__(self, rows=10, cols=15):
        self.rows = rows
        self.cols = cols
        self.grid = [["." for _ in range(cols)] for _ in range(rows)]

        for _ in range(25):
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)

            if (x, y) != (0, 0):
                self.grid[x][y] = "#"

    def inside(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def show(self, rover):
        for i in range(self.rows):
            row = ""

            for j in range(self.cols):
                if (i, j) == (rover.x, rover.y):
                    row += "R "
                elif (i, j) == (0, 0):
                    row += "B "
                elif (i, j) in rover.explored:
                    row += "* "
                else:
                    row += self.grid[i][j] + " "

            print(row)


# Запуск
def main():
    random.seed(10)

    env = Environment()
    rover = Rover()

    rover.explored.add((0, 0))

    print("Початкова карта:")
    env.show(rover)

    # Дослідження
    while not rover.need_return():

        direction = rover.choose_direction(env)

        if direction is None:
            break

        rover.move(direction, env)

    print("\nРовер завершив дослідження.")
    print("Повернення на базу...")

    # Повернення
    rover.return_base(env)

    print("\nФінальна карта:")
    env.show(rover)

    print("\nРезультати:")
    print("Досліджено клітин:", len(rover.explored))
    print("Енергія:", rover.energy)
    print("Кінцева позиція:", (rover.x, rover.y))

    print("\nТраєкторія:")
    print(rover.trajectory)


if __name__ == "__main__":
    main()

