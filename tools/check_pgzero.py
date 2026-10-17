import pgzrun

# Проверка Pygame Zero: должно открыться окно с текстом. Закрой его.

WIDTH = 400
HEIGHT = 300
TITLE = "Проверка Pygame Zero"


def draw():
    screen.fill((30, 30, 60))
    screen.draw.text(
        "Pygame Zero работает!\nЗакрой окно",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize=36,
        color="white",
    )


pgzrun.go()
