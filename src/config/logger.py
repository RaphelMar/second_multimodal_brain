import logging
import sys

def setup_logger(name='video_brain', level=logging.INFO):
    """
    Configura e retorna um logger padronizado para o projeto.

    Args:
        name (str): Nome do logger. Padrão é 'video_brain'.
        level (int): Nível de log. Padrão é logging.INFO.

    Returns:
        logging.Logger: Logger configurado.
    """
    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita a duplicação de handlers se o logger já existir
    if not logger.handlers:
        # Cria um handler que imprime no console
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Cria um formato para os logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        # Adiciona o handler ao logger
        logger.addHandler(handler)

    return logger

# Cria uma instância padrão do logger
logger = setup_logger()