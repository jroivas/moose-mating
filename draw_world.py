import Image, ImageDraw


class DrawWorld(object):
    def __init__(self, world, scale=1.0):
        self.world = world
        self.img = None
        self.scale = scale
        self.food_scale = scale * 0.5
        self.mooses = []
        self.flip_mooses = []
        self.food = None

        self.load_images()

    def load_images(self):
        self.mooses.append(Image.open('img/moose1.png'))
        self.mooses.append(Image.open('img/moose2.png'))
        self.mooses.append(Image.open('img/moose3.png'))
        self.mooses.append(Image.open('img/moose4.png'))
        self.food = Image.open('img/food.png')

        self.mooses = [x.resize((int(x.size[0] * self.scale), int(x.size[1] * self.scale))) for x in self.mooses]
        self.flip_mooses = [x.copy().transpose(Image.FLIP_LEFT_RIGHT) for x in self.mooses]
        self.food = self.food.resize((int(self.food.size[0] * self.food_scale), int(self.food.size[1] * self.food_scale)))

    def draw(self):
        self.img = Image.new('RGB', self.world.area)
        draw = ImageDraw.Draw(self.img)
        draw.rectangle([(0, 0), self.world.area], fill=(0, 100, 0))
        del draw

        for food in self.world.food:
            if not food.active:
                continue
            self.img.paste(self.food, (int(food.x), int(food.y)), self.food)

        for moose in self.world.animals:
            if not moose.item.alive:
                continue
            if moose.xspeed > 0:
                moo = self.flip_mooses[int(moose.item.shape, 2)]
            else:
                moo = self.mooses[int(moose.item.shape, 2)]
            self.img.paste(moo, (int(moose.x), int(moose.y)), moo)

    def save(self, name):
        self.img.save(name, 'PNG')

    def show(self):
        self.img.show()
