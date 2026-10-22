"""Custom exceptions for the Student Grade Analytics Tool.

File-level errors are fatal and are caught in main.py.
InvalidRecordError is row-level: callers skip the row and log a warning.
"""


class GradeAnalyticsError(Exception):
    """Base class for every error raised by this tool."""


class CSVNotFoundError(GradeAnalyticsError):
    """The CSV file does not exist."""


class CSVAccessError(GradeAnalyticsError):
    """The CSV file exists but cannot be read (permissions, or it is a folder)."""


class EmptyCSVError(GradeAnalyticsError):
    """The CSV file has no header or no data rows."""


class InvalidHeaderError(GradeAnalyticsError):
    """Required columns are missing, or no valid sN_COURSE columns were found."""


class InvalidRecordError(GradeAnalyticsError):
    """One row is invalid. The caller skips the row and logs a warning."""

    def __init__(self, row_number: int, reason: str) -> None:
        self.row_number = row_number
        self.reason = reason
        super().__init__(f"Row {row_number}: {reason}")


class NoValidRecordsError(GradeAnalyticsError):
    """Every row was invalid, so there is nothing to analyze."""


class ReportWriteError(GradeAnalyticsError):
    """The JSON report could not be written."""
