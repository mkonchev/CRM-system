from django.test import TestCase
from apps.workstatus.models import Workstatus
from apps.work.models import Work
from apps.order.models import Order
from apps.workstatus.models.consts import WorkStatusChoice
from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer


class WorkstatusSerializerlTest(TestCase):
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
        self.workstatus = Workstatus.objects.create(**self.workstatus_data)
        self.serializer = WorkstatusSerializer(instance=self.workstatus)

    def test_workstatus_serialization(self):
        self.assertEqual(self.serializer.data['work'],
                         self.workstatus_data['work'].pk)
        self.assertEqual(self.serializer.data['order'],
                         self.workstatus_data['order'].pk)
        self.assertEqual(self.serializer.data['status'],
                         self.workstatus_data['status']),
        self.assertEqual(self.serializer.data['amount'],
                         self.workstatus_data['amount']),
        self.assertEqual(self.serializer.data['fix_price'],
                         self.workstatus_data['fix_price'])

    def test_workstatus_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['work'], self.work.pk)
        self.assertEqual(data['order'], self.order.pk)
        self.assertEqual(data['status'], WorkStatusChoice.in_progress)
        self.assertEqual(data['amount'], 2)
        self.assertEqual(data['fix_price'], 2500)

    def test_create_serializer(self):
        new_workstatus_data = {
            'work': self.work.pk,
            'order': self.order.pk,
            'status': WorkStatusChoice.in_progress,
            'amount': 2,
            'fix_price': 2500
        }
        serializer = WorkstatusSerializer(data=new_workstatus_data)
        self.assertTrue(serializer.is_valid())
        workstatus = serializer.save()
        self.assertEqual(workstatus.work, self.work)

    def test_update_serializer(self):
        update_data = {'status': WorkStatusChoice.done}
        serializer = WorkstatusSerializer(instance=self.workstatus,
                                          data=update_data,
                                          partial=True)
        self.assertTrue(serializer.is_valid())
        workstatus = serializer.save()
        self.assertEqual(workstatus.status, WorkStatusChoice.done)
