from django.test import TestCase
from apps.workstatus.models import Workstatus
from apps.work.models import Work
from apps.order.models import Order
from apps.workstatus.models.consts import WorkStatusChoice


class WorkstatusModelTest(TestCase):
    def setUp(self):
        self.work = Work.objects.create(
            name="Замена масла",
            price=2000,
            description="Полная замена моторного масла"
        )
        self.order = Order.objects.create()

        self.workstatus_data = {
            'work': self.work,
            'order': self.order,
            'status': WorkStatusChoice.in_progress,
            'amount': 2,
            'fix_price': 2500
        }

    def test_workstatus_creation(self):
        """Тест создания объекта Workstatus"""
        ws = Workstatus.objects.create(**self.workstatus_data)

        self.assertEqual(ws.work, self.work)
        self.assertEqual(ws.order, self.order)
        self.assertEqual(ws.status, WorkStatusChoice.in_progress)
        self.assertEqual(ws.amount, 2)
        self.assertEqual(ws.fix_price, 2500)
        self.assertEqual(str(ws), "Замена масла x2")

    def test_relations(self):
        ws = Workstatus.objects.create(**self.workstatus_data)

        self.assertIn(ws, self.work.work_name.all())

        self.assertIn(ws, self.order.items.all())
