import json
import os
import re


def clear():
    print("\n" * 2)


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
def show_topic(topic):

    clear()

    print("=" * 60)
    print(topic["title"])
    print("=" * 60)

    print("\n[CONTENT]\n")
    print(topic["content"])

    print("\n[KEYWORDS]\n")

    for k in topic["keywords"]:
        print(
            f"{k['english']} → {k['chinese']}"
        )
    print("\n[KEY TAKEAWAYS]\n")

    for item in topic["summary"]:
        print(f" {item}")

def run_short_quiz(topic):

    score = 0

    clear()

    print("=" * 60)
    print("SHORT QUIZ")
    print("=" * 60)

    for q in topic["quiz_short"]:

        user = input(
            f"\n{q['question']}\n> "
        )

        if user.strip().lower() == \
            q["answer"].strip().lower():

            print("✅ Correct")
            score += 1
        else:

            print("❌ Incorrect")

        print(
            f"Answer: {q['answer']}"
        )
    print(
    f"\nFinal Score: {score}/{len(topic['quiz_short'])}"
    )

    input("\nPress Enter...")


def run_long_quiz(topic):

    clear()

    print("=" * 60)
    print("DISCUSSION QUESTIONS")
    print("=" * 60)

    for q in topic["quiz_long"]:
        print(
            "\nQuestion:"
        )

        print(
            q["question"]
        )

        input(
            "\nThink first. Press Enter when ready..."
        )

        print(
            "\nSuggested Answer:"
        )

        print(
            q["answer"]
        )

        input(
            "\nPress Enter..."
        )
    print("\n" + "=" * 60)
    print("TODAY LESSON IS FINISHED")
    print("=" * 60)

    print("\nWhat would you like to do?")
    print("1.Review this topic again")
    print("2.Choose another Topic")
    print("3.EXIT")

    return input("\nSelect: ")


def topic_menu(topic):

    while True:

        show_topic(topic)

        print("\n")
        print("1. Start Quiz")
        print("2. Review Again")
        print("3. Back to Topics")
        print("4"
              ". Exit")

        choice = input("\nSelect: ")

        if choice == "1":

            run_short_quiz(topic)

            action = run_long_quiz(topic)

            if action == "1":
                continue

            elif action == "2":
                return

            elif action == "3":
                exit()

        elif choice == "2":


            continue

        elif choice == "3":

            return

        elif choice == "4":

            exit()

def main():

    while True:

        clear()

        print("=" * 60)
        print("SEMICONDUCTOR LEARNING WITH JASMINE")
        print("=" * 60)

        json_files = [
            f for f in os.listdir()
            if f.endswith(".json")
        ]

        json_files.sort(
            key=lambda x: int(
                re.search(r"Module (\d+)", x).group(1)
            )
        )

        #print(json_files)


        for i, file in enumerate(
                json_files,
                start=1):
            module_name = file.replace(
                ".json", ""
            )

            print(
                f"{i}. {module_name}"
            )
        print("0. Exit")

        module_choice = input(
            "\nChoose Module: "
        )

        if module_choice == "0":
            break

        try:

            module_file = json_files[
                int(module_choice) - 1
                ]

            print("Opening " + module_file)

            data = load_json(module_file)

        except Exception as e:

            print("\nERROR:")
            print(e)

            input("\nPress Enter...")
            continue

        while True:

            clear()

            print(
                f"MODULE: {data['module_name']}"
            )

            print()

            for i, topic in enumerate(
                    data["topics"],
                    start=1):

                print(
                    f"{i}. {topic['title']}"
                )
            print("0. Back")

            topic_choice = input(
                "\nChoose Topic: "
            )

            if topic_choice == "0":
                break

            try:

                topic = data[
                    "topics"
                ][
                    int(topic_choice)-1
                ]

                topic_menu(topic)

            except:

                print(
                    "Invalid topic"
                )

                input(
                    "Press Enter..."
                )


main()