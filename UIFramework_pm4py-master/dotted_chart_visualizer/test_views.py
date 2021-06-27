from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):

    def test_POST_attributes(self):
        '''Test in setting the attributes'''
        self.client = Client()
        self.dcv_url = reverse("dotted-chart-visualizer")
        response = self.client.post(
            self.dcv_url,
            {
                "log_name": "log.csv",
                "default_axis_list": "default_axis_list",
                "default_label_list": "default_label_list",
                "attribute_list": "log_attribute_list",
                "default_try": True,
                "log_level_attributes": "log_level_attributes",
                "case_level_attributes": "case_level_attributes",
                "default_axis_order": "default_axis_order",
                "sort_selection": "default;log"
            },
        )
        self.assertEqual(response.status_code, 200)
