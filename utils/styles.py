

class ModernStyles:
    """Estilos modernos para a aplicação."""
    
    # Paleta de cores moderna
    COLORS = {
        # Cores primárias
        'primary': '#3B82F6',      # Azul moderno
        'primary_hover': "#444D62",
        'primary_light': '#DBEAFE',
        
        # Cores secundárias  
        'secondary': '#6366F1',     # Índigo
        'secondary_hover': '#4F46E5',
        
        # Cores de sucesso
        'success': '#10B981',       # Verde esmeralda
        'success_hover': '#059669',
        'success_light': '#D1FAE5',
        
        # Cores de aviso
        'warning': '#F59E0B',       # Âmbar
        'warning_hover': '#D97706',
        'warning_light': '#FEF3C7',
        
        # Cores de erro
        'danger': '#EF4444',        # Vermelho moderno
        'danger_hover': '#DC2626',
        'danger_light': '#FEE2E2',
        
        # Cores neutras
        'gray_50': '#F9FAFB',
        'gray_100': '#F3F4F6',
        'gray_200': '#E5E7EB',
        'gray_300': '#D1D5DB',
        'gray_400': '#9CA3AF',
        'gray_500': '#6B7280',
        'gray_600': '#4B5563',
        'gray_700': '#374151',
        'gray_800': '#1F2937',
        'gray_900': '#111827',
        
        # Cores de fundo
        'background': '#FFFFFF',
        'background_alt': '#F8FAFC',
        'card_bg': '#FFFFFF',
        
        # Texto
        'text_primary': '#1F2937',
        'text_secondary': '#6B7280',
        'text_muted': '#9CA3AF',
    }
    
    @staticmethod
    def get_button_style(color_type='primary', size='medium'):
        """Gera estilo de botão moderno."""
        colors = ModernStyles.COLORS
        
        color_map = {
            'primary': (colors['primary'], colors['primary_hover']),
            'success': (colors['success'], colors['success_hover']),
            'warning': (colors['warning'], colors['warning_hover']),
            'danger': (colors['danger'], colors['danger_hover']),
            'secondary': (colors['secondary'], colors['secondary_hover']),
        }
        
        size_map = {
            'small': ('8px 12px', '12px'),
            'medium': ('10px 16px', '14px'),
            'large': ('12px 20px', '16px'),
        }
        
        bg_color, hover_color = color_map.get(color_type, color_map['primary'])
        padding, font_size = size_map.get(size, size_map['medium'])
        
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: {padding};
                font-size: {font_size};
                font-weight: 600;
                transition: all 0.2s ease;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                transform: translateY(0px);
                background-color: {hover_color};
            }}
            QPushButton:disabled {{
                background-color: {colors['gray_300']};
                color: {colors['gray_500']};
            }}
        """
    
    @staticmethod
    def get_card_style(elevated=True):
        """Gera estilo de card moderno."""
        colors = ModernStyles.COLORS
        shadow = "box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);" if elevated else ""
        
        return f"""
            QFrame {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['gray_200']};
                border-radius: 12px;
                padding: 20px;
                {shadow}
            }}
        """
    
    @staticmethod
    def get_table_style():
        """Gera estilo de tabela moderno."""
        colors = ModernStyles.COLORS
        
        return f"""
            QTableWidget {{
                gridline-color: {colors['gray_200']};
                background-color: {colors['background']};
                alternate-background-color: {colors['gray_50']};
                color: {colors['text_primary']};
                border: 1px solid {colors['gray_200']};
                border-radius: 8px;
                selection-background-color: {colors['primary_light']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {colors['gray_700']}, stop:1 {colors['gray_800']});
                color: white;
                padding: 12px;
                font-weight: 600;
                border: none;
                border-right: 1px solid {colors['gray_600']};
            }}
            QHeaderView::section:first {{
                border-left: none;
                border-top-left-radius: 8px;
            }}
            QHeaderView::section:last {{
                border-right: none;
                border-top-right-radius: 8px;
            }}
            QTableWidget::item {{
                padding: 12px 8px;
                border-bottom: 1px solid {colors['gray_200']};
            }}
            QTableWidget::item:hover {{
                background-color: {colors['primary_light']};
            }}
            QTableWidget::item:selected {{
                background-color: {colors['primary']};
                color: white;
            }}
        """
    
    @staticmethod
    def get_combo_style():
        """Gera estilo de combobox moderno."""
        colors = ModernStyles.COLORS
        
        return f"""
            QComboBox {{
                background-color: {colors['background']};
                border: 2px solid {colors['gray_300']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: {colors['text_primary']};
                min-width: 200px;
            }}
            QComboBox:hover {{
                border-color: {colors['primary']};
            }}
            QComboBox:focus {{
                border-color: {colors['primary']};
                outline: none;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
                width: 12px;
                height: 12px;
                background-color: {colors['gray_500']};
            }}
            QComboBox QAbstractItemView {{
                background-color: {colors['background']};
                border: 1px solid {colors['gray_300']};
                border-radius: 4px;
                selection-background-color: {colors['primary_light']};
                outline: none;
            }}
        """
    
    @staticmethod
    def get_stats_card_style(color_type='primary'):
        """Gera estilo de card de estatísticas."""
        colors = ModernStyles.COLORS
        
        color_map = {
            'primary': colors['primary'],
            'success': colors['success'], 
            'warning': colors['warning'],
            'danger': colors['danger'],
        }
        
        accent_color = color_map.get(color_type, colors['primary'])
        
        return f"""
            QFrame {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['gray_200']};
                border-left: 4px solid {accent_color};
                border-radius: 8px;
                padding: 16px;
                margin: 4px;
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
        """