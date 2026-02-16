class DomainError(Exception):
    pass

class TaskNotFound(DomainError):
    def __init__(self, task_id: int | None = None):
        message = "Task nao encontrada"
        if task_id is not None:
            message += f"(id:{task_id})"

        super().__init__(message)


class NotAuthorized(DomainError):
    def __init__(self, message="Acao nao autorizada"):
        self.message = message
        super().__init__(self.message)


class BadRequest(DomainError):
    def __init__(self, message="Requisicao invalida"):
        self.message = message
        super().__init__(self.message)


class AlreadyExistError(DomainError):
    def __init__(self, message="Objeto ja existente"):
        self.message = message
        super().__init__(self.message)
