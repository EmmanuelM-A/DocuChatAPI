"""
This module defines custom exceptions for the API.
"""

from typing import Optional

from fastapi import HTTPException, status

from src.utils.api_responses import ErrorDetail, ErrorResponse


class ApiException(HTTPException):
    """
    Custom base error class for API errors/exceptions, providing a
    structured error response.

    Inherits from HTTPException.
    """

    def __init__(
        self,
        error_detail: ErrorDetail,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred.",
    ):
        """
        Initializes the ApiError.

        Args:
            error_detail: An instance of ErrorDetail providing specific error
            information.
            status_code: The HTTP status code for the response.
            message: A high-level message for the error response.
        """

        self.error_response = ErrorResponse(
            message=message, status_code=status_code, error=error_detail
        )

        super().__init__(status_code=status_code, detail=self.error_response)


# ======================= 4xx Client Errors =======================


class BadRequestException(ApiException):
    """
    Used for 400 request errors, handling Bad/Malformed requests.
    """

    def __init__(
        self,
        error_code: str = "BAD_REQUEST",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "The request is invalid or malformed.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
        )


class UnauthorizedException(ApiException):
    """
    Used for 401 request errors, handling unauthorized/unauthenticated requests.
    """

    def __init__(
        self,
        error_code: str = "UNAUTHORIZED",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "Authentication is required to access this resource.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
        )


class ForbiddenException(ApiException):
    """
    Used for 403 request errors, handling forbidden request errors or
    authorization failures.
    """

    def __init__(
        self,
        error_code: str = "FORBIDDEN",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "You do not have permission to access this resource.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
        )


class NotFoundException(ApiException):
    """
    Used for 404 request errors, handling resource not found errors.
    """

    def __init__(
        self,
        error_code: str = "NOT_FOUND",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "The requested resource was not found.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
        )


class ConflictException(ApiException):
    """
    Used for 409 request errors, handling resource conflicts and duplicate entries.
    """

    def __init__(
        self,
        error_code: str = "CONFLICT",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "The request conflicts with the current state of the resource.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_409_CONFLICT,
            message=message,
        )


class UnprocessableEntityException(ApiException):
    """
    Used for 422 request errors, handling semantic validation errors and well-formed
    but invalid requests.
    """

    def __init__(
        self,
        error_code: str = "UNPROCESSABLE_ENTITY",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "The request is well-formed but contains semantic errors.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
        )


class TooManyRequestsException(ApiException):
    """
    Used for 429 request errors, handling rate limiting and quota exceeded scenarios.
    """

    def __init__(
        self,
        error_code: str = "TOO_MANY_REQUESTS",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "Rate limit exceeded. Please try again later.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
        )


# ======================= 5xx Server Errors =======================


class InternalServerException(ApiException):
    """
    Used for 500 server errors, handling unexpected internal server failures.
    """

    def __init__(
        self,
        error_code: str = "INTERNAL_SERVER_ERROR",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "An unexpected error occurred on the server.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
        )


class ServiceUnavailableException(ApiException):
    """
    Used for 503 server errors, handling temporary service unavailability.
    """

    def __init__(
        self,
        error_code: str = "SERVICE_UNAVAILABLE",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "The service is temporarily unavailable.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super().__init__(
            error_detail=error_detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=message,
        )


# ======================= Domain-Specific Exceptions =======================


class AuthenticationException(UnauthorizedException):
    """
    Used for authentication failures during login/token verification.
    """

    def __init__(
        self,
        error_code: str = "AUTHENTICATION_FAILED",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "Invalid credentials provided.",
    ):
        super().__init__(
            error_code=error_code,
            details=details,
            stack_trace=stack_trace,
            message=message,
        )


class TokenException(UnauthorizedException):
    """
    Used for JWT token validation failures, expired or malformed tokens.
    """

    def __init__(
        self,
        error_code: str = "INVALID_TOKEN",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "The provided token is invalid or expired.",
    ):
        super().__init__(
            error_code=error_code,
            details=details,
            stack_trace=stack_trace,
            message=message,
        )


class UserNotFoundException(NotFoundException):
    """
    Used when user lookup operations fail to find specified user.
    """

    def __init__(
        self,
        error_code: str = "USER_NOT_FOUND",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "User with the user id: USER_ID does not exist.",
    ):
        super().__init__(
            error_code=error_code,
            details=details,
            stack_trace=stack_trace,
            message=message,
        )


class UserAlreadyExistsException(ConflictException):
    """
    Used during user registration when email/username already exists.
    """

    def __init__(
        self,
        error_code: str = "USER_ALREADY_EXISTS",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "A user with the provided credentials already exists.",
    ):
        super().__init__(
            error_code=error_code,
            details=details,
            stack_trace=stack_trace,
            message=message,
        )


