# Personal data

## What is Personally Identifiable Information (PII)?
Personally Identifiable Information (PII) is any data that can be used to identify a specific individual. This includes direct identifiers like names and social security numbers, as well as indirect identifiers like date of birth and ZIP codes.

Protecting PII and personal data is crucial to prevent identity theft, fraud, and other harms to individuals.

### Examples of PII:
- Full name
- Social Security Number (SSN)
- Driver's license number
- Passport number
- Email address
- Phone number
- Home address
- Date of birth

## logging

The logging system in Python is a powerful and flexible way to track events that happen when some software runs. Logging is crucial for debugging, monitoring, and understanding the behavior of applications

### Key Concepts of Python Logging
**Loggers:** These are the primary entry points of the logging system. You can create multiple loggers in your application, each with a unique name. Loggers are responsible for dispatching log messages to the appropriate destination

**Handlers:** Handlers are used to send the **log records** to the appropriate destination, such as the console.

**logRecords:**  instances are created automatically by the Logger every time something is logged, The primary information is passed in msg and args

**Formatters:**  specify the layout of log records in the final output. They define the structure of the log message, including the timestamp, log level, message.

**Filters:** Filters provide a finer-grained control over which log records are passed from loggers to handlers. They can be used to filter out log messages based on specific criteria.
