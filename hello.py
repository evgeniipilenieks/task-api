class Task:
    def __init__(self, title, status, priority):
        self.title = title
        self.status = status
        self.priority = priority
    
    def get_message(self):
        if self.status == "closed":
            return f"Пропущено: {self.title}"
        elif self.priority == "high":
            return f"[{self.priority}] {self.title} — {self.status} ⚠️"
        else:
            return f"[{self.priority}] {self.title} — {self.status}"            

tasks = [
    Task("Обработать письмо", "new", "high"),
    Task("Обновить отчёт", "in_progress", "low"),
    Task("Создать тикет", "new", "high"),
    Task("Проверить файлы", "closed", "medium")
]

for task in tasks:
    print(task.get_message())