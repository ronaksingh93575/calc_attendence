import math


class AttendanceCalculator:

    @staticmethod
    def estimate_classes(working_days, classes_per_5_days):
        """
        Estimate total classes in the selected month.
        """
        return round((working_days * classes_per_5_days) / 5)

    @staticmethod
    def required_classes(total_classes):
        """
        Minimum classes required for 75%.
        """
        return math.ceil(total_classes * 0.75)

    @staticmethod
    def calculate_subject(working_days, classes_per_5_days):

        total = AttendanceCalculator.estimate_classes(
            working_days,
            classes_per_5_days
        )

        required = AttendanceCalculator.required_classes(total)

        return total, required

    @staticmethod
    def calculate_overall(total_classes):

        return math.ceil(total_classes * 0.75)