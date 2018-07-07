from .base import APIError


_ERROR_CODE = 404  # not found


class ResourceNotFound(APIError):
    code = _ERROR_CODE
    message = 'Cannot find the resource requested for.'


class IncompleteTransaction(ResourceNotFound):
    message = 'Transaction incomplete or not found.'


class AccountNotFound(ResourceNotFound):
    message = 'Account not found.'


class BudgetNotFound(ResourceNotFound):
    message = 'Budget not found'


class CustomerNotFound(ResourceNotFound):
    message = 'Customer not found.'


class GroupNotFound(ResourceNotFound):
    message = 'Group not found.'


class OrganisationNotFound(ResourceNotFound):
    message = 'Organisation not found.'


class SavingsGoalNotFound(ResourceNotFound):
    message = 'Savings Goal not found.'
