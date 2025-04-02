from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from content.models import Chapter, Section, Subsection, QA

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create users if they don't exist
        if not User.objects.filter(username="editor").exists():
            editor = User.objects.create_user(
                username="editor",
                email="editor@example.com",
                password="password123",
                first_name="Петр",
                last_name="Петров",
                role=User.EDITOR,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created editor user: {editor.username}")
            )

        if not User.objects.filter(username="moderator").exists():
            moderator = User.objects.create_user(
                username="moderator",
                email="moderator@example.com",
                password="password123",
                first_name="Иван",
                last_name="Иванов",
                role=User.MODERATOR,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created moderator user: {moderator.username}")
            )

        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_user(
                username="admin",
                email="admin@example.com",
                password="password123",
                first_name="Александр",
                last_name="Александров",
                role=User.ADMIN,
                is_staff=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created admin user: {admin.username}")
            )

        # Create chapters
        chapters_data = [
            {
                "title": "Глава 1",
                "description": "Введение в законодательство",
                "order": 1,
            },
            {"title": "Глава 2", "description": "Гражданское право", "order": 2},
            {"title": "Глава 3", "description": "Уголовное право", "order": 3},
            {"title": "Глава 4", "description": "Административное право", "order": 4},
            {"title": "Глава 5", "description": "Трудовое право", "order": 5},
            {"title": "Глава 6", "description": "Семейное право", "order": 6},
            {"title": "Глава 7", "description": "Налоговое право", "order": 7},
            {"title": "Глава 8", "description": "Земельное право", "order": 8},
            {"title": "Глава 9", "description": "Жилищное право", "order": 9},
            {"title": "Глава 10", "description": "Процессуальное право", "order": 10},
        ]

        chapters = []
        for chapter_data in chapters_data:
            chapter, created = Chapter.objects.get_or_create(
                title=chapter_data["title"],
                defaults={
                    "description": chapter_data["description"],
                    "order": chapter_data["order"],
                },
            )
            chapters.append(chapter)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created chapter: {chapter.title}")
                )

        # Create sections for Chapter 1
        sections_data = [
            {
                "title": "Раздел 1.1",
                "description": "Основы законодательства",
                "order": 1,
                "chapter": chapters[0],
            },
            {
                "title": "Раздел 1.2",
                "description": "Конституционное право",
                "order": 2,
                "chapter": chapters[0],
            },
            {
                "title": "Раздел 1.3",
                "description": "Международное право",
                "order": 3,
                "chapter": chapters[0],
            },
            {
                "title": "Раздел 1.4",
                "description": "Нормативные акты",
                "order": 4,
                "chapter": chapters[0],
            },
            {
                "title": "Раздел 1.5",
                "description": "Правовая система РФ",
                "order": 5,
                "chapter": chapters[0],
            },
            {
                "title": "Раздел 1.6",
                "description": "Судебная система",
                "order": 6,
                "chapter": chapters[0],
            },
        ]

        sections = []
        for section_data in sections_data:
            section, created = Section.objects.get_or_create(
                title=section_data["title"],
                defaults={
                    "description": section_data["description"],
                    "order": section_data["order"],
                },
            )
            section.chapters.add(section_data["chapter"])
            sections.append(section)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created section: {section.title}")
                )

        # Create subsections for Section 1.1
        subsections_data = [
            {
                "title": "Подраздел 1.1.1",
                "description": "Структура законодательства",
                "order": 1,
                "section": sections[0],
            },
            {
                "title": "Подраздел 1.1.2",
                "description": "Принципы права",
                "order": 2,
                "section": sections[0],
            },
            {
                "title": "Подраздел 1.1.3",
                "description": "Правовые нормы",
                "order": 3,
                "section": sections[0],
            },
            {
                "title": "Подраздел 1.1.4",
                "description": "Источники права",
                "order": 4,
                "section": sections[0],
            },
            {
                "title": "Подраздел 1.1.5",
                "description": "Правоотношения",
                "order": 5,
                "section": sections[0],
            },
        ]

        subsections = []
        for subsection_data in subsections_data:
            subsection, created = Subsection.objects.get_or_create(
                title=subsection_data["title"],
                defaults={
                    "description": subsection_data["description"],
                    "order": subsection_data["order"],
                },
            )
            subsection.sections.add(subsection_data["section"])
            subsections.append(subsection)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created subsection: {subsection.title}")
                )

        # Create QA items for Subsection 1.1.1
        qa_items_data = [
            {
                "title": "Что такое законодательство?",
                "question_content": "Что такое законодательство и как оно структурировано в РФ?",
                "answer_content": "Законодательство - это совокупность законов и иных нормативных правовых актов. В РФ законодательство имеет иерархическую структуру: Конституция РФ, федеральные конституционные законы, федеральные законы, подзаконные акты.",
                "subsection": subsections[0],
                "created_by": admin,
                "status": QA.STATUS_PUBLISHED,
                "is_published": True,
            },
            {
                "title": "Как принимаются законы?",
                "question_content": "Каков процесс принятия законов в Российской Федерации?",
                "answer_content": "Законы в РФ принимаются Государственной Думой, одобряются Советом Федерации и подписываются Президентом. Процесс включает несколько чтений, обсуждений и возможных поправок.",
                "subsection": subsections[0],
                "created_by": editor,
                "status": QA.STATUS_PUBLISHED,
                "is_published": True,
            },
            {
                "title": "Что такое кодекс?",
                "question_content": "Что такое кодекс и какие основные кодексы существуют в РФ?",
                "answer_content": "Кодекс - это систематизированный законодательный акт, регулирующий определенную отрасль права. Основные кодексы в РФ: Гражданский, Уголовный, Трудовой, Семейный, Налоговый, Жилищный, Земельный, Административный и др.",
                "subsection": subsections[0],
                "created_by": moderator,
                "status": QA.STATUS_IN_REVIEW,
                "is_published": False,
            },
        ]

        for qa_data in qa_items_data:
            qa, created = QA.objects.get_or_create(
                title=qa_data["title"],
                defaults={
                    "question_content": qa_data["question_content"],
                    "answer_content": qa_data["answer_content"],
                    "created_by": qa_data["created_by"],
                    "status": qa_data["status"],
                    "is_published": qa_data["is_published"],
                },
            )
            qa.subsections.add(qa_data["subsection"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created QA: {qa.title}"))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
