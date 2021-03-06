import json
import colorsys


book_data = []

tag_dict = {}

tag_dict_entry = {}

# tag_dict = {
#   "TAG": {
#     "red": {
#       "score": 0,
#       "frequency": 0,
#       "totalPixelFraction": 0
#     }
#   }
# }

books_by_color = {}

primarycolors = ["red", "orange", "yellow", "green", "blue",
  "violet", "pink", "gray", "black", "white"]

for color in primarycolors:
  books_by_color[color] = []

with open('tag_object.json') as jsonfile:
  data = json.load(jsonfile)
  for tag in data.keys():
    tag_dict[tag] = {}
    for color in primarycolors:
      tag_dict[tag][color] = {"score": 0, "frequency": 0, "totalPixelFraction": 0}

def colorCategorize(color):
  for c in ["red", "green", "blue"]:
    if c not in color:
      color[c] = "0"

  (h, l, s) = colorsys.rgb_to_hls(int(color["red"])/255, int(color["green"])/255, int(color["blue"])/255)
  level1 = ""
  level2 = "" # do this later
  hue = h*360
  lightness = l*100
  saturation = s*100

  if lightness < 20:
    level1 = "black"
  elif lightness >= 90:
    level1 = "white"
  elif saturation < 10:
    level1 = "gray"
  elif hue <= 12 or hue >= 336:
    level1 = "red"
  elif hue > 12 and hue < 38:
    level1 = "orange"
  elif hue >= 38 and hue < 62:
    level1 = "yellow"
  elif hue >= 62 and hue < 150:
    level1 = "green"
  elif hue >= 150 and hue < 250:
    level1 = "blue"
  elif hue >= 250 and hue < 292:
    level1 = "violet"
  elif hue >= 292 and hue < 336:
    level1 = "pink"

  return level1, hue, lightness, saturation




with open("book_data.json") as json_file:
  data = json.load(json_file)
  for book in data:

    if "imagePropertiesAnnotation" in book and book["image_url"] != "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png":
      colorsLst = book["imagePropertiesAnnotation"]["dominantColors"]["colors"]
      primaryColor, h, l, s = colorCategorize(colorsLst[0]["color"])

      book["dominantColorCategory"] = primaryColor
      book_data.append(book)
      if int(book["book_id"] ) % 500 == 0:
        print("BOOK: " + book["book_id"])
        print(colorsLst[0]["color"])
        print(primaryColor, h, l, s)
      tag_dict["total"][primaryColor]["score"] += float(colorsLst[0]["score"])
      tag_dict["total"][primaryColor]["frequency"] += 1
      tag_dict["total"][primaryColor]["totalPixelFraction"] += float(colorsLst[0]["pixelFraction"])
      if "tags" in book and primaryColor:
        for tag in book["tags"]:
          if tag["tag_name"] in tag_dict.keys():
            tag_dict[tag["tag_name"]][primaryColor]["score"] += float(colorsLst[0]["score"])
            tag_dict[tag["tag_name"]][primaryColor]["frequency"] += 1
            tag_dict[tag["tag_name"]][primaryColor]["totalPixelFraction"] += float(colorsLst[0]["pixelFraction"])


      # secondaryColor = colorCategorize(colorsLst[1]["color"])

hierarchy_tag_color = {}

# calculate average pixel fraction
for tag_name, tag in tag_dict.items():
  hierarchy_tag_color[tag_name] = {}
  hierarchy_tag_color[tag_name]["tag_name"] = tag_name
  hierarchy_tag_color[tag_name]["children"] = []
  for color_name, color in tag.items():
    if color["frequency"] > 0:
      color["averagePixelFraction"] = color["totalPixelFraction"]/color["frequency"]
    else:
      color["averagePixelFraction"] = 0
    hierarchy_color = color
    hierarchy_color["color_name"] = color_name
    hierarchy_tag_color[tag_name]["children"].append(hierarchy_color)

with open('tag_color.json', 'w') as file:
  json.dump(tag_dict, file, ensure_ascii=False, indent=4)

with open('hierarchy_tag_color.json', 'w') as file:
  json.dump(hierarchy_tag_color, file, ensure_ascii=False, indent=4)

with open('new_book_data.json', 'w') as file:
  json.dump(book_data, file, ensure_ascii=False, indent=4)
