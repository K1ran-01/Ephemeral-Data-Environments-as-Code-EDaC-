variable "pr_number" {
  description = "The number of the pull request."
  type        = number
}

variable "pr_author" {
  description = "The username of the pull request author."
  type        = string
}

variable "service_principal_id" {
  description = "The Application ID of the service principal."
  type        = string
}
