class StatusError(Exception):
    """Статус ответа не равен 200."""

    pass


class EmptyListError(Exception):
    """Список пуст."""

    pass


class NonExistendStatusError(Exception):
    """Несуществующий статус Домашней работы."""

    pass
