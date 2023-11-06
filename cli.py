import questionary
from main import Streak
from main import Habit
from main import Timespan
from db import get_unchecked_habits
from db import del_habit
from db import update_longest_streak
from db import get_timespan_given_habit
from db import complete_habit
from db import reset_streak
from db import get_all_tracked_habits
from db import get_all_habits_same_periodicity
from db import get_longest_streak_given_habit
from db import get_highest_streak
from db import get_db
from db import add_new_habit


db = get_db()

def cli():

    choice = questionary.select(f"What do you want to do?",
                                choices=["Create Habit", "analyse habits", "manage habits"]).ask()

    if choice == "Create Habit":
        habit_name = questionary.text(f"Name the Habit you want to create").ask()
        description = questionary.text(f"what is this habit about?").ask()
        timespan = questionary.select(f"Please specify the timespan",
                                      choices=["weekly", "daily"]).ask()
        add_new_habit(habit_name, timespan, description)
        questionary.text("your Habit is no being tracked! \n Your Streak starts now!").ask()


    elif choice == "analyse habits":
        choice = questionary.select(f"What would you like to know about your habits?",
                           choices=["return a list of all currently tracked habits",
                                    "returning a list of all habits with the same timespan",
                                    "return the longest run streak of all defined habits",
                                    "returning the longest run streak for a given habit"]).ask()
        if choice == "return a list of all currently tracked habits":
            all_habits = get_all_tracked_habits
            questionary.text(f"Here is a list of all currently tracked habits: {all_habits} ").ask()

        elif choice == "returning a list of all habits with the same timespan":
            timespan = questionary.select(f"please clarify timespan.",
                                        choices=["weekly", "daily"]).ask()
            same_timespan = get_all_habits_same_periodicity(timespan)
            questionary.text(f"Here is a list of all tracked Habits with the same timespan: {same_timespan} ").ask()

        elif choice == "return the longest run streak of all defined habits":
            longest_streak_all_habits = get_highest_streak
            questionary.text(
                f"Here is the longest streak of all your tracked Habits: {longest_streak_all_habits}").ask()  # habit_name??

        elif choice == "returning the longest run streak for a given habit":
            habit_name = questionary.text(f"please specify habit name").ask()
            longest_streak_given_habit = get_longest_streak_given_habit(habit_name)
            questionary.text(
                f"Here is the longest Streak you ever accomplished for {habit_name}: {longest_streak_given_habit}").ask()

    elif choice == "manage habits":
        choice = questionary.select(f"what would you like to do?",
                           choices=["delete a habit", "check off a habit", "show unchecked Habits"]).ask()

        if choice == "delete a habit":
            habit_name = questionary.text(f"please give the name of the habit you want to delete").ask()
            del_habit(habit_name)
            questionary.text(f"your habit has been deleted ").ask()
        elif choice == "check off a habit":
            habit_name = questionary.text(f"Please give the name of the habit you would like to check off").ask()
            timespan = get_timespan_given_habit(habit_name)
            streak = Streak(habit_name)
            streak_update = streak.update_streak(habit_name)
            complete_habit(habit_name)
            update_longest_streak(habit_name)
            questionary.text(f"{streak_update}").ask()
            if streak_update == "Sadly, you have failed to keep up this streak.":
                choice = questionary.select("Do you want to start over?", choices=["Yes","No"]).ask()
                if choice == "Yes":
                    reset_streak(habit_name)
                    questionary.text("Your Habit is being tracked. Remember to check it off!").ask()
                else:
                    questionary.text("Press Enter to Continue").ask()

        elif choice == "show unchecked Habits":
            unchecked_habits = get_unchecked_habits()
            questionary.text(f"These are all uncompleted Habits: {unchecked_habits}").ask()


if __name__ == "__main__":
    cli()











