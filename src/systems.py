from config import GRID_WIDTH, GRID_HEIGHT


def check_wall_collision(snake):
    """Verifica se a cobra colidiu com as paredes."""
    if not snake.alive:
        return
    
    head_x, head_y = snake.body[0]
    
    if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
        snake.alive = False


def check_self_collision(snake):
    """Verifica se a cobra colidiu consigo mesma."""
    if not snake.alive:
        return
    
    head = snake.body[0]
    
    if head in snake.body[1:]:
        snake.alive = False


def check_snake_collision(snake1, snake2):
    """Verifica colisão entre duas cobras."""
    if not snake1.alive or not snake2.alive:
        return
    
    head1 = snake1.body[0]
    head2 = snake2.body[0]
    
    # Cobra 1 colide com o corpo da cobra 2
    if head1 in snake2.body:
        snake1.alive = False
    
    # Cobra 2 colide com o corpo da cobra 1
    if head2 in snake1.body:
        snake2.alive = False
    
    # Colisão frontal (cabeças colidem)
    if head1 == head2:
        snake1.alive = False
        snake2.alive = False


def check_food_collision(snake, food, all_snakes):
    """Verifica se a cobra comeu a comida."""
    if not snake.alive:
        return
    
    if snake.body[0] == food.position:
        snake.eat()
        food.respawn(all_snakes)


def update_direction(snake, new_direction):
    """Atualiza a direção da cobra, evitando que ela vire 180 graus."""
    current_dir_x, current_dir_y = snake.direction
    new_dir_x, new_dir_y = new_direction
    
    # Não permite virar 180 graus
    if (current_dir_x + new_dir_x, current_dir_y + new_dir_y) != (0, 0):
        snake.direction = new_direction
