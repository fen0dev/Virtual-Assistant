from sklearn.tree import DecisionTreeClassifier
import json

def load_training_data():
    try:
        with open('user_preferences.json', 'r') as file:
            user_data = json.load(file)
            preferences = user_data['preferences']
            mood = user_data['mood']
            activities = user_data['activity']

            # Encoding data
            pref_encoded = [0 if p == 'indoor' else 1 for p in preferences]
            mood_encoded = [0 if m == 'relaxed' else 1 for m in mood]
            activity_encoded = []
            for act in activities:
                if act in ["Reading a book", "Watching a movie or series", "Cooking or baking something new", "Playing board games or video games"]:
                    activity_encoded.append(0)
                elif act in ["Going for a walk in the park", "Having a picnic", "Going for a bike ride", "Playing outdoor sports like tennis or soccer", "Going to the beach"]:
                    activity_encoded.append(1)
                elif act in ["Doing a home workout or yoga session", "Dancing to your favorite music"]:
                    activity_encoded.append(2)
                elif act in ["Meditating or practicing mindfulness", "Taking a long bath"]:
                    activity_encoded.append(3)
                else:
                    activity_encoded.append(4)      # Default to relaxing at home

            x = list(zip(pref_encoded, mood_encoded))
            y = activity_encoded

            return x, y
    except FileNotFoundError:
        return [], []

def train_model():
    x, y = load_training_data()
    if x and y:
        model = DecisionTreeClassifier()
        model.fit(x, y)
        return model
    else:
        return None