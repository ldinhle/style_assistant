import json
import random
import matplotlib.pyplot as plt
from PIL import Image

with open('StyleAssistant/config.json', 'r') as f:
    config = json.load(f)

CATEGORIES = config['categories']

# Transition matrix defining the probabilities of moving from one clothing item to another
TRANSITION_MATRIX = {
	'tops' : {
		'tshirt' : {
			'jeans' : 0.3,
			'shorts' : 0.3,
			'skirt' : 0.1,
			'slacks' : 0.1,
			'leggings' : 0.2
		},
		'long-sleeve' : {
			'jeans' : 0.5,
			'shorts' : 0.1,	
			'skirt' : 0.1,
			'slacks' : 0.1,
			'leggings' : 0.2
		},
		'tanktop' : {
			'jeans' : 0.1,
			'shorts' : 0.5,
			'skirt' : 0.2,
			'slacks' : 0.1,
			'leggings' : 0.1
		},
		'blouse' : {
			'jeans' : 0.2,
			'shorts' : 0.05,
			'skirt' : 0.4,
			'slacks' : 0.4,
			'leggings' : 0.05
		},
		'corset-top' : {
			'jeans' : 0.2,
			'shorts' : 0.1,
			'skirt' : 0.5,
			'slacks' : 0.1,
			'leggings' : 0.1
		}
	},
	'pants' : {
		'jeans' : {
			'sneakers' : 0.35,
			'boots' : 0.2,
			'heels' : 0.05,
			'loafers' : 0.2,
			'sandals' : 0.2,
		},
		'shorts' : {
			'sneakers' : 0.3,
			'boots' : 0.2 ,
			'heels' : 0.15 ,
			'loafers' : 0.15,
			'sandals' : 0.2,
		},
		'skirt' : {
			'sneakers' : 0.05,
			'boots' : 0.25,
			'heels' : 0.5 ,
			'loafers' : 0.1,
			'sandals' : 0.1,
	},
		'slacks' : {
			'sneakers' : 0.05,
			'boots' : 0.25,
			'heels' : 0.5 ,
			'loafers' : 0.1,
			'sandals' : 0.1,
		},
		'leggings' : {
			'sneakers' : 0.2,
			'boots' : 0.2,
			'heels' : 0.05,
			'loafers' : 0.2,
			'sandals' : 0.35,
		}
	},
	'shoes': {
		'sneakers': {
			'end': 1.0
		},
		'boots': {
			'end': 1.0
		},
		'heels': {
			'end': 1.0
		},
		'loafers': {
			'end': 1.0
		},
		'sandals': {
			'end': 1.0
		}
	}
}

# Image paths for each clothing item
IMAGE_PATHS = {
	'tshirt' : 'StyleAssistant/assets/images/tshirt.jpg',
	'blouse' : 'StyleAssistant/assets/images/blouse.jpg',
	'tanktop' : 'StyleAssistant/assets/images/tanktop.jpg',
	'long-sleeve' : 'StyleAssistant/assets/images/longsleeve.jpg' ,
	'corset-top' : 'StyleAssistant/assets/images/corset-top.jpg',
	'jeans' : 'StyleAssistant/assets/images/jeans.jpg',
	'shorts' : 'StyleAssistant/assets/images/shorts.jpg',
	'skirt' : 'StyleAssistant/assets/images/skirt.jpg',
	'slacks' : 'StyleAssistant/assets/images/slacks.jpg',
	'leggings' : 'StyleAssistant/assets/images/leggings.jpg',
	'sneakers' : 'StyleAssistant/assets/images/sneakers.jpg',
	'boots' : 'StyleAssistant/assets/images/boots.jpg',
	'heels' : 'StyleAssistant/assets/images/heels.jpg',
	'loafers' : 'StyleAssistant/assets/images/loafers.jpg',
	'sandals' : 'StyleAssistant/assets/images/sandals.jpg',
}

# Load weather adjustment config file
with open('StyleAssistant/weather_adjustments.json', 'r') as f:
    weather_adjustments = json.load(f)

class StyleAssistant:
	def __init__(self, transition_matrix):
		self.transition_matrix = transition_matrix
		self.item_to_category = self.create_reverse_lookup(transition_matrix)

	
	def update_probabilities(self, weather):
		if weather in weather_adjustments:
			factors = weather_adjustments[weather]
			for category, items in self.transition_matrix.items():
				for item, transitions in items.items():
					if item in factors[category]:
						for target in transitions:
							self.transition_matrix[category][item][target] *= factors[category][item]

        # Normalize probabilities
		for category in self.transition_matrix:
			for item, transitions in self.transition_matrix[category].items():
				total = sum(transitions.values())
				for key in transitions:
					transitions[key] /= total

				
	def create_reverse_lookup(self, transition_matrix):
		item_to_category = {}
		for category, items in transition_matrix.items():
			for item in items:
				item_to_category[item] = category
		return item_to_category 
	
	def get_category(self, item):
		category = self.item_to_category.get(item, None)
		if category is None:
			print(f"warning, category not found for item '{item}' ")
		return category 
	
	def get_next_item(self, curr_item):
		curr_category = self.get_category(curr_item)
		possible_items = self.transition_matrix[curr_category][curr_item]
		next_item = random.choices(list(possible_items.keys()), weights=list(possible_items.values()))[0]
		return next_item
	
	def build_outfit(self, start_item):
		curr_item = start_item
		outfit_list = [curr_item]

		while curr_item != 'end':
			curr_item = self.get_next_item(curr_item)
			outfit_list.append(curr_item)
		return outfit_list[:-1]

	def show_outfit(self, outfit):
		fig, axs = plt.subplots(len(outfit), 1, figsize=(4, 6))
		images = []

		for ax, item in zip(axs, outfit):
			ax.imshow(Image.open(IMAGE_PATHS[item]))
			images.append(ax.imshow(Image.open(IMAGE_PATHS[item])))
			ax.set_title(item)
			ax.set_axis_off()
		plt.tight_layout()
		plt.show()


def main():
	closet = StyleAssistant(TRANSITION_MATRIX)
	
	# stable_outfit = ['tshirt', 'jeans', 'sneakers']
	# Prompt the user for the starting top item
	# start_item = input("Enter a top item you want to start with ('blouse', 'tshirt', 'tanktop', 'long-sleeve', 'corset-top'): ").strip().lower()
	

	# Prompt the user for the weather condition
	weather = input("Enter the weather condition ('cold', 'hot'): ").strip().lower()
    
    # Update probabilities based on weather
	closet.update_probabilities(weather)

	# Randomize the starting top item
	start_item = random.choice(CATEGORIES['tops'])
	print(f"Randomly selected starting top item: {start_item}")
	
	outfit = closet.build_outfit(start_item)
	closet.show_outfit(outfit)
	print(outfit)

if __name__ == "__main__":
	main()