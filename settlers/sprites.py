import Image, ImageDraw

def generate_settlement_sprite(width, height, color):
    points = [
        (0, height),
        (0, height / 2),
        (width/2, 0),
        (width, height / 2),
        (width, height)
    ]
    settle_sprite = Image.new('RGBA', (width, height), None)
    draw = ImageDraw.Draw(settle_sprite)
    draw.polygon(points, fill=color, outline=(0,0,0) )
    del draw
    return settle_sprite
    
generate_settlement_sprite(200,200,(123, 64, 201)).show()