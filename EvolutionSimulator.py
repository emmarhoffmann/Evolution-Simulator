# Author: Emma Hoffmann
# Description: Evolution simulator with creatures that move, find food, reproduce, mutate, and die. Using Python and Pygame.

import pygame
import random
from pygame.locals import *

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # For male creatures
PINK = (255, 105, 180)  # For female creatures
GREEN = (0, 255, 0)  # For food

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Evolution Simulator')
clock = pygame.time.Clock()

REPRODUCTION_DISTANCE_THRESHOLD = 10
ENERGY_THRESHOLD_FOR_DEATH = -300
REPRODUCTION_COOLDOWN = 275

class Creature:
    # Represents a creature in the ecosystem
    def __init__(self, ecosystem, energy, position, gender=None, generation=0):
        self.ecosystem = ecosystem
        self.energy = energy
        self.position = position
        self.gender = gender if gender else random.choice(['male', 'female'])
        self.generation = generation
        self.hunger = 0
        self.speed = 1
        self.reproduction_cooldown = 0

    def update(self):
        # Update creature state: increase hunger, decrease energy over time, and check for death condition
        self.hunger += 1
        self.adjust_speed_based_on_hunger()
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1
        self.energy -= 0.5
        if self.energy <= ENERGY_THRESHOLD_FOR_DEATH:
            self.die()

    def adjust_speed_based_on_hunger(self):
        self.speed = min(5, 1 + self.hunger / 100)

    def seekFood(self, foods):
        # Creatures prioritize finding food: if sufficiently hungry and no reproduction cooldown, they seek partners for reproduction
        if not foods:
            self.moveRandomly()
            return
        
        if self.hunger >= 50 and self.reproduction_cooldown <= 0:
            potential_partners = [c for c in self.ecosystem.creatures if c.gender != self.gender and c.reproduction_cooldown <= 0]
            if potential_partners:
                partner = min(potential_partners, key=lambda c: self.distance_to(c.position))
                if self.distance_to(partner.position) <= REPRODUCTION_DISTANCE_THRESHOLD:
                    self.reproduce(partner)
                    return

        food_target = min(foods, key=lambda x: self.distance_to(x.position))
        self.moveTowards(food_target.position)
        if food_target.isOverlapping(self.position):
            self.eat_food(food_target)
            self.ecosystem.foods.remove(food_target)

    def reproduce(self, other_creature):
        if self.gender == other_creature.gender or self.reproduction_cooldown > 0 or other_creature.reproduction_cooldown > 0:
            return

        self.reproduction_cooldown = REPRODUCTION_COOLDOWN
        other_creature.reproduction_cooldown = REPRODUCTION_COOLDOWN

        offspring_count = random.randint(1, 3)
        for _ in range(offspring_count):
            new_position = ((self.position[0] + other_creature.position[0]) // 2, (self.position[1] + other_creature.position[1]) // 2)
            new_energy = max(10, int((self.energy + other_creature.energy) / 4 * random.uniform(0.9, 1.1)))
            
            # Speed mutation for offspring: 50% chance offspring speed will vary +/- 40% of average of parents' speeds
            base_speed = (self.speed + other_creature.speed) / 2
            mutation_chance = 0.5
            speed_mutation_factor = random.uniform(0.8, 1.2)
            new_speed = base_speed * speed_mutation_factor if random.random() < mutation_chance else base_speed

            new_creature = Creature(self.ecosystem, new_energy, new_position, generation=self.generation + 1)
            new_creature.speed = new_speed
            self.ecosystem.creatures.append(new_creature)

    def moveRandomly(self):
        # Allows the creature to move randomly if no food or partners are nearby, simulating searching behavior
        self.position = (max(0, min(SCREEN_WIDTH, self.position[0] + random.randint(-10, 10))),
                         max(0, min(SCREEN_HEIGHT, self.position[1] + random.randint(-10, 10))))

    def moveTowards(self, target_position):
        dx, dy = target_position[0] - self.position[0], target_position[1] - self.position[1]
        distance = max(1, self.distance_to(target_position))
        step_x, step_y = dx / distance * self.speed, dy / distance * self.speed
        self.position = (max(0, min(SCREEN_WIDTH, self.position[0] + step_x)),
                         max(0, min(SCREEN_HEIGHT, self.position[1] + step_y)))

    def distance_to(self, position):
        return ((self.position[0] - position[0]) ** 2 + (self.position[1] - position[1]) ** 2) ** 0.5

    def eat_food(self, food):
        # Simulates the creature eating food, which increases its energy and reduces hunger
        self.energy += food.energyContent
        self.hunger = max(0, self.hunger - 50)

    def die(self):
        self.ecosystem.creatures.remove(self)

    def draw(self, screen):
        color = BLUE if self.gender == 'male' else PINK 
        pygame.draw.circle(screen, color, self.position, 10)

class Food:
    def __init__(self, energyContent, position):
        self.energyContent = energyContent
        self.position = position

    def isOverlapping(self, position):
        return abs(self.position[0] - position[0]) < 10 and abs(self.position[1] - position[1]) < 10

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (*self.position, 10, 10))

class Ecosystem:
    # Manages the entire ecosystem, including spawning food and handling creature actions each cycle
    def __init__(self):
        self.creatures = [Creature(self, 100, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))) for _ in range(10)]
        self.foods = []

    def spawn_food(self):
        max_food_count = 50
        while len(self.foods) < max_food_count:
            x, y = random.randint(0, SCREEN_WIDTH - 10), random.randint(0, SCREEN_HEIGHT - 10)
            self.foods.append(Food(random.randint(3, 7), (x, y)))

    def manage(self):
        for creature in self.creatures:
            creature.update()
            creature.seekFood(self.foods)
        self.spawn_food()

ecosystem = Ecosystem()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    ecosystem.manage()

    screen.fill(WHITE)
    for creature in ecosystem.creatures:
        creature.draw(screen)
    for food in ecosystem.foods:
        food.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
