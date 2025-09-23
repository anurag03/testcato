# Core logic for categorizing test results


class TestCategorizer:
    def __init__(self):
        pass

    def categorize(self, test_results):
        """
        Categorize test results into groups (e.g., passed, failed, skipped).
        :param test_results: List of test result dicts
        :return: Dict with categories as keys and lists of test names as values
        """
        categories = {"passed": [], "failed": [], "skipped": []}
        for result in test_results:
            status = result.get("status")
            name = result.get("name")
            if status in categories:
                categories[status].append(name)
        return categories
