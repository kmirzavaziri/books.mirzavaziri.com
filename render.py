import copy
import sys

import yaml
import jinja2

CHAPTER_FA = "فصل"
CHAPTER_EN = "Chapter"
SECTION_FA = "بخش"
SECTION_EN = "Section"
SEMICOLON_FA = "؛"
SEMICOLON_EN = ";"


def main():
    if len(sys.argv) < 1:
        raise ValueError("Please provide book name")

    book = sys.argv[1]

    info_filename = f"info/{book}.yaml"
    template_filename = f"{book}/index.html.j2"
    result_filename = f"public/{book}/index.html"

    if book == "root":
        result_filename = "public/index.html"

    with open(info_filename, "r") as f:
        info = yaml.safe_load(f)

    templateEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="templates"))
    template = templateEnv.get_template(template_filename)

    with open(result_filename, "w") as f:
        f.write(template.render(info=enrich(book, info)))


def enrich(book, info):
    if book == "virgo":
        return enrich_virgo(info)


def enrich_virgo(info):
    info = copy.copy(info)
    for section in info["sections"]:
        if "generate_title" in section:
            section["title"] = generate_title(section["generate_title"], info["chapters"])

    return info


def generate_title(t, chapters):
    return {
        "fa": f"{CHAPTER_FA} {ordinal_fa(t['chapter'])}{SEMICOLON_FA} {chapters[t['chapter'] - 1]['fa']}<br>"
              f"{SECTION_FA} {ordinal_fa(t['section'])}",
        "en": f"{CHAPTER_EN} {t['chapter']}{SEMICOLON_EN} {chapters[t['chapter'] - 1]['en']}<br>"
              f"{SECTION_EN} {t['section']}",
    }


def ordinal_fa(n):
    return {
        1: "اول",
        2: "دوم",
        3: "سوم",
        4: "چهارم",
        5: "پنجم",
        6: "ششم",
        7: "هفتم",
        8: "هشتم",
        9: "نهم",
        10: "دهم",
    }[n]


if __name__ == "__main__":
    main()
