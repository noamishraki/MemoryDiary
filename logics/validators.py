from typing import List
from datetime import datetime

from errors import DateBeforeDataDates


def validate_range(dates: List, smallest_date: datetime.date):
    """
     Validate that all dates in the list are after the specified smallest_date.

     Parameters:
         dates (List[datetime.date]): A list of datetime.date objects to be validated - dates of the treatment.
         smallest_date (datetime.date): The reference date to compare against.

     Raises:
         DateBeforeDataDates: If any date in the 'dates' list is not after 'smallest_date'.

     Returns:
         None: This function does not return anything. It raises an exception if the validation fails.
     """
    if not all(date > smallest_date for date in dates):
        raise DateBeforeDataDates
