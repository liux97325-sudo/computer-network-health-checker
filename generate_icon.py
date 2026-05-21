from PIL import Image, ImageDraw


def make_icon(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    scale = size / 256

    def xy(points):
        return tuple(int(v * scale) for v in points)

    draw.rounded_rectangle(xy((18, 18, 238, 238)), radius=int(48 * scale), fill=(20, 110, 243, 255))
    draw.rounded_rectangle(xy((34, 34, 222, 222)), radius=int(38 * scale), outline=(120, 205, 255, 255), width=max(2, int(8 * scale)))

    draw.arc(xy((56, 92, 200, 222)), 205, 335, fill=(255, 255, 255, 255), width=max(3, int(14 * scale)))
    draw.arc(xy((82, 122, 174, 220)), 205, 335, fill=(54, 179, 126, 255), width=max(3, int(14 * scale)))
    draw.ellipse(xy((116, 174, 140, 198)), fill=(255, 176, 32, 255))

    draw.line(xy((128, 140, 128, 58)), fill=(255, 255, 255, 255), width=max(3, int(16 * scale)))
    draw.ellipse(xy((104, 34, 152, 82)), fill=(255, 176, 32, 255), outline=(255, 255, 255, 255), width=max(2, int(6 * scale)))
    return image


sizes = [16, 24, 32, 48, 64, 128, 256]
images = [make_icon(size) for size in sizes]
images[-1].save("network_health.ico", sizes=[(size, size) for size in sizes], append_images=images[:-1])
