# data-engineering-interviews.org © 2020-present
# maintainer: Dmitry Kisler

import os
import sys
import pathlib
from typing import List, Union
import time
import re
import logging
import inspect


DIR_BASE = pathlib.Path(__file__).absolute().parents[1]

DIR_SOURCE_QUESTIONS = os.getenv("DIR_SOURCE_QUESTIONS",
                                 f"{DIR_BASE}/questions")
DIR_SITE_CONTENT = os.getenv("DIR_SITE_CONTENT",
                             f"{DIR_BASE}/website/content")
DIR_SOURCE_CONTENT = os.getenv("DIR_SOURCE_CONTENT",
                               f"{DIR_BASE}/website/content-fixed")
DIR_SOURCE_IMG = os.getenv("DIR_SOURCE_IMG",
                           f"{DIR_BASE}/img")
DIR_DESTINATION_IMG = os.getenv("DIR_DESTINATION_IMG",
                                f"{DIR_BASE}/website/static/img")
PATH_README = os.getenv("PATH_README",
                        f"{DIR_BASE}/README.md")
PATH_COC = os.getenv("PATH_COC",
                     f"{DIR_BASE}/CODE-OF-CONDUCT.md")

CONFIG = {
    "question": {
        "weight": 1,
        "prefix": """{{<panel title="Warning" style="warning" >}}
The answers here are given by the community. Be careful and double check the answers before using them. If you see an error, please create a PR with a fix.
{{< button style="outline-success" link="https://github.com/kislerdm/data-engineering-interviews/edit/master/questions/<<category>>.md" >}} Edit questions {{< /button >}}
{{</panel >}}

{{<panel title="Legend" style="success" >}}
👶 easy ‍⭐ medium 🚀 expert
{{</panel>}}
""",
    },
    "questions_categories": {
        "weight": 2,
        "title": "Questions categories",
        "prefix": """{{<panel title="Warning" style="warning" >}}
The answers here are given by the community. Be careful and double check the answers before using them. If you see an error, please create a PR with a fix.
{{</panel >}}
"""
    },
    "home": {
        "weight": 1,
        "title": "Home",
        "prefix": """<img src="https://img.shields.io/badge/dynamic/json?label=24h%20visitors&style=social&color=green&query=cnt&url=https%3A%2F%2Fdata-engineering-interviews-stats.dkisler.workers.dev%2F%3Fq%3D1440&cacheSeconds=1800">"""
    },
    "coc": {
        "weight": 10,
        "title": "Code of conduct",
    },
}

CONTENT_TAG = "<!-- content -->"
CONTENT_TAG_RE = re.compile(f"{CONTENT_TAG}(.*)$", re.M | re.DOTALL)
QUESTION_TAG_RE = re.compile(r"###\s.*\?")


