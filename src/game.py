import pygame
import random
import sys
from config import *
from sprites import Snake, Food
from systems import (
    check_wall_collision,
    check_self_collision,
    check_snake_collision,
    check_food_collision,
    update_direction
)
#som de gameover
gameover = pygame.mixer.Sound('assets/gameover.wav')

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Configuração da tela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Multiplayer (até 4 jogadores) - Atari Style")
        self.clock = pygame.time.Clock()
        
        # Font para pontuação
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
        # Estado do jogo
        self.running = True
        self.game_started = False
        self.game_over = False
        self.winner = None
        self.num_players = 2  # Número padrão de jogadores
        
        # Lista de jogadores
        self.players = []
        
        # Mostrar tela de seleção
        self.show_player_selection()
    
    def show_player_selection(self):
        """Tela para selecionar o número de jogadores."""
        selecting = True
        
        while selecting:
            self.screen.fill(BLACK)
            
            # Título
            title_text = self.font.render("SNAKE MULTIPLAYER", True, GREEN)
            title_rect = title_text.get_rect()
            title_rect.centerx = WIDTH // 2
            title_rect.top = HEIGHT // 4
            self.screen.blit(title_text, title_rect)
            
            # Instruções
            instruction_text = self.small_font.render(
                "Selecione o número de jogadores (2-4):",
                True,
                WHITE
            )
            instruction_rect = instruction_text.get_rect()
            instruction_rect.centerx = WIDTH // 2
            instruction_rect.centery = HEIGHT // 2 - 50
            self.screen.blit(instruction_text, instruction_rect)
            
            # Opções
            options = [
                ("Pressione 2 para 2 jogadores", 2),
                ("Pressione 3 para 3 jogadores", 3),
                ("Pressione 4 para 4 jogadores", 4)
            ]
            
            for i, (text, num) in enumerate(options):
                color = YELLOW if num == self.num_players else WHITE
                option_text = self.small_font.render(text, True, color)
                option_rect = option_text.get_rect()
                option_rect.centerx = WIDTH // 2
                option_rect.centery = HEIGHT // 2 + 20 + (i * 50)
                self.screen.blit(option_text, option_rect)
            
            # Instruções de controles
            controls_y = HEIGHT // 2 + 200
            controls = [
                "P1: WASD | P2: Setas",
                "P3: IJKL | P4: TFGH",
                "Pressione ENTER para começar | ESC para sair"
            ]
            
            for i, control_text in enumerate(controls):
                control_render = self.tiny_font.render(control_text, True, CYAN)
                control_rect = control_render.get_rect()
                control_rect.centerx = WIDTH // 2
                control_rect.top = controls_y + (i * 30)
                self.screen.blit(control_render, control_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        self.num_players = 2
                    elif event.key == pygame.K_3:
                        self.num_players = 3
                    elif event.key == pygame.K_4:
                        self.num_players = 4
                    elif event.key == pygame.K_RETURN:
                        selecting = False
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def reset_game(self):
        """Reinicia o jogo com o número de jogadores selecionado."""
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        
        self.players = []
        
        # Configurações para cada jogador
        player_configs = [
            {
                'color': GREEN,
                'start_pos': (center_x - 15, center_y - 10),
                'direction': RIGHT,
                'keys': P1_KEYS,
                'name': 'P1'
            },
            {
                'color': BLUE,
                'start_pos': (center_x + 15, center_y + 10),
                'direction': LEFT,
                'keys': P2_KEYS,
                'name': 'P2'
            },
            {
                'color': YELLOW,
                'start_pos': (center_x - 15, center_y + 10),
                'direction': RIGHT,
                'keys': P3_KEYS,
                'name': 'P3'
            },
            {
                'color': MAGENTA,
                'start_pos': (center_x + 15, center_y - 10),
                'direction': LEFT,
                'keys': P4_KEYS,
                'name': 'P4'
            }
        ]
        
        # Criar apenas o número de jogadores selecionado
        for i in range(self.num_players):
            config = player_configs[i]
            snake = Snake(
                color=config['color'],
                start_pos=config['start_pos'],
                direction=config['direction']
            )
            snake.name = config['name']
            snake.keys = config['keys']
            self.players.append(snake)
        
        # Comida
        self.food = Food()
        self.food.respawn(self.players)
        
        self.game_started = True
        self.game_over = False
        self.winner = None
    
    def handle_events(self):
        """Processa eventos do pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Controles de cada jogador
                for player in self.players:
                    if event.key in player.keys:
                        update_direction(player, player.keys[event.key])
                
                # Reiniciar jogo
                if event.key == pygame.K_SPACE and self.game_over:
                    self.show_player_selection()
                
                # Sair do jogo
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Atualiza a lógica do jogo."""
        if self.game_over or not self.game_started:
            return
        
        # Mover as cobras
        for player in self.players:
            player.move()
        
        # Verificar colisões com paredes
        for player in self.players:
            check_wall_collision(player)
        
        # Verificar auto-colisão
        for player in self.players:
            check_self_collision(player)
        
        # Verificar colisão entre cobras
        for i, player1 in enumerate(self.players):
            for player2 in self.players[i+1:]:
                check_snake_collision(player1, player2)
        
        # Verificar colisão com comida
        for player in self.players:
            check_food_collision(player, self.food, self.players)
        
        # Verificar fim de jogo
        self.check_game_over()
    
    def check_game_over(self):
        """Verifica se o jogo acabou e determina o vencedor."""
        alive_players = [p for p in self.players if p.alive]
        
        # Jogo continua se mais de 1 jogador está vivo
        if len(alive_players) > 1:
            return
        
        self.game_over = True
        gameover.play()
        
        # Determinar vencedor
        if len(alive_players) == 1:
            self.winner = alive_players[0].name
        else:
            # Todos morreram, quem tem mais pontos vence
            max_score = max(p.score for p in self.players)
            winners = [p for p in self.players if p.score == max_score]
            
            if len(winners) == 1:
                self.winner = winners[0].name
            else:
                self.winner = "Empate entre " + ", ".join(w.name for w in winners)
    
    def draw(self):
        """Renderiza todos os elementos na tela."""
        if not self.game_started:
            return
        
        # Fundo preto (estilo Atari)
        self.screen.fill(BLACK)
        
        # Desenhar grid (opcional, para efeito Atari)
        self.draw_grid()
        
        # Desenhar comida
        self.food.draw(self.screen)
        
        # Desenhar cobras
        for player in self.players:
            player.draw(self.screen)
        
        # Desenhar HUD (pontuação)
        self.draw_hud()
        
        # Desenhar tela de game over
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_grid(self):
        """Desenha um grid sutil no fundo (estilo Atari)."""
        grid_color = (20, 20, 20)
        
        # Linhas verticais
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, HEIGHT))
        
        # Linhas horizontais
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, grid_color, (0, y), (WIDTH, y))
    
    def draw_hud(self):
        """Desenha a interface (pontuação e controles)."""
        # Layout da pontuação baseado no número de jogadores
        if self.num_players == 2:
            # P1 esquerda, P2 direita
            positions = [
                (20, 20, 'left'),  # P1
                (WIDTH - 20, 20, 'right')  # P2
            ]
        elif self.num_players == 3:
            # P1 esquerda, P2 centro, P3 direita
            positions = [
                (20, 20, 'left'),  # P1
                (WIDTH // 2, 20, 'center'),  # P2
                (WIDTH - 20, 20, 'right')  # P3
            ]
        else:  # 4 jogadores
            # P1 e P3 em cima, P2 e P4 embaixo
            positions = [
                (20, 20, 'left'),  # P1
                (WIDTH - 20, 20, 'right'),  # P2
                (20, 70, 'left'),  # P3
                (WIDTH - 20, 70, 'right')  # P4
            ]
        
        for i, player in enumerate(self.players):
            status = "✓" if player.alive else "✗"
            text = self.small_font.render(
                f"{player.name}: {player.score} {status}",
                True,
                player.color
            )
            
            x, y, align = positions[i]
            
            if align == 'left':
                text_rect = text.get_rect()
                text_rect.topleft = (x, y)
            elif align == 'right':
                text_rect = text.get_rect()
                text_rect.topright = (x, y)
            else:  # center
                text_rect = text.get_rect()
                text_rect.midtop = (x, y)
            
            self.screen.blit(text, text_rect)
        
        # Instruções (centro inferior)
        controls_text = self.tiny_font.render(
            "ESC: Sair | ESPAÇO: Menu",
            True,
            WHITE
        )
        controls_rect = controls_text.get_rect()
        controls_rect.centerx = WIDTH // 2
        controls_rect.bottom = HEIGHT - 10
        self.screen.blit(controls_text, controls_rect)
    
    def draw_game_over(self):
        """Desenha a tela de game over."""
        # Overlay semi-transparente
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título "GAME OVER"
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.centerx = WIDTH // 2
        game_over_rect.centery = HEIGHT // 2 - 120
        self.screen.blit(game_over_text, game_over_rect)
        
        # Vencedor
        if "Empate" in self.winner:
            winner_color = WHITE
            winner_msg = self.winner.upper()
        else:
            winner_player = next(p for p in self.players if p.name == self.winner)
            winner_color = winner_player.color
            winner_msg = f"{self.winner} VENCEU!"
        
        winner_text = self.font.render(winner_msg, True, winner_color)
        winner_rect = winner_text.get_rect()
        winner_rect.centerx = WIDTH // 2
        winner_rect.centery = HEIGHT // 2 - 40
        self.screen.blit(winner_text, winner_rect)
        
        # Placar final
        y_offset = HEIGHT // 2 + 40
        for player in sorted(self.players, key=lambda p: p.score, reverse=True):
            score_text = self.small_font.render(
                f"{player.name}: {player.score} pontos",
                True,
                player.color
            )
            score_rect = score_text.get_rect()
            score_rect.centerx = WIDTH // 2
            score_rect.top = y_offset
            self.screen.blit(score_text, score_rect)
            y_offset += 40
        
        # Instruções para reiniciar
        restart_text = self.small_font.render(
            "Pressione ESPAÇO para voltar ao menu",
            True,
            WHITE
        )
        restart_rect = restart_text.get_rect()
        restart_rect.centerx = WIDTH // 2
        restart_rect.bottom = HEIGHT - 60
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Loop principal do jogo."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
