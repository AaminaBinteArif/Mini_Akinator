import random

FILENAME = "characters.txt"

QUESTION_MAP = {
    "magic": "magical",
    "glasses": "wear glasses",
    "hero": "a hero",
    "royal": "royalty",
    "villain_parent": "a child of a villain",
    "pirate": "a pirate",
    "athletic": "athletic",
    "fashionable": "fashionable",
    "tech_savvy": "tech-savvy",
    "color_purple": "associated with purple",
    "color_blue": "associated with blue"
}

def load_characters():
    characters = {}
    try:
        with open(FILENAME, "r") as file:
            lines = file.read().strip().split("\n")

        current_name = None
        current_traits = {}

        for line in lines + [""]:
            line = line.strip()
            if not line:
                if current_name:
                    characters[current_name] = current_traits
                    current_name = None
                    current_traits = {}
            elif current_name is None:
                current_name = line
            else:
                if "=" in line:
                    key, value = line.split("=")
                    current_traits[key.strip()] = value.strip().lower() == "true"

        return characters

    except FileNotFoundError:
        print("❌ characters.txt not found.")
        return {}

def save_characters(characters):
    with open(FILENAME, "w") as file:
        for name, traits in characters.items():
            file.write(f"{name}\n")
            for k, v in traits.items():
                file.write(f"{k}={'true' if v else 'false'}\n")
            file.write("\n")
    print("Character saved.")

def ask_traits(known_traits, already_asked=None, max_questions=10):
    traits = {}
    trait_list = list(known_traits)

    if already_asked:
        trait_list = [t for t in trait_list if t not in already_asked]

    random.shuffle(trait_list)
    to_ask = trait_list[:max_questions]

    print("\nAnswer yes or no:")
    for trait in to_ask:
        question = QUESTION_MAP.get(trait, trait)
        answer = input(f"Is / Does the character {question}? (yes/no): ").strip().lower()
        while answer not in ("yes", "no"):
            print("Please answer 'yes' or 'no'.")
            answer = input(f"Is / Does the character {question}? (yes/no): ").strip().lower()
        traits[trait] = answer == "yes"

    return traits

def top_matches(user_traits, characters, top_n=2):
    scored = []

    for name, traits in characters.items():
        score = 0
        total = 0
        for trait, user_val in user_traits.items():
            if trait in traits:
                total += 1
                if traits[trait] == user_val:
                    score += 1
        if total > 0:
            scored.append((name, score / total if total else 0, score, total))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]

def add_additional_traits():
    print("\nWould you like to add additional traits for this character? (yes/no)")
    answer = input().strip().lower()
    additional_traits = {}
    if answer == "yes":
        print("Enter traits one by one in the format trait_name=true/false . Type 'done' when finished.")
        while True:
            line = input().strip()
            if line.lower() == "done":
                break
            if "=" in line:
                key, value = line.split("=")
                val = value.strip().lower() == "true"
                additional_traits[key.strip()] = val
            else:
                print("Invalid format. Please enter as trait_name=true/false")
    return additional_traits

def main():
    characters = load_characters()

    if not characters:
        print("⚠️ No characters in the file.")
        return

    all_traits = set()
    for traits in characters.values():
        all_traits.update(traits.keys())

    print("\nWelcome to Mini Akinator!")

    # First round: ask 10 traits
    user_traits = ask_traits(all_traits, max_questions=10)

    guesses = top_matches(user_traits, characters)

    for i, (name, confidence, score, total) in enumerate(guesses):
        percent = round(confidence * 100)
        answer = input(f"\nIs your character {name}? ({percent}% match) (yes/no): ").strip().lower()
        while answer not in ("yes", "no"):
            print("Please answer 'yes' or 'no'.")
            answer = input(f"Is your character {name}? ({percent}% match) (yes/no): ").strip().lower()
        if answer == "yes":
            print(f"\nYay! I guessed it right: {name}")
            return

    # Second round: ask remaining traits (up to 10 more)
    user_traits.update(ask_traits(all_traits, already_asked=user_traits.keys(), max_questions=10))

    # Second guess
    guesses = top_matches(user_traits, characters)
    for i, (name, confidence, score, total) in enumerate(guesses):
        percent = round(confidence * 100)
        answer = input(f"\nIs your character {name}? ({percent}% match) (yes/no): ").strip().lower()
        while answer not in ("yes", "no"):
            print("Please answer 'yes' or 'no'.")
            answer = input(f"Is your character {name}? ({percent}% match) (yes/no): ").strip().lower()
        if answer == "yes":
            print(f"\nAwesome! I got it after asking more questions: {name}")
            return

    # Still failed to guess
    print("\nI couldn't guess the character.")
    real_name = input("Who was it? ").strip()

    if real_name in characters:
        print("This character already exists in the system. Updating their traits...")
    else:
        print("Adding a new character...")

    # Ask for additional traits if needed
    additional_traits = add_additional_traits()

    # Combine all known traits
    combined_traits = user_traits.copy()
    combined_traits.update(additional_traits)

    characters[real_name] = combined_traits
    save_characters(characters)
    print(f"Learned a character: {real_name}")

if __name__ == "__main__":
    main()
