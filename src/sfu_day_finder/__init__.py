import sfu_api
import typer
from tqdm import tqdm

def main(department: str = typer.Argument(help="Department code")):
    client = sfu_api.Client()
    course_numbers = client.get_course_numbers("current", "current", department)
    for course_number in tqdm(course_numbers, desc="Course Numbers"):
        course_sections = client.get_course_sections("current", "current", department, course_number)
        for course_section in tqdm(course_sections, desc="Course Sections"):
            course_outline = client.get_course_outline("current", "current", department, course_number, course_section)
            for schedule in course_outline.course_schedule:
                days = schedule.days
                start_time = schedule.start_time
                end_time = schedule.end_time
                
                if days:
                    for day in days:
                        print(f"{department} {course_number} {course_section}: {day.name} from {start_time}-{end_time}")
def app():
    typer.run(main)