"""
Acceptance tests for grade settings in Studio.
"""
from common.test.acceptance.pages.studio.settings_graders import GradingPage
from common.test.acceptance.tests.studio.base_studio_test import StudioCourseTest
from common.test.acceptance.fixtures.course import XBlockFixtureDesc


class GradingPageTest(StudioCourseTest):
    """
    Bockchoy tests to add/edit grade settings in studio.
    """

    url = None

    def setUp(self):
        super(GradingPageTest, self).setUp()
        self.grading_page = GradingPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )

        self.grading_page.visit()

    def populate_course_fixture(self, course_fixture):
        """
        Return a test course fixture.
        """
        course_fixture.add_children(
            XBlockFixtureDesc("chapter", "Test Section").add_children(
                XBlockFixtureDesc("sequential", "Test Subsection").add_children(
                )
            )
        )

    def test_add_grade_range(self):
        """
        Scenario: Users can add grading ranges
            Given I have opened a new course in Studio
            And I am viewing the grading settings
            When I add "1" new grade
            Then I see I now have "3"
        """
        self.grading_page.add_grades(1)
        self.grading_page.save()
        self.grading_page.refresh_and_wait_for_load()
        total_number_of_grades = self.grading_page.get_total_number_of_grades()
        self.assertEqual(total_number_of_grades, 3)

    def test_staff_can_add_up_to_five_grades_only(self):
        """
        Scenario: Users can only have up to 5 grading ranges
            Given I have opened a new course in Studio
            And I am viewing the grading settings
            When I try to add more than 5 grades
            Then I see I have only "5" grades
        """
        self.grading_page.add_grades(6)
        self.grading_page.save()
        self.grading_page.refresh_and_wait_for_load()
        total_number_of_grades = self.grading_page.get_total_number_of_grades()
        self.assertEqual(total_number_of_grades, 5)

    def test_grades_remain_consistent(self):
        """
        Scenario: When user removes a grade the remaining grades should be consistent
            Given I have opened a new course in Studio
            And I am viewing the grading settings
            When I add "2" new grade
            Then Grade list has "A,B,C,F" grades
            And I delete a grade
            Then Grade list has "A,B,F" grades
        """
        self.grading_page.add_grades(2)
        self.grading_page.save()
        grades_alphabets = self.grading_page.get_grade_alphabets()
        self.assertEqual(grades_alphabets, ['A', 'B', 'C', 'F'])
        self.grading_page.remove_grades(1)
        self.grading_page.save()
        grades_alphabets = self.grading_page.get_grade_alphabets()
        self.assertEqual(grades_alphabets, ['A', 'B', 'F'])
