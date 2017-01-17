import sys
import json


def fetch_items(filein):
    movies = list()
    with open(filein, 'r', encoding='utf-8') as f:
        for row in f:
            # file = [ comment | movie ]*
            # comment = # string
            # movie = disk TAB title_with_attributes
            # title_with_attributes =  title TAB attributes
            # attributes = *format | COMMA § category | COMMA # language | COMMA & on_mediaserver
            # title = string [string SPACE]*
            # language = audio SLASH subtitle
            # on_mediaserver = & ms

            # comment
            if row[0] == "#":
                print("continue 1")
                continue

            # wanted
            if row.find("§wanted") > -1:
                print("continue 2")
                continue

            print(">"+row.strip("\n)"))

            # disk, title, attributes
            tokens = row.split("\t")
            disk = ""
            title = ""
            attributes = ""
            if len(tokens) >= 1:
                disk = tokens[0].strip("\n")
            if len(tokens) >= 2:
                title = tokens[1].strip("\n")
            if len(tokens) >= 3:
                attributes = tokens[2].strip("\n")
            print("disk=[{}], title=[{}], attributes=[{}]".format(disk, title, attributes))


            # attributes
            attr = attributes.split(",")
            media = ""
            if len(attributes) == 0 and title != "---":
                media = "AttributeError"
            if len(attributes) > 0 and attributes[0] == " ":
                media = "AttributeError"
            language_spoken = ""
            language_subtitle = ""
            category = []
            onmediaserver = False
            comment = ""
            for i in attr:
                #print("<<{}>>".format(i))
                i = i.strip(" ").strip("\n")
                if len(i) == 0:
                    continue
                if i.find("*") >= 0:
                    media = i.strip("*")
                if i.find("#") >= 0:
                    languages = i.strip("#").split("/")
                    language_spoken = languages[0]
                    if len(languages) >= 2:
                        language_subtitle = languages[1]
                if i.find("§") >= 0:
                    category.append(i.strip("§"))
                if i.find("&ms") >= 0:
                    onmediaserver = True
                if i.find("/") >= 0:
                    comment = i.strip("/")
            print("\tmedia=[{}], spoken=[{}], subtitle=[{}], cat={}, ms=[{}], comment=[{}]".format(
                media, language_spoken, language_subtitle, category, onmediaserver, comment))

            movie = {"title": title, "disk": disk, "media": media, "audio": language_spoken,
                     "subtitle": language_subtitle, "category": category,
                     "mediaserver": onmediaserver, "comment": comment}
            movies.append(movie)
    return movies


def main(filein, fileout):
    items = fetch_items(filein)
    open(fileout, 'wb').write(json.dumps(items, sort_keys=False, indent=4, ensure_ascii=False)
                              .encode('utf8'))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
