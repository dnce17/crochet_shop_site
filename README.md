# Crochet Shop Application

<!-- ABOUT THE PROJECT -->
## About The Project
The Crochet Shop web app is a functional prototype e-commerce platform designed for selling handmade crochet items online. Users can browse products, add items to their cart, and update quantities.

While it doesn’t yet include features like checkout, user accounts, or payment integration, the app demonstrates the core shopping experience and responsive design for both desktop and mobile devices.

The idea for this project came from a friend who hopes to start a crochet business in the future. I built this prototype app for her, should she wish to use it as a starting point for her online shop.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
- **Languages:** Python, JavaScript, HTML, CSS
- **Backend**: Flask, Flask-SocketIO
- **Database**: SQLite
- **Deployment / Server**: Gunicorn, Gevent
- **Hosting**: Render

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps:

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dnce17/crochet_shop_site.git
   ```
2. Navigate into the project folder
   ```sh
   cd <project-folder>
   ```
3. Create a virtual environment (venv)
   ```sh
   python3 -m venv .venv
   ```
4. Activate venv
   ```sh
   source .venv/bin/activate
   ```
6. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
6. Run the development server
   ```sh
   flask run --debug
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURE EXAMPLES -->
## Features
- Browse items in the shop
- Add items to cart
- Update quantity in the cart
- Remove items from cart
- Responsive design – works on both desktop and mobile devices


