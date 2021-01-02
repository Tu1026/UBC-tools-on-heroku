import os
import re

from pathvalidate import sanitize_filename
from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.exceptions import Unauthorized, ResourceDoesNotExist
from canvasapi.file import File
from canvasapi.module import Module, ModuleItem
from pathlib import Path


def extract_files(text):
    text_search = re.findall("/files/(\\d+)", text, re.IGNORECASE)
    groups = set(text_search)
    return groups


def extraction(token, num):
    url1 = "https://canvas.ubc.ca/"
    output1 = Path("scraper/")
    num_of_courses = 1
    output = Path("app/scraper/")
    
    canvas = Canvas(url1, token)
    course = canvas.get_course(int(num))
    courses = []
    for x in range(num_of_courses):
        courses.append(course)
        
    for course in courses:
        course: Course = course
        modules = course.get_modules()

        files_downloaded = set()

        for module in modules:
            module: Module = module
            module_items = module.get_module_items()
            for item in module_items:
                item: ModuleItem = item

                path = f"{output}/" \
                    f"{sanitize_filename(course.name)}/" \
                    f"{sanitize_filename(module.name)}/"
                if not os.path.exists(path):
                    os.makedirs(path)

                item_type = item.type
                print(f"{course.name} - "
                      f"{module.name} - "
                      f"{item.title} ({item_type})")

                if item_type == "File":
                    file = canvas.get_file(item.content_id)
                    files_downloaded.add(item.content_id)
                    file.download(path + sanitize_filename(file.filename))
                elif item_type == "Page":
                    page = course.get_page(item.page_url)
                    with open(path + sanitize_filename(item.title) + ".html", "w", encoding="utf-8") as f:
                        f.write(page.body or "")
                    files = extract_files(page.body or "")
                    for file_id in files:
                        if file_id in files_downloaded:
                            continue
                        try:
                            file = course.get_file(file_id)
                            files_downloaded.add(file_id)
                            file.download(path + sanitize_filename(file.filename))
                        except ResourceDoesNotExist:
                            pass
                elif item_type == "ExternalUrl":
                    url = item.external_url
                    with open(path + sanitize_filename(item.title) + ".url", "w") as f:
                        f.write("[InternetShortcut]\n")
                        f.write("URL=" + url)
                elif item_type == "Assignment":
                    assignment = course.get_assignment(item.content_id)
                    with open(path + sanitize_filename(item.title) + ".html", "w", encoding="utf-8") as f:
                        f.write(assignment.description or "")
                    files = extract_files(assignment.description or "")
                    for file_id in files:
                        if file_id in files_downloaded:
                            continue
                        try:
                            file = course.get_file(file_id)
                            files_downloaded.add(file_id)
                            file.download(path + sanitize_filename(file.filename))
                        except ResourceDoesNotExist:
                            pass

        try:
            files = course.get_files()
            for file in files:
                file: File = file
                if not file.id in files_downloaded:
                    print(f"{course.name} - {file.filename}")
                    path = f"{output}/{sanitize_filename(course.name)}/" \
                        f"{sanitize_filename(file.filename)}"
                    file.download(path)
        except Unauthorized:
            pass