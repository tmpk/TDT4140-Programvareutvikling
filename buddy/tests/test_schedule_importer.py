from django.test import TestCase
from ..common import schedule_importer
import codecs


class ScheduleImporterTestCase(TestCase):
    def test_extracts_course_code_from_line(self):
        description_line = 'DESCRIPTION:Forelesning - Teknologiledelse (TIØ4258)'
        course_code = schedule_importer.extract_course_code_from_description_line(description_line)
        self.assertEqual(course_code, 'TIØ4258')

    def test_extracts_course_code_from_lines(self):
        description_lines = {   'DESCRIPTION:Forelesning - Teknologiledelse (TIØ4258)',
                                'DESCRIPTION:Forelesning - Datamodellering og databasesystemer (TDT4145)',
                                'DESCRIPTION:Øving - Programvarearkitektur (TDT4240)',
                                'DESCRIPTION:Øving - Datamodellering og databasesystemer (TDT4145)',
                                }
        course_codes = list(set(schedule_importer.extract_course_code_from_description_lines(description_lines)))
        expected = ['TIØ4258', 'TDT4145', 'TDT4240']
        # Sort to ease comparison
        course_codes.sort()
        expected.sort()
        self.assertEqual(course_codes, expected)
