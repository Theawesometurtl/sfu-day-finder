from calendar import day_abbr
from datetime import datetime

import sfu_api
import typer
from rich.console import Console
from rich.progress import track
from rich.table import Column, Table

day_abbr = list(day_abbr)


def main(department: str = typer.Argument(help="Department code")):
    client = sfu_api.Client()
    course_numbers = client.get_course_numbers("current", "current", department)
    table = Table(title=f"{department.title()} Course Schedules")
    table.add_column("Course", justify="right", style="cyan")
    table.add_column("Course Sections")
    for course_number in track(course_numbers, description="Course Numbers"):
        course_sections = client.get_course_sections(
            "current", "current", department, course_number
        )
        for course_section in course_sections:
            course_outline = client.get_course_outline(
                "current", "current", department, course_number, course_section
            )
            if (
                course_outline.course_schedule is not None
                and len(course_outline.course_schedule) != 0
            ):
                schedule_tables = (
                    (schedule, Table("Day", "Start Time", "End Time"))
                    for schedule in course_outline.course_schedule
                    if schedule.days is not None
                    and schedule.start_time is not None
                    and schedule.end_time is not None
                    and schedule.start_date is not None
                    and schedule.end_date is not None
                    and schedule.start_date <= datetime.now() <= schedule.end_date
                )
                for schedule, schedule_table in schedule_tables:
                    assert schedule.days is not None  # for type checking
                    assert schedule.start_time is not None  # for type checking
                    assert schedule.end_time is not None  # for type checking

                    schedule_table.add_row(
                        ", ".join(map(day_abbr.__getitem__, schedule.days)),
                        schedule.start_time.strftime("%H:%M"),
                        schedule.end_time.strftime("%H:%M"),
                    )
                    section_table = Table(
                        Column("Course Section", justify="right", style="green"), "Days"
                    )
                    section_table.add_row(str(course_section), schedule_table)
                    table.add_row(course_number.name, section_table)
                    # days = schedule.days
                    # name = course_outline.info.name
                    # start_time = schedule.start_time
                    # end_time = schedule.end_time

                    # if name is not None:
                    #     print(f"{name} ({course_number}-{course_section})")
                    # else:
                    #     print(f"{department} {course_number}-{course_section}")
                    # for day in days:
                    #     print(
                    #         f"  {day_name[day]} from {map_opt(isoformat_m, start_time)}-{end_time}"
                    #     )
    console = Console()
    console.print(table)


def app():
    typer.run(main)


if __name__ == "__main__":
    app()
