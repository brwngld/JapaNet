# JapaNet E-commerce Platform
![alt text](<Blue Minimalist B letter Business Company Logo (1).png>)

## Table of Contents

- [JapaNet E-commerce Platform](#japanet-e-commerce-platform)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Known Issues](#known-issues)
  - [ Related Projects](#related-projects)
  - [License](#license)
  - [Contact](#contact)

## About

JapaNet is a simple e-commerce web application built with Flask designed to serve both local and international markets, with a primary focus on promoting local businesses. Our platform offers a wide range of products sourced from local vendors, providing customers with access to unique and high-quality goods while supporting local economies.

## Features

- **Local and International Markets:** JapaNet caters to both local customers looking for locally-made products and international customers interested in unique items from different regions.
- **Promotion of Local Businesses:** Our platform prioritizes local vendors, helping them reach a wider audience and grow their businesses.
- **Secure Payment Processing:** We ensure secure transactions through encrypted payment gateways, providing customers with peace of mind when making purchases.
- **User-Friendly Interface:** Our intuitive interface makes it easy for customers to browse products, place orders, and track shipments with ease.


## Installation

To install JapaNet locally, follow these steps:

1. Make a fork of the repository: `Fork the JapaNet repository to your GitHub organization. This means that you'll have a copy of the ropository unuder your-GitHub-username/repository-name.`
2. Clone the repository: `git clone https://github.com/{your-Github-username}/JapaNet.git`
3. Navigate to the project directory: `cd JapaNet`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure environment variables as needed.
6. Run the application: `python app.py`

## Usage

Once installed, you can access JapaNet through your web browser. Simply navigate to the provided URL and start exploring the products available on the platform. Customers can search for specific items, view product details, add items to their cart, and proceed to checkout securely.

## Contributing

We welcome contributions from the community to help improve JapaNet. If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch.
2. Make your changes and ensure they adhere to the project's coding standards.
3. Test your changes thoroughly.
4. Submit a pull request with a clear description of your changes.


# Known Issues

## Incomplete Image Deletion

- **Issue**: When products are deleted from the administrator panel, associated images may not be deleted, leading to potential clutter and wasted storage space.

## Limited Search Functionality

- **Issue**: The search functionality for customers is limited to searching by brand, description, and price only. Additionally, there are no dedicated buttons or filters for these search criteria. Administrators do not have access to an implemented search algorithm.

## PDF Rendering Delays and Image Retrieval Failures

- **Issue**: Rendering PDF documents, such as receipts, using the pdfkit module may take longer than expected, especially when Bootstrap is not fully loaded. Additionally, image retrieval from the database for inclusion in PDF documents may fail intermittently. This is also dependent on an external software. Click [here](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf) to access their GitHub documentation page.

## Payment Integration for Testing Purposes Only

- **Issue**: The payment option integrated with Paystack is intended for testing purposes only. Users are required to register and obtain a live key from Paystack to fully implement payment functionality for live transactions.

For more information on installing dependencies and resolving these issues, please refer to the project documentation or relevant external resources.


# Related Projects

## Dependencies

- [Flask](https://github.com/pallets/flask) - A lightweight WSGI web application framework in Python.
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - SQL toolkit and Object-Relational Mapping (ORM) for Python.
- [Bootstrap](https://github.com/twbs/bootstrap) - Front-end framework for building responsive and mobile-first websites.
- [pdfkit](https://github.com/JazzCore/python-pdfkit) - Python wrapper for the wkhtmltopdf tool to convert HTML to PDF.

## Contributors' Projects

- [Contributor's Portfolio Website](https://github.com/contributor-username/portfolio) - Check out the portfolio of one of our contributors who helped improve JapaNet.

## Examples and Demos

- [JapaNet Demo](https://github.com/your-username/japanet-demo) - Explore a demo version of JapaNet to see its features in action.

## Images

![Home Page](images/home_page.png)

![Product Listing](images/product_listing.png)

![Checkout Process](images/checkout_process.png)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries or feedback regarding JapaNet, please contact our team:

- **GitHub Repositories:** 
[Izuchukwu Peter Abonyi](https://github.com/Drpmartins/) 
[Bernard Amegah](https://github.com/brwngld/)
- **Twitter:** 
[Izuchukwu Peter Abonyi](https://twitter.com/dr_coded)
[Bernard Amegah](https://twitter.com/bern587)
- **LinkedIn:**
[Izuchukwu Peter Abonyi](https://www.linkedin.com/in/izuchukwu-peter-abonyi-446b95278/)
[Bernard Amegah](https://www.linkedin.com/in/bernard-amegah-6191222ba/)