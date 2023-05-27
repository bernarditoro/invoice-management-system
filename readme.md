# Invoice Management System

The Invoice Management System is a web application designed to help manage invoices, clients, and projects. It provides features such as converting invoices to PDF, automatic email sending, and payment tracking.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

1. **Invoice to PDF Conversion**: The system allows you to convert invoices to PDF using a pre-defined HTML template. This is made possible by integrating the Python weasyprint package into the project.

2. **Automatic PDF Emailing**: When an invoice is created, the system automatically generates the corresponding PDF and sends it to the client's email address. This streamlines the process of sending invoices to clients.

3. **Payment Tracking**: Clients can pay their invoices using a special one-time link created for each invoice. The system provides a dashboard where the administrator can view pending and paid payments, making it easy to track the payment status of each invoice.

## Installation

To install and run the Invoice Management System, follow these steps:

1. Clone the repository from GitHub:

   ```
   git clone https://github.com/bernarditoro/invoice-management-system.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure the project by following the instructions in the [Configuration](#configuration) section.

4. Run the tests
   ```
   python manage.py test
   ```

5. Create superuser
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```
   python manage.py runserver
   ```

7. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. Register and log in to the application using your administrator credentials.

2. Add clients and projects to the system.

3. Create invoices for clients and assign them to specific projects.

4. View the list of invoices, their payment status, and other details on the dashboard.

5. Generate PDFs for invoices and automatically send them to clients' email addresses.

6. Track the payment status of invoices and view pending and paid payments on the dashboard.

## Configuration

To configure the Invoice Management System, follow these steps:

1. Rename the `.env_sample` file to `.env`.

2. Update the `.env` file with the necessary configurations, such as database settings, email SMTP details, and any other required settings.

3. The payment system used in the project is [Paystack](https://paystack.com/). Copy your api keys and add them to the `.env` file.

4. Customize the HTML template used for invoice PDF generation located at `templates/invoice_detail.html` to match your desired invoice format.

## Contributing

Contributions to the Invoice Management System project are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and commit them with descriptive messages.

4. Push your changes to your forked repository.

5. Submit a pull request, explaining the changes you have made and the purpose of your contribution.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code in accordance with the terms of the license.