class getLogger():
    def __init__(self,
                 kill: bool = True):
        """Logger.

        Args:
          kill: Terminate process on error.
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s.%(msecs)03d [%(levelname)-5s] [%(name)-12s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logs = logging.getLogger("website_builder")
        self.kill = kill

    def send(self, message: str, is_error: bool = True):
        """Message send method

        Args:
          message: Logging message
          is_error: Message severity level.
        """
        if is_error:
            self.logs.error(message)
        else:
            self.logs.info(message)

        if self.kill:
            sys.exit(1)


def get_line():
    """Returns the current line number."""
    return inspect.currentframe().f_back.f_lineno


def ls(path: str,
       file_extention: str = "") -> List[str]:
    """List files.

    Args:
      path: Path to files.
      file_ending: Files extention.

    Returns:
      List of files.
    """
    output = []
    for p in os.listdir(path):
        path_inner = f"{path}/{p}"
        if os.path.isdir(path_inner):
            output.extend(ls(path_inner,
                             file_extention=file_extention))
        elif p.endswith(file_extention):
            output.append(path_inner)
    return output


def read(path: str) -> str:
    """Function to read a md file.

    Args:
      path: Path to file.

    Returns:
      File text content.

    Raises:
      IOError: Happened when i/o error occurred.
      FileNotFoundError: Happened when file not found.
      PermissionError: Happened when file is not accessible.
    """
    try:
        if os.path.isfile(path):
            with open(path, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"{path} doesn't exist.")
    except FileNotFoundError as ex:
        raise FileNotFoundError(f"[line {get_line()}] {ex}")
    except PermissionError as ex:
        raise PermissionError(f"[line {get_line()}] {ex}")


def mkdir(path: Union[str, pathlib.PosixPath]) -> None:
    """Function to run 'mkdir -p'.

    Args:
      path: Path to object on disk.

    Raises:
      NotADirectoryError: Happened when path points to a file.
      PermissionError: Happened when access to create dir(s) is denied.
    """
    try:
        path = str(path) if isinstance(path, pathlib.Path) else path
        if not os.path.isdir(path):
            os.makedirs(path)
    except NotADirectoryError as ex:
        raise NotADirectoryError(f"[line {get_line()}] {ex}")
    except PermissionError as ex:
        raise PermissionError(f"[line {get_line()}] {ex}")


def ln(source: str,
       destination: str) -> None:
    """Function to bulk symblink content of one dir to another dir.

    Args:
      source: Source dir.
      dist: Destination dir.

    Raises:  
      PermissionError: Happened on permission denied.
      IOError: Happened when i/o error occurred.
    """
    try:
        for obj in ls(source):
            dest_obj = obj.replace(source, destination)
            mkdir(pathlib.Path(dest_obj).parent)
            os.system(f"ln -sf {obj} {dest_obj}")
    except PermissionError as ex:
        raise PermissionError(f"[line {get_line()}] {ex}")
    except IOError as ex:
        raise IOError(f"[line {get_line()}] {ex}")


def write(path: str, obj: str) -> None:
    """Function to write a md file.

    Args:
      path: Path to file.
      obj: Text to write

    Raises:
      IOError: Happened when i/o error occurred.
      IsADirectoryError: Happened when path points to a dir.
      PermissionError: Happened when access to create dir(s) is denied.
    """
    try:
        dir_obj = pathlib.Path(path).absolute().parent
        mkdir(dir_obj)
        with open(path, 'w') as f:
            f.write(obj)
    except IOError as ex:
        raise IOError(ex)
    except IsADirectoryError as ex:
        raise IsADirectoryError(f"[line {get_line()}] {ex}")
    except PermissionError as ex:
        raise PermissionError(f"[line {get_line()}] {ex}")


def generate_page(config: dict,
                  content_input: str) -> str:
    """Function to generate output md page.

    Args:
      config: Page config.
      content: Source content

    Returns:
      Resulting page for output.

    Raises:
      ValueError: Happened on faulty input.
    """
    def _extract_content(inpt: str) -> str:
        """Main content extractor."""
        return "\n".join(CONTENT_TAG_RE.findall(inpt))

    if "title" not in config:
        raise ValueError(f"Input config must contain 'title' attribute.")

    output = f"""---
title: {config['title']}
weight: {config['weight']}
draft: false
---\n
"""

    if "prefix" in config:
        output = f"{output}{config['prefix']}"

    output = f"{output}\n{_extract_content(content_input)}"

    return output


def get_stats(content: str) -> int:
    """Function to count number of questions.

    Args:
      content: Page content.

    Returns:
      Count of questions on the page.
    """
    return len(QUESTION_TAG_RE.findall(content))


def generate_stats_table(stats: dict) -> str:
    """Function to generate md table with questions stats.

    Args:
      stats: Stats dict. 

            {
                "category": {
                    "title" str,
                    "cnt": int,
                }
            }

    Returns:
      Md table string.
    """
    cnt_total = sum([v['cnt'] for v in stats.values()])

    header = f"""## Questions categories
    
