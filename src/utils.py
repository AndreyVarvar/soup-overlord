import pygame as pg
from math import sin, cos, pi

from pygame.geometry import Circle



def average(iterable: list[int]):
    if len(iterable) == 0:
        return 0
    return sum(iterable)/len(iterable)


def draw_aa_arc(
        surface: pg.Surface, 
        color: pg.typing.ColorLike, 
        rect: pg.typing.RectLike, 
        start_angle: float, 
        end_angle: float, 
        width: int, 
        scale: int = 4
    ):
    x, y, w, h = pg.Rect(rect)
    
    temp_surf = pg.Surface((w * scale, h * scale), pg.SRCALPHA)
    
    scaled_rect = pg.Rect(0, 0, w * scale, h * scale)
    scaled_width = width * scale
    
    pg.draw.arc(temp_surf, color, scaled_rect, start_angle, end_angle, scaled_width)
    
    smooth_surf = pg.transform.smoothscale(temp_surf, (w, h))
    
    surface.blit(smooth_surf, (x, y))



def draw_pie_chart(
        surface: pg.Surface, 
        center: pg.typing.Point,
        radius: int,
        angles: list[float],
        colors: list[pg.typing.ColorLike],
        texts: list[str],
        clockwise: bool = True,
        chart_start_angle: float = 0.0
    ):

    pg.font.init()
    

    center = pg.Vector2(center)
    rect = pg.Rect(0, 0, 2*radius, 2*radius)
    rect.center = center

    arcs = list(zip(angles, colors, texts))
    if clockwise:
        arcs = arcs[::-1]

    circle = Circle(center.x, center.y, radius)

    text_rects = []

    accumulated_angle = chart_start_angle % (2*pi)
    for angle, color, text in arcs:
        start_angle = accumulated_angle
        stop_angle = accumulated_angle + angle

        accumulated_angle += angle
        accumulated_angle %= (2*pi)

        draw_aa_arc(surface, color, rect, start_angle, stop_angle, radius//2)

        font = pg.font.SysFont("arial", radius//10)  # font size is proportional to the radius
     
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_frect()
        displacement_vector = pg.Vector2(cos(accumulated_angle - angle/2), -sin(accumulated_angle - angle/2))
        text_rect.center = center + displacement_vector * radius * 1.2

        while circle.colliderect(text_rect) or any([text_rect.colliderect(r) for r in text_rects]):
            text_rect.center = pg.Vector2(text_rect.center) + displacement_vector

        text_rects.append(text_rect)

        surface.blit(text_surf, text_rect)

    pg.font.quit()