class SessionNotFoundException(NotFoundException):
    """
    Used when chat session lookup operations fail to find specified session.
    """

    def __init__(
        self,
        error_code: str = "SESSION_NOT_FOUND",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "Chat session cannot be found.",
    ):
        super().__init__(
            error_code=error_code,
            details=details,
            stack_trace=stack_trace,
            message=message,
        )


class DocumentNotFoundException(NotFoundException):
    """
    Used when document lookup operations fail to find specified document.
    """

    def __init__(
        self,
        document_id: Optional[str] = None,
        error_code: str = "DOCUMENT_NOT_FOUND",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details and document_id:
            details = f"Document with ID '{document_id}' not found."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Document not found.",
        )


class MessageNotFoundException(NotFoundException):
    """
    Used when chat message lookup operations fail to find specified message.
    """

    def __init__(
        self,
        message_id: Optional[str] = None,
        error_code: str = "MESSAGE_NOT_FOUND",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details and message_id:
            details = f"Message with ID '{message_id}' not found."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Message not found.",
        )


class DocumentUploadException(BadRequestException):
    """
    Used when document upload operations fail due to processing errors.
    """

    def __init__(
        self,
        error_code: str = "DOCUMENT_UPLOAD_ERROR",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "Failed to upload document.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
        )


class FileSizeException(BadRequestException):
    """
    Used when uploaded files exceed maximum size limits.
    """

    def __init__(
        self,
        max_size: Optional[str] = None,
        error_code: str = "FILE_SIZE_EXCEEDED",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details and max_size:
            details = f"File size exceeds maximum limit of {max_size}."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="File size limit exceeded.",
        )


class FileTypeException(BadRequestException):
    """
    Used when uploaded files have unsupported file types or formats.
    """

    def __init__(
        self,
        file_type: Optional[str] = None,
        supported_types: Optional[str] = None,
        error_code: str = "UNSUPPORTED_FILE_TYPE",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details:
            if file_type and supported_types:
                details = f"File type '{file_type}' is not supported. Supported types: {supported_types}."
            elif file_type:
                details = f"File type '{file_type}' is not supported."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Unsupported file type.",
        )


class QuotaExceededException(TooManyRequestsException):
    """
    Used when users exceed their usage quotas or subscription limits.
    """

    def __init__(
        self,
        quota_type: str = "usage",
        limit: Optional[str] = None,
        error_code: str = "QUOTA_EXCEEDED",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details:
            details = f"Your {quota_type} quota has been exceeded."
            if limit:
                details += f" Limit: {limit}."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message="Quota exceeded.",
        )


class ChatbotException(InternalServerException):
    """
    Used when AI/chatbot processing fails or encounters errors.
    """

    def __init__(
        self,
        error_code: str = "CHATBOT_ERROR",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
        message: str = "An error occurred while processing your request.",
    ):
        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
        )


class DatabaseException(InternalServerException):
    """
    Used when database operations fail or encounter connection issues.
    """

    def __init__(
        self,
        operation: str = "operation",
        error_code: str = "DATABASE_ERROR",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details:
            details = f"Database {operation} failed."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Database error.",
        )


class ExportException(InternalServerException):
    """
    Used when export operations (PDF, TXT) fail to generate or process files.
    """

    def __init__(
        self,
        export_type: str = "data",
        error_code: str = "EXPORT_ERROR",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details:
            details = f"Failed to export {export_type}."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Export error.",
        )


class ValidationException(UnprocessableEntityException):
    """
    Used when request data fails validation rules or business logic checks.
    """

    def __init__(
        self,
        field: Optional[str] = None,
        error_code: str = "VALIDATION_ERROR",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details:
            if field:
                details = f"Validation failed for field '{field}'."
            else:
                details = "Data validation failed."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error.",
        )


class PermissionException(ForbiddenException):
    """
    Used when users lack required permissions to access resources or perform actions.
    """

    def __init__(
        self,
        resource: Optional[str] = None,
        action: Optional[str] = None,
        error_code: str = "PERMISSION_DENIED",
        details: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ):
        if not details:
            if resource and action:
                details = f"You do not have permission to {action} {resource}."
            elif resource:
                details = f"You do not have permission to access {resource}."
            else:
                details = "You do not have permission to perform this action."

        error_detail = ErrorDetail(
            code=error_code, details=details, stack_trace=stack_trace
        )
        super(ApiException, self).__init__(
            error_detail=error_detail,
            status_code=status.HTTP_403_FORBIDDEN,
            message="Permission denied.",
        )
