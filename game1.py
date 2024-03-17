import pygame


pygame.init()
screen = pygame.display.set_mode((590, 290))
pygame.display.set_caption("Idle run")
icon = pygame.image.load('images/icon.jpg')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
ghost = pygame.image.load("images/ghost.png").convert_alpha()
ghost_x = 600
walk_left = [
    pygame.image.load('images/player4left.png').convert_alpha(),
    pygame.image.load('images/player4leftv2.png').convert_alpha(),
    pygame.image.load('images/player4leftv3.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/player4right.png').convert_alpha(),
    pygame.image.load('images/player4rightv2.png').convert_alpha(),
    pygame.image.load('images/player4rightv3.png').convert_alpha(),
]

player_anim_count = 0
ghost_collision_count = 0
bg_x = 0
bg_sound = pygame.mixer.Sound("images/bg_sound.mp3")
bg_sound.play()
jump_sound = pygame.mixer.Sound("images/jump.mp3")
death_sound = pygame.mixer.Sound("images/death.mp3")
player_speed = 7
player_x =  150
player_y = 70
is_jump = False
frame_count = 0
jump_count = 7
coin_list = []
score = 0
myfont =  pygame.font.Font('images/txt.ttf', 70)
myfont2 = pygame.font.Font('images/txt.ttf', 50)
text_surface = myfont.render('You lose',False,'Red')
text_restart = myfont2.render('Try again',False,'Red',)
text_restart_rect = text_restart.get_rect(topleft=(215,180))
bg = pygame.image.load('images/56.jpg').convert_alpha()
running = True


player_masks = [pygame.mask.from_surface(img) for img in walk_left + walk_right]
ghost_mask = pygame.mask.from_surface(ghost)
el_mask = pygame.mask.from_surface(ghost)
ghost_timer = pygame.USEREVENT + 1
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ghost_timer, 2500)
pygame.time.set_timer(coin_timer, 3000)
ghost_list_ingame = []
gameplay = True

while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 580, 0))
    screen.blit(ghost, (ghost_x, 160))



    if gameplay:
        keys = pygame.key.get_pressed()
        player_mask = player_masks[player_anim_count // 2 if not keys[pygame.K_LEFT] else player_anim_count]
        player_rect = pygame.Rect(player_x, player_y, player_mask.get_size()[0], player_mask.get_size()[1])
        
        for (i, el) in enumerate(ghost_list_ingame):
            el_rect = pygame.Rect(el.x, 160, ghost_mask.get_size()[0], ghost_mask.get_size()[1])
            el_mask = pygame.mask.from_surface(ghost)
            screen.blit(ghost, el)
            el.x -= 10
            if el.x < -10:
                ghost_list_ingame.pop(i)

            offset = (el_rect.x - player_rect.x, el_rect.y - player_rect.y)
            if player_mask.overlap(el_mask, offset):
                ghost_collision_count += 1
                death_sound.play()
                if ghost_collision_count >= len(ghost_list_ingame):  
                    gameplay = False
            else:
                score +=1
        if keys[pygame.K_LEFT]:
            if frame_count % 6 == 0:  
                screen.blit(walk_left[player_anim_count], (player_x, player_y))
            else:
                screen.blit(walk_left[player_anim_count // 2], (player_x, player_y))
        else:
            if frame_count % 6 == 0:
                screen.blit(walk_right[player_anim_count], (player_x, player_y))
            else:
                screen.blit(walk_right[player_anim_count // 2], (player_x, player_y))
    
        if keys[pygame.K_LEFT] and player_x > 15:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 500:
            player_x += player_speed
        
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
                jump_sound.play()
        else:
            if jump_count >= -7:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 7
            
        if player_anim_count == 2:
            player_anim_count = 0
        else:
            player_anim_count += 1

        

        bg_x -= 3
        ghost_x -= 10
        

        
        if bg_x == -618:
            bg_x = 0
    
    else:
        screen.fill((87, 88, 89))
        bg_sound.stop()
        screen.blit(text_surface, (200, 80))
        screen.blit(text_restart, (215, 180))
        mouse = pygame.mouse.get_pos()
        if text_restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150  
            ghost_list_ingame.clear()
            bg_sound.play()
            score = 0
    score_text = myfont2.render("Score:"+str(score),False,"White")
    screen.blit(score_text,(10,10))
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_ingame.append(ghost.get_rect(topleft=(600, 160)))
         
    clock.tick(20)

