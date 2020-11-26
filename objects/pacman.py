import pygame as pg
from misc import CELL_SIZE, get_image_path_for_animator, Health, Animator
from objects import Character


class Pacman(Character):
    action = {
        pg.K_w: 'up',
        pg.K_a: 'left',
        pg.K_s: 'down',
        pg.K_d: 'right'
    }

    def __init__(self, game, start_pos: tuple):
        self.__hp = Health(3, 3)
        self.__walk_anim = Animator(
            get_image_path_for_animator('pacman', 'walk')
        )
        self.__dead_anim = Animator(
            get_image_path_for_animator('pacman', 'dead'), 100, False, True
        )
        super().__init__(game, self.__walk_anim, start_pos)
        self.dead = False
        self.__feature_rotate = "none"

    @property
    def hp(self):
        return self.__hp.lives

    def process_event(self, event):
        if event.type == pg.KEYDOWN and event.key in self.action.keys() and not self.dead:
            self.go()
            self.__feature_rotate = self.action[event.key]

    def process_logic(self):
        self.animator.timer_check()
        if not self.dead:
            if self.in_center():
                if self.move_to(self.rotate):
                    self.go()
                else:
                    self.stop()
                    self.animator.change_cur_image(0)
                c = self.direction[self.__feature_rotate][2]
                if self.move_to(c):
                    self.set_direction(self.__feature_rotate)
            super().process_logic()

    def get_cell(self):
        return (self.rect.centerx // CELL_SIZE, (self.rect.centery-17) // CELL_SIZE)

    def death(self):
        self.__hp.change_count_lives(-1)
        self.animator = self.__dead_anim
        self.animator.run = True
        self.dead = True

    def reset(self):
        self.animator = self.__walk_anim
        self.__dead_anim.reset()
        self.move(*self.start_pos)
        self.speed = 0
        self.shift_x, self.shift_y = self.direction["right"][:2]
        self.animator.stop()
        self.animator.change_cur_image(0)
        self.dead = False

    def in_center(self) -> bool:
        return self.rect.x % CELL_SIZE == 6 and (self.rect.y-20) % CELL_SIZE == 6
