import pygame
from settings import *

class Upgrade: 
    """The upgrade menu (key M): choose a stat with the arrows and spend XP on it with Space."""
    def __init__(self, player):

        # general setups 
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.stat_count = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # items dimensions menu 
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # selection systems ==> index that increases as menu changed 
        self.selection_index = 0 
        self.selection_time = None 
        self.can_move = True 


    def input (self):
        """Left and right arrows move the selection; Space upgrades the selected stat."""
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys [pygame.K_RIGHT] and self.selection_index < self.stat_count -1 :
                self.selection_index += 1 
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1 :
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.items_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        """Allow input again a short time (MENU_INPUT_COOLDOWN) after the last key press, so one press moves one step."""
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= MENU_INPUT_COOLDOWN:
                self.can_move = True 

    def create_items(self):
        """Create one menu card per player stat, spread evenly across the screen."""
        self.items_list = []

        for item, index in enumerate(range(self.stat_count)):
            #horizontal (1280 )
            full_width = self.display_surface.get_size()[0]
            increment  = full_width // self.stat_count 
            left = (item * increment) + (increment - self.width) // 2

            #vertical pos (720)
            top = self.display_surface.get_size()[1] * 0.1 # y 10% at the top to create a good offset 
             
            # create the object
            item = Item(left,top, self.width, self.height, index, self.font) 
            self.items_list.append(item)      

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.items_list):

            #get attributes 
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
        
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

class Item:
    """One card of the upgrade menu, for one stat."""
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index 
        self.font = font 

    def display_names( self, surface, name, cost, selected):

        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title 
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect( midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        # cost 
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        """Draw the stat's level as a marker on a vertical line."""

        # drawing setup 
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        #bar setup 
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height #turns this into pixels
        value_rect = pygame.Rect(top[0] - 15 ,bottom[1] - relative_number,30,10)

        # drawing elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """Spend XP to raise the selected stat, never above its maximum."""
        stat_name = list(player.stats.keys())[self.index]
        cost = player.upgrade_cost[stat_name]
        max_value = player.max_stats[stat_name]

        has_enough_exp = player.exp >= cost
        is_below_max = player.stats[stat_name] < max_value
        if has_enough_exp and is_below_max:
            player.exp -= cost
            player.stats[stat_name] = min(player.stats[stat_name] * UPGRADE_STAT_FACTOR, max_value)
            player.upgrade_cost[stat_name] *= UPGRADE_COST_FACTOR

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)


        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)