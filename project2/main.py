"""
main.py
Entry point for the Dice Simulator.
Gets input from the user, runs the simulation and generates the PDF report.
No logic here — only calls to dicesimulator and generate_report.
"""

import os
import time
import random
from dicesimulator import run_analysis, MIN_THROWS, MAX_THROWS
from report import generate_report


DICE_EMOJI = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}


def print_banner():
    print("\n" + "=" * 50)
    print("   🎲  DICE SIMULATOR — Casino Odds Analyser")
    print("=" * 50)


def get_int_input(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  That doesn't look like a number. Try again.")


def roll_animation(num_dice: int):
    """Simple dice rolling animation using emojis."""
    for _ in range(8):
        dice = " ".join(DICE_EMOJI[random.randint(1, 6)] for _ in range(num_dice))
        print(f"\r  🎲 {dice}", end="", flush=True)
        time.sleep(0.1)
    print()


def print_summary(analysis: dict):
    n  = analysis["num_throws"]
    nd = analysis["num_dice"]
    print(f"\n{'─' * 50}")
    print(f"  Results for {n:,} throws with {nd} {'die' if nd == 1 else 'dice'}")
    print(f"{'─' * 50}")

    print("\n📊  Q1 & Q2 — Distribution")
    for v, c in sorted(analysis["distribution"].items()):
        bar = "█" * int(c / n * 200)
        emoji = DICE_EMOJI.get(v, "  ") if nd == 1 else ""
        print(f"  {emoji} {v:>2} │ {bar:<40} {c:>6} ({c/n:.1%})")

    most_v, most_c = analysis["most_frequent"]
    least_v, least_c = analysis["least_frequent"]
    print(f"\n  Most frequent : {most_v}  ({most_c:,} times)")
    print(f"  Least frequent: {least_v}  ({least_c:,} times)")

    print("\n🎯  Q3 — Empirical Probability")
    for v, p in sorted(analysis["empirical_probabilities"].items()):
        print(f"  Result {v}: {p:.2%}")

    print("\n📈  Q4 — Stats")
    print(f"  Average : {analysis['average']}")
    print(f"  Min     : {analysis['minimum']}")
    print(f"  Max     : {analysis['maximum']}")

    if nd == 1:
        print("\n⚖️   Q5 — Evenness")
        ev = analysis["evenness"]
        print(f"  Max diff: {ev['max_diff']}  →  {ev['verdict']}")

    print("\n🃏  Q7 & Q8 — Even / Odd")
    print(f"  Even: {analysis['even_percentage']:.2f}%")
    print(f"  Odd : {analysis['odd_percentage']:.2f}%")

    if nd == 2:
        print(f"\n🎰  Q6 — Doubles: {analysis['doubles_percentage']:.2f}%")

    # bonus 1 — Casino verdict
    most_v, _ = analysis["most_frequent"]
    verdict = "🤑 Lucky night! Go to the casino!" if most_v > 3.5 else "😬 Bad luck... stay home tonight!"
    print(f"\n{'─' * 50}")
    print(f"  {verdict}")

    # bonus 2 — Lucky number
    lucky = random.choice(analysis["results"])
    lucky_emoji = DICE_EMOJI.get(int(lucky), "🎲")
    print(f"  🍀 Your lucky number tonight: {lucky_emoji} {lucky}")
    print(f"{'─' * 50}")


def main():
    print_banner()

    num_dice = get_int_input("\nHow many dice? (1 or 2): ", 1, 2)
    num_throws = get_int_input(
        f"How many throws? ({MIN_THROWS} – {MAX_THROWS:,}): ",
        MIN_THROWS, MAX_THROWS
    )

    # Run simulation
    analysis = run_analysis(num_throws, num_dice)
    roll_animation(num_dice)

    # Print results
    print_summary(analysis)

    # Generate PDF
    output_path = os.path.join(os.path.dirname(__file__), "dice_report.pdf")
    print("\n📄 Generating PDF report...", end="", flush=True)
    generate_report(analysis, output_path)
    print(f" ✓\n\n  Saved to: {output_path}\n")


if __name__ == "__main__":
    main()
