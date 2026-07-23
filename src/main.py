from dataclasses import dataclass
from typing import List


@dataclass
class School:
    name: str
    country: str
    programs: List[str]
    study_levels: List[str]
    language: str


SCHOOLS = [
    School(
        name="Example Technical University",
        country="Slovakia",
        programs=[
            "Artificial Intelligence",
            "Computer Science",
            "Cybersecurity",
        ],
        study_levels=["Bachelor", "Master"],
        language="English",
    ),
    School(
        name="Example International University",
        country="Armenia",
        programs=[
            "Information Technology",
            "Data Science",
            "Software Engineering",
        ],
        study_levels=["Bachelor", "Master"],
        language="English",
    ),
    School(
        name="Example Research Institute",
        country="Germany",
        programs=[
            "Machine Learning",
            "Robotics",
            "Quantum Computing",
        ],
        study_levels=["Master", "PhD", "Research"],
        language="English",
    ),
]


def search_schools(
    program: str,
    country: str = "",
    study_level: str = "",
) -> List[School]:
    program_query = program.strip().lower()
    country_query = country.strip().lower()
    level_query = study_level.strip().lower()

    results = []

    for school in SCHOOLS:
        matches_program = any(
            program_query in available_program.lower()
            for available_program in school.programs
        )

        matches_country = (
            not country_query
            or country_query in school.country.lower()
        )

        matches_level = (
            not level_query
            or any(
                level_query in level.lower()
                for level in school.study_levels
            )
        )

        if matches_program and matches_country and matches_level:
            results.append(school)

    return results


def display_results(results: List[School]) -> None:
    if not results:
        print("\nNo matching schools were found.")
        return

    print(f"\nFound {len(results)} matching school(s):\n")

    for number, school in enumerate(results, start=1):
        print(f"{number}. {school.name}")
        print(f"   Country: {school.country}")
        print(f"   Programs: {', '.join(school.programs)}")
        print(f"   Study levels: {', '.join(school.study_levels)}")
        print(f"   Language: {school.language}\n")


def main() -> None:
    print("School Check")
    print("Global Academic Discovery Tool")

    program = input("\nEnter a course or research program: ")
    country = input(
        "Enter a preferred country or press Enter for all countries: "
    )
    study_level = input(
        "Enter a study level or press Enter for all levels: "
    )

    results = search_schools(
        program=program,
        country=country,
        study_level=study_level,
    )

    display_results(results)


if __name__ == "__main__":
    main()
