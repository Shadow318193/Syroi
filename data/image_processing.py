from PIL import Image, ImageDraw

CHUNK_DEFAULT = 64
ROWS_DEFAULT = 48
OFFSET_DEFAULT = 0
NES_ROWS_DEFAULT = 32
COLORS_FOR_NES_DEFAULT = ((48, 48, 48),
                          (48 * 2, 48 * 2, 48 * 2),
                          (48 * 3, 48 * 3, 48 * 3),
                          (48 * 4, 48 * 4, 48 * 4))


def make_raw_image_mode_simple(file_in, file_out, chunk=CHUNK_DEFAULT, height_in_chunks=ROWS_DEFAULT,
                               start=OFFSET_DEFAULT):
    with open(file_in, "rb") as f:
        data = [_ for _ in f.read()]

    height = chunk * height_in_chunks
    width = len(data) // height
    if len(data) % height != 0:
        width += 1

    img = Image.new("RGB", (width, height))
    drawer = ImageDraw.Draw(img)

    for h in range(height_in_chunks):
        for x in range(width):
            for y in range(chunk):
                pos = y + x * chunk + h * chunk * width + start
                try:
                    drawer.point((x, y + h * chunk), (data[pos], data[pos], data[pos]))
                except IndexError:
                    drawer.point((x, y + h * chunk), (0, 0, 0))

    img.save(file_out)
    print("Файл", file_out, "сохранён")


def make_raw_image_mode_nes(file_in, file_out, height_in_chunks=NES_ROWS_DEFAULT, colors=COLORS_FOR_NES_DEFAULT):
    with open(file_in, "rb") as f:
        data = [bin(_)[2:].rjust(8, "0") for _ in f.read()]

    chunk = 8
    height = chunk * height_in_chunks
    width = len(data) // height_in_chunks // 2

    img = Image.new("RGB", (width, height))
    drawer = ImageDraw.Draw(img)

    row_s = -chunk * 2
    for h in range(height_in_chunks):
        for ch in range(0, width * 2 // chunk, 2):
            row_s += chunk * 2
            if row_s % 16 != 0:
                row_s += row_s % 16
            row_e = row_s + chunk * 2
            row = data[row_s:row_e]
            if len(row) != 16:
                continue
            sprite1 = row[0:chunk]
            sprite2 = row[chunk:chunk*2]
            sprite = [0, 0, 0, 0, 0, 0, 0, 0]
            for x in range(chunk):
                sprite[x] = str(int(sprite1[x]) + int(sprite2[x]) * 2).rjust(8, "0")

            for y in range(chunk):
                for x in range(chunk):
                    try:
                        drawer.point(((ch * chunk // 2) + x, h * chunk + y),
                                     (colors[int(sprite[y][x])][0],
                                      colors[int(sprite[y][x])][1],
                                      colors[int(sprite[y][x])][2]))
                    except IndexError:
                        drawer.point(((ch * chunk // 2) + x, h * chunk + y), (0, 0, 0))

    img.save(file_out)
    print("Файл", file_out, "сохранён")


if __name__ == "__main__":
    pass