*Total number of questions as of {time.strftime('%Y-%m-%d', time.gmtime())}*: **{cnt_total}**
"""

    table_body = "\n".join([f"|[{v['title']}](questions/{k}/)|{v['cnt']}|"
                            for k, v in stats.items()])
    return f"""{header}\n
|Category|Number of questions|
|:-:|-:|
{table_body}"""


def main() -> None:
    logs = getLogger()

    stats_questions = {}

    # generate questions pages
    path_questions = ls(DIR_SOURCE_QUESTIONS)

    for path in path_questions:
        category = path.split('/')[-1].split('.')[0]
        category_title = category.replace("-", " ").capitalize()

        try:
            content_input = read(path)
        except Exception as ex:
            logs.send(f"Reading error for {category}: {ex}")

        try:
            content_page = generate_page(
                config={
                    **CONFIG['question'],
                    "title": category_title,
                },
                content_input=content_input)

            content_page = content_page.replace("<<category>>", category)
        except Exception as ex:
            logs.send(f"Content generating error for {category}: {ex}")

        try:
            write(f"{DIR_SITE_CONTENT}/questions/{category}.md", content_page)
        except Exception as ex:
            logs.send(f"Writing error for {category}: {ex}")

        stats_questions[category] = {
            "cnt": get_stats(content_page),
            "title": category_title,
        }

    # generate questions_categories page
    content_input = "\n".join([f"- [{v['title']}]({k}) (**{v['cnt']}** questions)\n"
                               for k, v in stats_questions.items()])

    content_input = f"{CONTENT_TAG}\n{content_input}"

    content_page = generate_page(config=CONFIG['questions_categories'],
                                 content_input=content_input)

    try:
        write(f"{DIR_SITE_CONTENT}/questions/_index.md", content_page)
    except Exception as ex:
        logs.send(f"Writing error for questions categories page: {ex}")
    
    # generate LP
    try:
        content_input = read(PATH_README)
    except Exception as ex:
        logs.send(f"README.md reading error: {ex}")

    try:
        content_page = generate_page(config=CONFIG['home'],
                                     content_input=content_input)
    except Exception as ex:
        logs.send(f"Home page generating error: {ex}")

    # add stats
    try:
        stats = generate_stats_table(stats_questions)

        content_page = content_page.replace("""Find full list of questions <a href="https://www.data-engineering-interviews.org/questions/" target="_blank">here</a>.""",
                                            stats)
    except Exception as ex:
        logs.send(f"Cannot add stats to home page: {ex}", kill=False)

    content_page = content_page.replace("CODE-OF-CONDUCT.md",
                                        "/code-of-conduct/")\
                               .replace("https://github.com/kislerdm/data-engineering-interviews/contributors",
                                        "/contributors-list/")
    
    try:
        write(f"{DIR_SITE_CONTENT}/_index.md", content_page)
    except Exception as ex:
        logs.send(f"Writing error for home page: {ex}")

    # generate code of conduct page
    try:
        content_input = read(PATH_COC)
    except Exception as ex:
        logs.send(f"CoC reading error: {ex}")

    try:
        content_page = generate_page(config=CONFIG['coc'],
                                     content_input=content_input)
    except Exception as ex:
        logs.send(f"CoC generating error: {ex}")
    try:
        write(f"{DIR_SITE_CONTENT}/code-of-conduct/_index.md", content_page)
    except Exception as ex:
        logs.send(f"Writing error for CoC page: {ex}")

    # link images
    try:
        ln(DIR_SOURCE_IMG, DIR_DESTINATION_IMG)
    except Exception as ex:
        logs.send(f"Images copy error: {ex}")
    
    # link fixed predefined pages
    try:
        ln(DIR_SOURCE_CONTENT, DIR_SITE_CONTENT)
    except Exception as ex:
        logs.send(f"Predefined pages copy error: {ex}")


if __name__ == "__main__":
    main()
