# data-engineering-interviews.org © 2020-present
# maintainer: Dmitry Kisler

import os
import sys
from typing import List
import pathlib
from typing import Union
import time
import re
import logging
import inspect


DIR_BASE = pathlib.Path(__file__).absolute().parents[1]

DIR_SOURCE_QUESTIONS = os.getenv("DIR_SOURCE_QUESTIONS",
                                 f"{DIR_BASE}/questions")
DIR_SITE_CONTENT = os.getenv("DIR_SITE_CONTENT",
                             f"{DIR_BASE}/website/content")
DIR_SOURCE_IMG = os.getenv("DIR_SOURCE_IMG",
                           f"{DIR_BASE}/img")
DIR_DESTINATION_IMG = os.getenv("DIR_SOURCE_IMG",
                                f"{DIR_BASE}/website/static/img")
PATH_COC = os.getenv("PATH_COC",
                     f"{DIR_BASE}/CODE-OF-CONDUCT.md")
PATH_README = os.getenv("PATH_README",
                        f"{DIR_BASE}/README.md")

CONFIG = {
    "question": {
        "weight": 2,
        "prefix": """{{<panel title="Warning" style="warning" >}}
The answers here are given by the community. Be careful and double check the answers before using them. If you see an error, please create a PR with a fix.
{{</panel >}}

{{<panel title="Legend" style="success" >}}
👶 easy ‍⭐️ medium 🚀 expert
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
    },
    "coc": {
        "weight": 3,
        "title": "Code of conduct",
    }
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
    
    table_body = "\n".join([f"|[{v['title']}]({k})|{v['cnt']}|"
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
        
        content_input = read(path)

        content_page = generate_page(
            config={
                **CONFIG['question'],
                "title": category_title,
            },
            content_input=content_input)

        write(f"{DIR_SITE_CONTENT}/questions/{category}.md", content_page)
        
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
    
    write(f"{DIR_SITE_CONTENT}/questions/_index.md", content_page)
    
    # generate LP
    content_input = read(PATH_README)

    content_page = generate_page(config=CONFIG['home'],
                                 content_input=content_input)
    
    # add stats    
    stats = generate_stats_table(stats_questions)
    
    # adjust the page content
    content_page = content_page.replace("CODE-OF-CONDUCT.md",
                                        "code-of-conduct")\
                               .replace("Find full list of questions [here](https://www.data-engineering-interviews.org/questions/)", 
                                        stats)
    
    write(f"{DIR_SITE_CONTENT}/_index.md", content_page)
    
    # generate code of conduct page
    content_input = read(PATH_COC)

    content_page = generate_page(config=CONFIG['coc'],
                                 content_input=content_input)
    
    write(f"{DIR_SITE_CONTENT}/code-of-conduct/_index.md", content_page)


if __name__ == "__main__":
    main()
