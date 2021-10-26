class InvalidImageBinaryError(Exception):
    def __init__(self):
        super().__init__('Binário de imagem inválido.')


class InvalidImageExtensionError(Exception):
    def __init__(self):
        super().__init__('Extensão de imagem inválida.')


class InvalidImageForTrainingError(Exception):
    def __init__(self):
        super().__init__('Imagem inválida para treinamento.')


class RepeatedImageError(Exception):
    def __init__(self):
        super().__init__('Imagem repetida.')
