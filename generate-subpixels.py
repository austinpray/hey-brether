from PIL import Image, ImageDraw

def make_image(plan: str) -> Image:
    im = Image.new(mode='RGB', size=(128, 128), color='#ffffff')
    im.filename = f'0c_bin_{plan}.png'

    draw = ImageDraw.Draw(im)

    q1 = [0, 0, 64, 64]
    q2 = [64, 0, 128, 64]
    q3 = [0, 64, 64, 128]
    q4 = [64, 64, 128, 128]

    quadrants = [q1, q2, q3, q4]
    for i, quadrant in enumerate(quadrants):
        if plan[i] == '1':
            draw.rectangle(quadrant, fill='#000000')


    return im


image_plans = [f'{i:04b}' for i in range(16)]

images = [make_image(plan) for plan in image_plans]

if __name__ == '__main__':
    for image in images:
        image.save(f'img/{image.filename}')
