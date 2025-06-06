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
        print(" characters.txt not found.")
        return {}

def save_characters(characters):
    with open(FILENAME, "w") as file:
        for name, traits in characters.items():
            file.write(f"{name}\n")
            for k, v in traits.items():
                file.write(f"{k}={'true' if v else 'false'}\n")
            file.write("\n")
    print("Character saved.")

def ask_traits(known_traits):
    traits = {}
    print("\nAnswer yes or no:")
    for trait in known_traits:
        question = QUESTION_MAP.get(trait, trait)
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
        print("Enter traits one by one in the format trait_name=true/false. Type 'done' when finished.")
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
    user_traits = ask_traits(all_traits)

    guesses = top_matches(user_traits, characters)

    # Interactive guessing loop
    for i, (name, confidence, score, total) in enumerate(guesses):
        percent = round(confidence * 100)
        answer = input(f"\nIs your character {name}? ({percent}% match) (yes/no): ").strip().lower()
        if answer == "yes":
            print(f"\nYay! I guessed it right: {name}")
            return
        elif answer != "no":
            print("Please answer 'yes' or 'no'.")
            return

    # If both guesses fail
    print("\nI couldn't guess the character.")
    real_name = input("Who was it? ").strip()

    # Ask if user wants to add additional traits
    additional_traits = add_additional_traits()

    # Combine traits: user traits + additional traits (overwriting if needed)
    combined_traits = user_traits.copy()
    combined_traits.update(additional_traits)

    characters[real_name] = combined_traits
    save_characters(characters)
    print(f"Learned a new character: {real_name}")

if __name__ == "__main__":
    main()

